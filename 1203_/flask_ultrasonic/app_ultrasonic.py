from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import time
import threading  ### 시험 ###
# 센서 데이터를 백그라운드에서 계속 측정하기 위한 스레드를 사용하기 위해 가져옴

app = Flask(__name__)  # 객체 생성  

# GPIO 핀 번호 설정
TRIG = 23
ECHO = 24
LED_PIN = 17
# GPIO17 - 케이블 -  저항 - (+)긴다리 led 짧은(-) - 케이블 - 그라운드(GPIO17한칸위에)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# 전역 변수(어떤 함수에서도 사용 가능)
current_distance = 0
led_status = False


# 초음파 센서로 거리를 측정 
def measure_distance():  # 거리 측정 함수
    GPIO.output(TRIG, True)
    time.sleep(0.00001)    # 1/10만초 동안 전기
    GPIO.output(TRIG, False)  # 전기 끝
    
    start_time = time.time()    # 시간 초기화
    timeout = time.time() + 0.1  # 100ms 타임아웃
    
    # ECHO 핀 값이 0(LOW)인 동안, 그리고 아직 타임아웃 시간이 지나지 않았으면 계속 반복
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start_time = time.time()
    
    # ECHO 핀 값이 1(HIGH)인 동안, 그리고 타임아웃 전까지 반복.
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        end_time = time.time()
    
    try:
        elapsed_time = end_time - start_time   # ECHO가 HIGH였던 시간(왕복 시간)을 계산.
        distance = (elapsed_time * 34300) / 2  # 편도
        return round(distance, 2)
    
    except:
        return -1  # 에러 시

# 백그라운드에서 거리 값을 계속 갱신하는 함수
def update_sensor_data():
    global current_distance  # global : 전역변수 가리키는 키워드

    while True:
        current_distance = measure_distance()   # 앞에서 만든 거리 측정 함수 호출 → 최신 거리 값을 저장
        time.sleep(0.5)  # 0.5초 딜레이

# 백그라운드에서 센서 데이터 업데이트
# threading 모듈의 Thread객체 생성. Thread랑 함수 바인딩함
sensor_thread = threading.Thread(target=update_sensor_data)  
sensor_thread.daemon = True  
#daemon : 백그라운드. 메인 종료되면 sensor_thread가 하던 작업 끝나지 않아도 강제로 종료
sensor_thread.start()


# 메인 시작
@app.route('/')
def index():
    return render_template('index.html')


# /get_distance 경로로 들어오면 실행되는 함수
@app.route('/get_distance')
def get_distance():
    return jsonify({'distance': current_distance})


# /led/on, /led/off 같은 URL로 들어왔을 때 실행
@app.route('/led/<action>')
def control_led(action):
    global led_status
    if action == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED 켜기
        led_status = True   # 상태 저장
        return jsonify({'status': 'LED ON'})    # JSON 반환
    
    elif action == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        led_status = False
        return jsonify({'status': 'LED OFF'})
    return jsonify({'status': 'Invalid action'})  # 그 외 값

# /get_led_status 요청 → 현재 LED가 켜져 있는지/꺼져 있는지 상태를 JSON으로 반환
@app.route('/get_led_status')
def get_led_status():
    return jsonify({'led_on': led_status})  # {"led_on": true} 또는 {"led_on": false} 반환


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()