import math


def count_divisors(n):
    cnt = 0
    for i in range(1, (int)(math.sqrt(n)) + 1):
        if n % i == 0:

            # If divisors are equal,
            # count only one
            if n / i == i:
                cnt = cnt + 1
            else:  # Otherwise count both
                cnt = cnt + 2

    return cnt


i = 10000
while True:
    i += 1
    v = i * (i + 1) // 2
    if count_divisors(v) > 500:
        print(v)
        break
    print(i, v, count_divisors(v))
