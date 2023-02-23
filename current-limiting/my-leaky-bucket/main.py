import time
from datetime import datetime, timedelta


class LeakyBucket:

    def __init__(self, capacity, rate):
        self._bucket_capacity = capacity  # 桶的容量
        self._rate = rate
        self.water = 0  # 水量，初始的时候为空
        self._last = datetime.now()

    def _leak(self):
        now = datetime.now()
        delta = now - self._last
        leak_amount = delta.seconds * self._rate.seconds  # 这段时间，可漏出的水量
        self.water = max(0, self.water - leak_amount)  # 算下还剩多少水在桶里，最多漏到0，也就是桶清空

    def is_allow(self) -> bool:
        self._leak()  # 更新漏桶
        if self.water < self._bucket_capacity:
            self.water += 1
            return True
        return False


if __name__ == '__main__':
    lb = LeakyBucket(10, timedelta(seconds=1))
    for i in range(10):
        if not lb.is_allow():
            print(f"num:{i} 0 - 10 should be allowed")
            exit(0)

    for i in range(10, 20):
        if lb.is_allow():
            print(f"num:{i} 10 - 20 should not be allowed, water={lb.water}")
            exit(0)

    time.sleep(1)
    for i in range(20, 30):
        if not lb.is_allow():
            print(f"num:{i} 20 - 30 should be allowed")
            exit(0)
