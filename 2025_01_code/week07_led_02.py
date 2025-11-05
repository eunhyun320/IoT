import RPi.GPIO as GPIO
import time

LED_PIN = 17  # BOARD 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)  # set output

try:
    while True:
        #GPIO.output(LED_PIN, GPIO.HIGH)
        GPIO.output(LED_PIN, 1)
        time.sleep(2)  # delay
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(2)  # delay
except KeyboardInterrupt:
    print("Exit program!")
finally:
    GPIO.cleanup()  # initialize gpio setting
