from gpiozero import LED
#import time
from time import sleep

led = LED(17)  # GPIO PIN

try:
    while True:
        led.on()
        #time.sleep(2)  # delay
        sleep(2)
        #GPIO.output(LED_PIN, GPIO.LOW)
        led.off()
        sleep(2)  # delay
except KeyboardInterrupt:
    print("Exit program!")
finally:
    #GPIO.cleanup()  # initialize gpio setting
    led.close()


# GPIO17 - 케이블 -  저항 - (+)긴다리 led 짧은(-) - 케이블 - 그라운드(GPIO17한칸위에)

