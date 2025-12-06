# GPIO17 - 케이블 -  저항 - (+)긴다리 led 짧은(-) - 케이블 - 그라운드(GPIO17한칸위에)

from gpiozero import LED    # gpiozero 라이브러리에서 LED 클래스를 가져옴
import threading    # 파이썬에서 스레드(Thread) 를 사용하기 위한 모듈. 동시(병렬) 실행 가능하도록
import time

led = LED(17)

# LED 깜빡이는 함수
# LED는 0.3초 ON → 0.3초 OFF 를 10번 반복. 총 약 6초 소요
def blink_led():
    print("LED 깜빡임 시작")
    for i in range(10):
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)
    print("LED 깜빡임 종료")

# 숫자 세는 함수
# 0.5초 × 10번 = 총 약 5초 소요
def count_numbers():
    print("카운팅 시작")
    for i in range(1, 11):
        print(f"카운트: {i}")
        time.sleep(0.5)
    print("카운팅 종료")


# 스레드 없이 실행 - 순차적
print("=== 순차 실행 ===")
start = time.time()
blink_led()
count_numbers()
# LED 깜빡이기가 끝난 후에 숫자 세기 실행
print(f"소요시간: {time.time() - start:.1f}초\n")   # 약 11초


# 스레드로 동시 실행
print("=== 동시 실행 (스레드 사용) ===")
start = time.time()

thread1 = threading.Thread(target=blink_led)    # blink_led 함수를 실행하는 스레드 생성 
thread2 = threading.Thread(target=count_numbers)    # count_numbers 함수를 실행하는 두 번째 스레드 생성

# 동시에 시작
thread1.start()
thread2.start()

# 스레드 종료 대기
thread1.join()
thread2.join()

# 더 오래 걸리는 작업 기준으로 전체 시간이 결정됨 -> 약 6초
print(f"소요시간: {time.time() - start:.1f}초")

led.close()   # LED 객체 사용 종료