from imco import *

n = 1
i = 0
primes = list(get_prime(100))
while (k := n * primes[i]) <= 1e6:
    n = k
    i += 1
print(n)
print(primes)
