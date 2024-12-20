from functools import cache

from tqdm import tqdm


@cache
def coll(n):
    count = 1
    while n != 1:
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1
        count += 1
    return count


best, val = 0, 0
for i in range(1, int(1e6)):
    if coll(i) > best:
        best = coll(i)
        val = i
print(val)
