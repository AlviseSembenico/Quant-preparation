import math

import numpy


def apply(dist, f):
    return set([(f(k), v) for k, v in dist])


def coapply(dist1, dist2, f):
    return set([(f(k1, k2), v1) for k1, v1 in dist1 for k2, v2 in dist2])


def expected_value(dist):
    return sum([key * value for (key, value) in dist])


def variance(dist):
    return math.sqrt(
        expected_value(apply(dist, lambda x: (x - expected_value(dist)) ** 2))
    )


# def covariance(dist1, dist2):
#     return expected_value(
#         coapply(
#             dist1,
#             dist2,
#             lambda x, y: (x - expected_value(dist1)) * (y - expected_value(dist2)),
#         )
#     )


def bayes(p_a, p_b_given_a, p_b_given_not_a):
    p_not_a = 1 - p_a
    p_b = p_b_given_a * p_a + p_b_given_not_a * p_not_a
    return p_b_given_a * p_a / p_b


def main():
    dist = set([(1, 1 / 6), (2, 1 / 6), (3, 1 / 6), (4, 1 / 6), (5, 1 / 6), (6, 1 / 6)])
    print(expected_value(dist))
    print(variance(dist))


if __name__ == "__main__":
    main()
