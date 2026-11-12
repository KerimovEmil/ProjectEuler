r"""
PROBLEM

A k-bounded partition of a positive integer N is a way of writing N as a sum of positive integers that do not exceed k.

A balanceable partition is a partition that can be split into two sub-multisets of equal sums.

For example, 3 + 2 + 2 + 2 + 2 + 1 is a balanceable 3-bounded partition of 12, since 3 + 2 + 1 = 2 + 2 + 2 = 6.
Conversely, 3 + 3 + 3 + 3 is a 3-bounded partition of 12 that is not balanceable.

Let f(k) be the smallest positive integer N such that all k-bounded partitions of N are balanceable.
For example, f(3) = 12 and f(6) = 120.

Find f(10^8). Give your answer modulo 1,000,000,007.

ANSWER: 83985379
Solve time: ~0.9 seconds

---
MATHEMATICAL DERIVATION:

1. Divisibility Requirement:
   For every integer d with 1 <= d <= k, consider the partition consisting entirely of parts equal to d:
     N = d + d + ... + d = (N / d) * d.
   For this partition to be balanceable, we must be able to partition these parts into two sets of equal sum N/2.
   Since each part is d, any subset sum is a multiple of d.
   Thus N/2 must be an integer multiple of d for every d in {1, 2, ..., k}.
   Consequently, lcm(1, 2, ..., k) must divide N/2, which implies:
     N >= 2 * lcm(1, 2, ..., k).

2. Sufficiency:
   It is a known combinatorial result that for N = 2 * lcm(1, 2, ..., k), every k-bounded partition
   is indeed balanceable.
   Hence f(k) = 2 * lcm(1, 2, ..., k).
   Verified against given values:
     f(3) = 2 * lcm(1, 2, 3) = 2 * 6 = 12.
     f(6) = 2 * lcm(1, 2, 3, 4, 5, 6) = 2 * 60 = 120.

3. Computation for k = 10^8 modulo 10^9 + 7:
   The prime factorization of lcm(1, 2, ..., k) is:
     lcm(1, 2, ..., k) = prod_{p <= k} p^(floor(log_p(k))).
   For primes p > sqrt(k) = 10^4, the exponent floor(log_p(k)) is exactly 1.
   For primes p <= 10^4, the exponent is floor(log_p(k)).
   We sieve primes up to 10^8 via NumPy, compute prime powers for small primes p <= 10^4,
   and multiply large primes p > 10^4 with exponent 1 directly modulo 1,000,000,007 in ~0.9 seconds.
"""

import math
import unittest
import numpy as np

from util.utils import timeit


class Problem772:
    def __init__(self, limit: int = 10**8, mod: int = 1000000007):
        self.limit = limit
        self.mod = mod

    def compute_f(self, k: int, mod: int | None = None) -> int:
        if mod is None:
            mod = self.mod
        if k < 2:
            return 2 if k == 1 else 0

        max_i = (k - 1) // 2
        sieve = np.ones(max_i + 1, dtype=bool)
        sieve[0] = False
        sqrt_k = math.isqrt(k)
        for i in range(1, sqrt_k // 2 + 1):
            if sieve[i]:
                p = 2 * i + 1
                sieve[(p * p - 1) // 2 :: p] = False

        primes = (2 * np.flatnonzero(sieve) + 1).astype(np.int64)

        ans = 2
        p2 = 1
        while p2 * 2 <= k:
            p2 *= 2
        ans = (ans * p2) % mod

        idx = np.searchsorted(primes, sqrt_k + 1)
        small_primes = primes[:idx]
        large_primes = primes[idx:]

        for p in small_primes:
            pw = int(p)
            while pw * p <= k:
                pw *= p
            ans = (ans * pw) % mod

        for p in large_primes.tolist():
            ans = (ans * p) % mod

        return ans

    @timeit
    def solve(self) -> int:
        return self.compute_f(self.limit, self.mod)


class Solution772(unittest.TestCase):
    def setUp(self):
        self.problem = Problem772()

    def test_samples(self):
        self.assertEqual(12, self.problem.compute_f(3))
        self.assertEqual(120, self.problem.compute_f(6))

    def test_solution(self):
        self.assertEqual(83985379, self.problem.solve())


if __name__ == "__main__":
    unittest.main()
