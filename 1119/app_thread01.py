import time

print("=== 스레드 없이 실행 ===")
def count_task(name,count):
    for i in range(count):
        print(f"{name}: {i+1}")
        time.sleep(0.5)
    

start = time.time()
count_task("작업A", 3)
count_task("작업B", 3)
print(f"총 소요시간: {time.time() - start:.1f}초\n")