import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17
RED_LED = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RED_LED, GPIO.OUT)

try:
    while True:
        state = GPIO.input(BUTTON_PIN)
        print(f"스위치 상태 : {state}")
        if state == 1:
            GPIO.output(RED_LED, 1)
        else:
            GPIO.output(RED_LED, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    GPIO.cleanup()

