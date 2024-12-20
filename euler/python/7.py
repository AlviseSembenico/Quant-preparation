from functools import cache


@cache
def is_prime(n):
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


p = 0
n = 2
while p < 10001:
    if is_prime(n):
        p += 1
    n += 1

print(n - 1)
