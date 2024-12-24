from imco import *

MOD = int(1e6)


@lru_cache(None)
def m(n, sat):
    if n < 0:
        return 0
    if n == 1 or n == 0:
        if sat:
            return 1
        return 0

    res = 0
    for i in range(1, n + 1):
        res += m(n - i, sat or i == 2)
        res = res % MOD
    return res


def t(n):
    if n == 1:
        return 1
    if n == 0:
        return 1

    res = 0
    # even number
    if n % 2 == 0:
        res += m(n // 2, False)
        res = res % MOD

    for i in range(1, n + 1):
        if ((n - i) % 2) == 0:
            res += m((n - i) // 2, i == 2)
            res = res % MOD
    return res


"""
3 -> 0
4 -> 121, 2,2
"""
print(t(6), t(20), t(42))
i = 43
while t(i) % MOD != 0:
    i += 1
    # print(i, t(i))
print("result ", i)
