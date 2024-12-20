from icecream import ic


def f(n):
    a = (n**3 - n) / 3 + n * (n + 1) / 2 - n**2 * (n + 1) ** 2 / 4
    return -a


print(f(100))
