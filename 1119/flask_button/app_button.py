from flask import Flask, render_template, jsonify
from gpiozero import LED, Button
import time
import random
import threading

app = Flask(__name__)  

# GPIO 설정
led = LED(17)
button = Button(27, pull_up=True)   # 풀업 저항 사용 (pull_up=True) → 평상시 HIGH, 눌렀을 때 LOW

# 스레드 안전성을 위한 락
state_lock = threading.Lock()

# 게임 상태
game_state = {
    'status': 'ready',  # ready, waiting, measuring, result, early_press, timeout
    'reaction_time': 0,
    'start_time': 0,
    'best_score': None
}


# 타임아웃 타이머
# 5초 안 누르면 자동으로 타임아웃 처리하는 타이머를 저장해 둘 변수
timeout_timer = None       # timeout_timer 전역 변수를 None으로 초기화


# 버튼 눌렀을 때 실행되는 함수
def game_logic():
    """버튼이 눌렸을 때 실행"""
    global timeout_timer
    
    with state_lock:    # state_lock으로 락을 걸면서 아래 블록 실행
        if game_state['status'] == 'measuring':
            # 정상 반응 - 반응 시간 측정
            reaction = (time.time() - game_state['start_time']) * 1000  # ms로 변환
            game_state['reaction_time'] = round(reaction, 2)    # 반응시간 저장. 소수 둘째 자리까지 반올림
            game_state['status'] = 'result'  # 상태를 result로 변경
            led.off()   # LED 끄기
            
            # 타임아웃 타이머 취소
            # 만약 타임아웃을 담당하던 타이머가 실행 대기 중이었다면(timeout_timer가 None이 아니면),
            # .cancel() 해서 타임아웃 스레드가 실행되지 않도록 취소
            if timeout_timer:
                timeout_timer.cancel()
            
            # 최고 기록 업데이트(최고 기록이 없거나(None), 이번 기록 reaction이 기존 최고 기록보다 더 작다면(더 빠르면))
            if game_state['best_score'] is None or reaction < game_state['best_score']:
                game_state['best_score'] = round(reaction, 2)
        

        elif game_state['status'] == 'waiting':
            # 너무 빨리 누름 (얼리 프레스)
            game_state['status'] = 'early_press'
            game_state['reaction_time'] = 0
            led.off()
            
            # 타임아웃 타이머 취소
            if timeout_timer:
                timeout_timer.cancel()


# 버튼 이벤트 연결(GPIO 버튼이 눌리면 game_logic() 실행)
button.when_pressed = game_logic


# 메인페이지
@app.route('/')
def index():
    return render_template('index.html')


# /start URL로 POST 요청이 들어오면 start_game() 함수가 실행
@app.route('/start', methods=['POST'])
def start_game():
    """게임 시작"""
    global timeout_timer    # 전역 timeout_timer를 수정해야 하므로 global 선언
    
    with state_lock:
        # 게임이 이미 진행중일 때(ready 상태일때만 새로 시작 가능)
        if game_state['status'] != 'ready':     
            return jsonify({'error': '게임이 이미 진행중입니다'}), 400  # 에러
        
        game_state['status'] = 'waiting'
        game_state['reaction_time'] = 0
        game_state['start_time'] = 0
    
    # 랜덤 딜레이 후 LED 켜기 (스레드)
    def delayed_led():
        global timeout_timer
        
        # 1~4초 사이 랜덤 대기
        delay = random.uniform(1, 4)    # 실수 랜덤 값을 생성
        time.sleep(delay)   # 이 시간 동안은 LED가 켜지지 않은 상태이고, 사용자는 언제 켜질지 모르는 상태에서 기다리는 게임 구조
        
        with state_lock:
            # waiting 상태가 유지되는지 확인 (얼리 프레스로 취소되지 않았는지)
            if game_state['status'] == 'waiting':   # 1초~4초 대기 후 상태가 waiting이면
                led.on()
                game_state['start_time'] = time.time()
                game_state['status'] = 'measuring'

        
        # 타임아웃 설정 (5초). 5초 뒤에 실행될 함수.
        def handle_timeout(): 
            with state_lock:
                # LED가 켜진 상태(measuring)에서 5초 동안 버튼을 안 누르면
                if game_state['status'] == 'measuring':
                    led.off()
                    game_state['status'] = 'timeout'
                    game_state['reaction_time'] = 0
        
        timeout_timer = threading.Timer(5.0, handle_timeout)    # 5초 후에 handle_timeout()을 실행하는 타이머 객체를 생성.
        timeout_timer.start()
    
    thread = threading.Thread(target=delayed_led)   # delayed_led 함수를 실행하는 새 스레드를 만듦
    thread.daemon = True  # daemon : 백그라운드에서 돌아갈 수 있는 스레드. 메인 프로그램이 종료될 때 같이 자동으로 종료
    thread.start()
    
    return jsonify({'message': '준비... LED가 켜지면 버튼을 누르세요!'})


# /status URL로 GET 요청이 오면 이 함수 실행
@app.route('/status')
def get_status():
    """현재 상태 반환"""
    with state_lock:
        return jsonify({
            'status': game_state['status'],
            'reaction_time': game_state['reaction_time'],
            'best_score': game_state['best_score']
        })


# /reset URL로 POST 요청이 오면 reset_game() 함수 실행
@app.route('/reset', methods=['POST'])
def reset_game():
    """게임 리셋"""
    global timeout_timer
    
    # 타임아웃 타이머 취소
    if timeout_timer:
        timeout_timer.cancel()
    
    led.off()
    
    with state_lock:
        game_state['status'] = 'ready'
        game_state['reaction_time'] = 0
        game_state['start_time'] = 0
    
    return jsonify({'message': '리셋 완료'})


if __name__ == '__main__':  # 프로그램 실행
    try:
        # 재시작 방지 및 프로덕션 모드
        # import os
        # os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        print("반응속도 게임 서버 시작...")
        print("http://0.0.0.0:5000 접속하세요")
        app.run(host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
    finally:
        led.off()
        print("GPIO 정리 완료")