from imco import *


@cache
def f(n, m):
    if n == 0 or m == 0:
        return 1
    return f(n - 1, m) + f(n, m - 1)


print(f(20, 20))
# for i in range(2, 5):
#     print(f(i, i))
