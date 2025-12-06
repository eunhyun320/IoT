from flask import Flask, render_template, request, redirect, url_for
# import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep

app = Flask(__name__)  # Flask 앱 객체 생성

# GPIO 설정
# GPIO.setmode(GPIO.BCM)
# LED1 = 20
# LED2 = 21

led1 = LED(5)  # GPIO PIN. 5번 핀
led2 = LED(6) 

# GPIO.setup(LED1, GPIO.OUT)
# GPIO.setup(LED2, GPIO.OUT)

# LED 상태 저장(0 → OFF, 1 → ON)
led_states = {'led1': 0, 'led2': 0}


# 메인페이지
@app.route('/')
def index():
    return render_template('index.html', states=led_states)   # index.html을 불러오면서 LED 상태(states)를 HTML로 전달


# 개별 LED 제어 URL
@app.route('/led/<int:led_num>/<int:state>')
def control_led(led_num, state):   # /led/1/1 → LED1 ON, /led/1/0 → LED1 OFF, /led/2/1 → LED2 ON
    """개별 LED 제어"""
    if led_num == 1:
        # GPIO.output(LED1, state)
        if state == 1:
            led1.on()
        else:
            led1.off()

        led_states['led1'] = state   # 상태를 led_states에 저장

    elif led_num == 2:
        # GPIO.output(LED2, state)
        if state == 1:
            led2.on()
        else:
            led2.off()

        led_states['led2'] = state
    
    return redirect(url_for('index'))   # LED 켠 뒤 메인 페이지로 다시 이동

# 모든 LED 동시 제어
@app.route('/all/<int:state>')
def all_leds(state):    # /all/1 → LED1, LED2 모두 ON, /all/0 → 모두 OFF
    """모든 LED 동시 제어"""
    # GPIO.output(LED1, state)
    # GPIO.output(LED2, state)
    if state == 1:
        led1.on()
        led2.on()
    else:
        led1.off()
        led2.off()
        
    led_states['led1'] = state
    led_states['led2'] = state
    
    return redirect(url_for('index'))


if __name__ == '__main__':  # 프로그램 실행
    try:
        app.run(host='192.168.55.45', port=5000)
        
    finally:    # 프로그램 종료 시 GPIO 해제
        # GPIO.cleanup()
        led1.close()
        led2.close()
        # lgpio.gpio.unclaim()