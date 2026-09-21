"""
PROBLEM

For a positive integer n, let σ2(n) be the sum of the squares of its divisors. For example,

σ2(10) = 1 + 4 + 25 + 100 = 130.
Find the sum of all n, 0 < n < 64,000,000 such that σ2(n) is a perfect square.

ANSWER: 1922364685
Solve time: ~4.8 seconds
"""

import math
import unittest
import numpy as np
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Multiplicative Divisor Square Sum Function:
#    For n = prod p_i^{a_i}, the sum of squares of divisors is:
#      sigma_2(n) = prod_{i} (1 + p_i^2 + p_i^4 + ... + p_i^{2 a_i})
#                 = prod_{i} (p_i^{2 a_i + 2} - 1) / (p_i^2 - 1)
#
# 2. Vectorized Sieve via Small Primes:
#    For N = 64,000,000, any integer n < N has at most one prime factor p > sqrt(N) = 8000.
#    There are only 1007 primes p <= 8000.
#    - We initialize sigma2 = np.ones(N, dtype=np.int64) and rem = np.arange(N, dtype=np.int32).
#    - For each small prime p <= 8000:
#        We track the multiplicity e of p across all multiples and divide rem[p^k::p^k] by p.
#        We multiply sigma2[p::p] by the corresponding factor (1 + p^2 + ... + p^{2e}).
#    - For all remaining elements where rem[i] > 1, rem[i] is prime:
#        sigma2[i] *= (1 + rem[i]^2).
#
# 3. Perfect Square Detection:
#    Using vector operations, check if int(sqrt(sigma2))^2 == sigma2.
#    Sum all valid indices in [1, N-1]. Total runtime is ~4.8s.


class Problem211:
    def __init__(self, limit: int = 64_000_000):
        self.limit = limit

    @timeit
    def solve(self, limit: int = None) -> int:
        if limit is None:
            limit = self.limit

        limit_sqrt = math.isqrt(limit)

        # Sieve primes up to sqrt(limit)
        is_p = bytearray([1]) * (limit_sqrt + 1)
        is_p[0] = is_p[1] = 0
        for p in range(2, math.isqrt(limit_sqrt) + 1):
            if is_p[p]:
                is_p[p * p::p] = bytearray(len(is_p[p * p::p]))
        small_primes = [p for p in range(2, limit_sqrt + 1) if is_p[p]]

        sigma2 = np.ones(limit, dtype=np.int64)
        rem = np.arange(limit, dtype=np.int32)

        for p in small_primes:
            p2 = p * p
            p_pow = p

            num_multiples = len(sigma2[p::p])
            exp = np.zeros(num_multiples + 1, dtype=np.int8)

            while p_pow < limit:
                rem[p_pow::p_pow] //= p
                step = p_pow // p
                exp[step::step] += 1
                p_pow *= p

            max_e = int(exp.max())
            factor_table = np.ones(max_e + 1, dtype=np.int64)
            cur_term = 1
            cur_p2 = 1
            for e in range(1, max_e + 1):
                cur_p2 *= p2
                cur_term += cur_p2
                factor_table[e] = cur_term

            sigma2[p::p] *= factor_table[exp[1:num_multiples + 1]]

        # Multiply primes > sqrt(limit)
        mask = rem > 1
        rem_primes = rem[mask].astype(np.int64)
        sigma2[mask] *= (1 + rem_primes * rem_primes)

        # Vectorized square check
        sq = np.sqrt(sigma2[1:].astype(np.float64)).astype(np.int64)
        is_square = (sq * sq == sigma2[1:])

        return int(np.sum(np.flatnonzero(is_square).astype(np.int64) + 1))


class Solution211(unittest.TestCase):
    def setUp(self):
        self.problem = Problem211()

    def test_small(self):
        # For n <= 100, 1 (sigma2=1=1^2), 42 (sigma2=2500=50^2) -> sum = 1 + 42 = 43
        self.assertEqual(43, self.problem.solve(limit=100))

    def test_solution(self):
        self.assertEqual(1922364685, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
