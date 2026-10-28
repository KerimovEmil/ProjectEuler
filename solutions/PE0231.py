"""
PROBLEM

The binomial coefficient comb(10, 3) = 120.
120 = 2^3 * 3 * 5 = 2 * 2 * 2 * 3 * 5, and 2 + 2 + 2 + 3 + 5 = 14.
So the sum of the terms in the prime factorisation of comb(10, 3) is 14.

Find the sum of the terms in the prime factorisation of comb(20,000,000, 15,000,000).

ANSWER: 7526965179680
Solve time: ~0.09 seconds

---
MATHEMATICAL DERIVATION:

1. Additive Valuation via Legendre's Formula:
   Let S(m) denote the sum of prime factors of m counted with multiplicity:
     S(prod p_i^{e_i}) = sum p_i * e_i.
   Since comb(n, k) = n! / (k! * (n - k)!), the p-adic valuation v_p(comb(n, k)) satisfies:
     v_p(comb(n, k)) = v_p(n!) - v_p(k!) - v_p((n - k)!).
   By Legendre's formula, for any prime p <= n:
     v_p(n!) = sum_{j >= 1} floor(n / p^j),
   so the sum of terms in the prime factorization of comb(n, k) is:
     S(comb(n, k)) = sum_{p <= n} p * sum_{j >= 1} (floor(n / p^j) - floor(k / p^j) - floor((n - k) / p^j)).

2. Vectorized Evaluation via Splitting at sqrt(n):
   - For j = 1, we evaluate sum_{p <= n} p * (floor(n / p) - floor(k / p) - floor((n - k) / p)) across all
     primes p <= n in a single vectorized NumPy operation.
   - For j >= 2, only primes p <= isqrt(n) (at most 4,472 primes for n = 20,000,000) have p^j <= n. We accumulate
     the higher-power contributions p * (floor(n / p^j) - floor(k / p^j) - floor((n - k) / p^j)) for those small
     primes in a tiny loop.
   This computes S(comb(20,000,000, 15,000,000)) in ~0.09 seconds.
"""

import math
import unittest
import numpy as np
from util.utils import primes_upto, timeit


class Problem231:
    def __init__(self, n: int = 20_000_000, k: int = 15_000_000):
        self.n = n
        self.k = k

    @staticmethod
    def sum_prime_factors_binomial(n: int, k: int) -> int:
        m = n - k
        primes = primes_upto(n).astype(np.int64)

        # j = 1 contribution across all primes <= n
        counts_j1 = (n // primes) - (k // primes) - (m // primes)
        total = int(np.sum(primes * counts_j1))

        # j >= 2 contributions only for primes <= isqrt(n)
        limit_sqrt = math.isqrt(n)
        for p in primes:
            p_int = int(p)
            if p_int > limit_sqrt:
                break
            pk = p_int * p_int
            exp_high = 0
            while pk <= n:
                exp_high += (n // pk) - (k // pk) - (m // pk)
                pk *= p_int
            total += p_int * exp_high

        return total

    @timeit
    def solve(self) -> int:
        return self.sum_prime_factors_binomial(self.n, self.k)


class Solution231(unittest.TestCase):
    def setUp(self):
        self.problem = Problem231()

    def test_sample(self):
        self.assertEqual(14, self.problem.sum_prime_factors_binomial(10, 3))

    def test_solution(self):
        self.assertEqual(7526965179680, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
