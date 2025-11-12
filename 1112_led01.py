from gpiozero import LED
#import time
from time import sleep

led_red = LED(20)  # GPIO PIN
led_blue = LED(21) 
try:
    while True:
        led_red.on()
        led_blue.on()
        #time.sleep(2)  # delay
        sleep(2)
        #GPIO.output(LED_PIN, GPIO.LOW)
        led_red.off()
        led_blue.off()
        sleep(2)  # delay
except KeyboardInterrupt:
    print("Exit program!")
finally:
    #GPIO.cleanup()  # initialize gpio setting
    led_red.close()
    led_blue.close()


# GPIO17 - 케이블 -  저항 - (+)긴다리 led 짧은(-) - 케이블 - 그라운드(GPIO17한칸위에)

