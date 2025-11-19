import time
import threading

print("=== 스레드 없이 실행 ===")
def count_task(name,count):
    for i in range(count):
        print(f"{name}: {i+1}")
        time.sleep(0.5)
    

start = time.time()

# 멀티 스레드 : 멀티 가능이라 각 1.5초 이고 총 소요시간도 1.5초임
t1 = threading.Thread(target=count_task, args=("작업A", 3))
t2 = threading.Thread(target=count_task, args=("작업B", 3))
t3 = threading.Thread(target=count_task, args=("작업C", 3))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# 아래처럼 쓰면 멀티 스레드 아니어서 각각 1.5초씩이라 총 3초 걸림
# count_task("작업A", 3)
# count_task("작업B", 3)

print(f"총 소요시간: {time.time() - start:.1f}초\n")