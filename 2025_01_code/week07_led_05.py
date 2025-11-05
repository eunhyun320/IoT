import RPi.GPIO as GPIO
from time import sleep

red_led = 17  
green_led = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

try:
    while True:
        GPIO.output(red_led, 1)
        GPIO.output(green_led, 0)
        sleep(2)
        GPIO.output(red_led, GPIO.LOW)
        GPIO.output(green_led, GPIO.HIGH)
        sleep(2)  # delay
except KeyboardInterrupt:
    print("Exit program!")
finally:
    GPIO.cleanup()



