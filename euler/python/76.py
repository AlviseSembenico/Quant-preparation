from imco import *

cache = {}


def f(n, t):
    if n == 1:
        return 1
    if n == 2:
        return 1
    res = 0
    for i in range(1, floor(n / 2) + 1):
        res += f(i) + f(n - 1)
    return res


def f(n):
    # Create a list to store partition counts
    partitions = [0] * (n + 1)

    # Base case: there's one way to partition 0 (the empty set)
    partitions[0] = 1

    # Fill the partitions array using the recurrence relation
    for i in range(1, n + 1):  # Iterate over all possible summands
        for j in range(i, n + 1):  # Add the summand to partitions[j]
            partitions[j] += partitions[j - i]

    # Total partitions of n is partitions[n]
    # Subtract 1 to exclude the partition consisting of just [n]
    return partitions[n] - 1


for i in range(2, 8):
    print(f(i))

print(f(100))
