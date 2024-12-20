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


res = 0
for i in range(int(2e6) + 1):
    if is_prime(i):
        res += i
print(res)
