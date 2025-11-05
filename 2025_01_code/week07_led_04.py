from gpiozero import LED
from time import sleep

red_led = LED(17)  # GPIO PIN
green_led = LED(27)  # GPIO PIN
 
try:
    while True:
        red_led.on()
        green_led.off()
        sleep(2)
        red_led.off()
        green_led.on()
        sleep(2)  # delay
except KeyboardInterrupt:
    print("Exit program!")
finally:
    red_led.close()
    green_led.close()


