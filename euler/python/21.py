from imco import *


# @cache
def sum_divisors(n):
    res = 0
    for i in range(1, n // 2 + 2):
        if n % i == 0:
            res += i
    return res


seen = set()

res = 0
for i in range(1, 10000):
    if i in seen:
        continue
    b = sum_divisors(i)
    if b == i:
        continue
    if sum_divisors(b) == i:
        res += i
        if i != b:
            res += b
        seen.add(b)
        print(i, b)

print(res)
