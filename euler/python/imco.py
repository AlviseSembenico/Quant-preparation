from functools import *
from math import *

import numpy as np
from tqdm import *


def is_prime(n):
    """ "pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2  # return False
    k = 3
    while k * k <= n:
        if n % k == 0:
            return False
        k += 2
    return True


def get_prime(limit=None):
    i = 2
    count = 0
    while limit is None or count < limit:
        if is_prime(i):
            yield i
            count += 1
        i += 1
