import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 정의
TRIG = 23
ECHO = 24
RED_LED = 5  # 빨간색 LED를 GPIO 5번 핀에 연결
GREEN_LED = 6  # 녹색 LED를 GPIO 6번 핀에 연결
THRESHOLD = 5  # 거리 임계값 (cm)

def setup():
    GPIO.setmode(GPIO.BCM)
    
    # 초음파 센서 핀 설정
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # LED 핀 설정
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    
    # 초기 상태 설정
    GPIO.output(TRIG, False)
    GPIO.output(RED_LED, False)
    GPIO.output(GREEN_LED, False)
    
    print("초음파센서 및 LED 준비 중 ....")
    time.sleep(2)

def get_distance():
    # 초음파 발사
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10us
    GPIO.output(TRIG, False)
    
    # ECHO 핀에 HIGH가 될 때까지 측정
    pulse_start = time.time()
    time_out = pulse_start + 1
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > time_out:
            return -1
    
    # ECHO 핀에 LOW가 될 때까지 측정
    pulse_end = time.time()
    time_out = pulse_end + 1
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > time_out:
            return -1
    
    # 시간차 계산
    pulse_duration = pulse_end - pulse_start
    # 거리 계산 (음속 34300cm/s)
    distance = pulse_duration * 34300 / 2
    return round(distance, 2)

def update_leds(distance):
    if distance <= THRESHOLD and distance > 0:
        # 5cm 이내로 물체 접근 시 빨간색 LED 켜기, 녹색 LED 끄기
        GPIO.output(RED_LED, True)
        GPIO.output(GREEN_LED, False)
        print(f"물체 접근: {distance}cm - 빨간색 LED ON")
    else:
        # 5cm를 벗어나면 녹색 LED 켜기, 빨간색 LED 끄기
        GPIO.output(RED_LED, False)
        GPIO.output(GREEN_LED, True)
        print(f"안전 거리: {distance}cm - 녹색 LED ON")

def cleanup():
    GPIO.cleanup()
    print("GPIO 자원 회수 완료")

if __name__ == "__main__":
    try:
        setup()
        while True:
            distance = get_distance()
            if distance == -1:
                print("측정 오류: 신호를 받지 못함")
            else:
                print(f"거리: {distance}cm")
                update_leds(distance)
            time.sleep(0.5)  # 측정 주기 (0.5초)
    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        cleanup()