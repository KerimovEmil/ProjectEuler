"""
PROBLEM

Find the number of integers 1 < n < 10^7, for which n and n + 1 have the same number of positive divisors.
For example, 14 has the positive divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15.

ANSWER: 986262
Solve time: ~0.38 seconds
"""

import math
import unittest
import numpy as np
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Multiplicative Divisor Function:
#    For n = prod p_i^{a_i}, the divisor count function is:
#      tau(n) = prod (a_i + 1)
#
# 2. Vectorized Sieve via Small Primes:
#    Since n <= 10^7, any number n has at most ONE prime factor p > sqrt(n) ~ 3162.
#    There are only 446 primes p <= 3162.
#    - We maintain an array rem = [0, 1, 2, ..., n] and tau = [1, 1, 1, ..., 1].
#    - For each small prime p <= sqrt(n):
#        For each power p^k <= n, we compute the multiplicity of p and divide rem[p^k :: p^k] by p.
#        We multiply tau[p :: p] by (e + 1).
#    - After processing all primes p <= sqrt(n):
#        If rem[i] > 1, then rem[i] is prime (since it has no prime factors <= sqrt(n) and i <= n < (sqrt(n)+1)^2).
#        Therefore, we multiply tau[rem > 1] by 2.
#
# 3. Consecutive Divisor Comparison:
#    Count indices 2 <= i < n where tau[i] == tau[i + 1] using numpy vectorization.
#    Total runtime is ~0.38s (down from ~18s).


class Problem179:
    def __init__(self, n: int = 10**7):
        self.n = n

    @timeit
    def solve(self, n: int = None) -> int:
        if n is None:
            n = self.n

        limit_sqrt = math.isqrt(n)

        # Sieve primes up to sqrt(n)
        is_p = bytearray([1]) * (limit_sqrt + 1)
        is_p[0] = is_p[1] = 0
        for p in range(2, math.isqrt(limit_sqrt) + 1):
            if is_p[p]:
                is_p[p * p::p] = bytearray(len(is_p[p * p::p]))
        small_primes = [p for p in range(2, limit_sqrt + 1) if is_p[p]]

        tau = np.ones(n + 1, dtype=np.int16)
        rem = np.arange(n + 1, dtype=np.int32)

        for p in small_primes:
            p_pow = p
            exp = np.zeros(n // p + 1, dtype=np.int8)
            while p_pow <= n:
                rem[p_pow::p_pow] //= p
                exp[p_pow // p::p_pow // p] += 1
                p_pow *= p
            tau[p::p] *= (exp[1:] + 1)

        # Any remaining factor > 1 is a prime > sqrt(n)
        tau[rem > 1] *= 2

        return int(np.count_nonzero(tau[2:n] == tau[3:n + 1]))


class Solution179(unittest.TestCase):
    def setUp(self):
        self.problem = Problem179(n=int(1e7))

    def test_example(self):
        # 14 and 15 both have 4 divisors
        # For n = 15, valid pairs below 15: (2,3) both have 2, (14,15) both have 4
        self.assertEqual(2, self.problem.solve(n=15))

    def test_solution(self):
        self.assertEqual(986262, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
