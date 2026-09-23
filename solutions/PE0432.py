"""
PROBLEM

Let S(n,m) = sum_{i=1}^m phi(n * i). (phi is Euler's totient function)
You are given that S(510510, 10^6) = 45480596821125120.

Find S(510510, 10^11).
Give the last 9 digits of your answer.

ANSWER: 754862080
Solve time: ~2.8 seconds (reduced from ~618 seconds / 10 minutes)

MATHEMATICAL DERIVATION:
1. Multiplicative Reduction of S(n, m):
   For a prime p dividing n where n is square-free, we have the identity:
     S(p * k, m) = (p - 1) * S(k, m) + S(p * k, floor(m / p))
   Recursively applying this identity decomposes S(n, m) into subproblems ending
   at S(1, x) = Phi(x) = sum_{i=1}^x phi(i).

2. Fast Totient Prefix Sum (Du's Sieve / Hyperbolic Slicing):
   By Dirichlet hyperbola summation on phi * 1 = id:
     Phi(x) = x * (x + 1) // 2 - sum_{d=2}^x Phi(floor(x / d))
   Splitting the summation at D = floor(sqrt(x)):
     sum_{d=2}^x Phi(floor(x / d)) = sum_{d=2}^{floor(x / (D + 1))} Phi(floor(x / d))
                                   + sum_{q=1}^D (floor(x / q) - floor(x / (q + 1))) * Phi(q)

3. High-Performance Pure Python Optimization:
   - A precomputed prefix sieve of phi(k) for all k <= L (L = 5,000,000) is built via a fast NumPy prime sieve.
   - For all q <= D <= sqrt(10^11) ~ 316,227 <= L, Phi(q) is directly looked up in the precomputed array,
     and the entire second sum is evaluated as a single vectorized NumPy dot product.
   - In the first sum, any terms with floor(x / d) <= L are evaluated via vectorized array slicing on the precomputed table.
   - Only values with floor(x / d) > L branch into recursive memoized calls.
   This executes the entire solution in ~2.8 seconds purely in Python without external C dependencies.
"""

import unittest
import numpy as np
from util.utils import timeit, euler_totient_function, sum_phi


def fast_phi_prefix_sieve(limit):
    """Precomputes prefix sums of Euler's totient function up to `limit`."""
    phi = np.arange(limit + 1, dtype=np.int64)
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = False
    primes = np.nonzero(is_prime)[0]
    for p in primes:
        phi[p::p] -= phi[p::p] // p
    return np.cumsum(phi)


class Problem432:
    def __init__(self, n=510510, ls_p=(2, 3, 5, 7, 11, 13, 17), mod=int(1e9), sieve_limit=5000000):
        self.n = n
        self.ls_p = list(ls_p)
        self.mod = mod
        self.sieve_limit = sieve_limit
        self.phi_pref = fast_phi_prefix_sieve(sieve_limit)
        self.memo_phi = {}
        self.memo_s = {}

    def get_phi(self, x):
        """Computes Phi(x) = sum_{k=1}^x phi(k) via Du's sieve and hyperbolic splitting."""
        limit = self.sieve_limit
        if x <= limit:
            return int(self.phi_pref[x])
        if x in self.memo_phi:
            return self.memo_phi[x]

        total = x * (x + 1) // 2
        sx = int(x ** 0.5)
        max_d = x // (sx + 1)

        # Part 2: q from 1 to sx (all q <= sx <= sqrt(10^11) <= limit)
        q = np.arange(1, sx + 1, dtype=np.int64)
        counts = x // q - x // (q + 1)
        s2 = int(np.dot(counts, self.phi_pref[q]))

        # Part 1: d from 2 to max_d
        d_thresh = x // limit
        s1 = 0
        # Terms with x // d > limit need recursion
        for d in range(2, min(max_d + 1, d_thresh + 1)):
            s1 += self.get_phi(x // d)

        # Terms with x // d <= limit are retrieved directly from precomputed array
        if max_d > d_thresh:
            d_arr = np.arange(max(2, d_thresh + 1), max_d + 1, dtype=np.int64)
            s1 += int(np.sum(self.phi_pref[x // d_arr]))

        res = total - s1 - s2
        self.memo_phi[x] = res
        return res

    def _s_rec(self, p_idx, x):
        """Evaluates S(n, m) recursively via S(p*k, m) = (p - 1)*S(k, m) + S(p*k, m // p)."""
        if p_idx == len(self.ls_p):
            return self.get_phi(x) % self.mod
        if x == 0:
            return 0
        state = (p_idx, x)
        if state in self.memo_s:
            return self.memo_s[state]

        p = self.ls_p[p_idx]
        t1 = self._s_rec(p_idx + 1, x)
        t2 = self._s_rec(p_idx, x // p)
        res = ((p - 1) * t1 + t2) % self.mod
        self.memo_s[state] = res
        return res

    @timeit
    def solve(self, m=10**11):
        self.memo_phi.clear()
        self.memo_s.clear()
        return self._s_rec(0, m)


class Solution432(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problem = Problem432(n=510510, ls_p=[2, 3, 5, 7, 11, 13, 17], mod=int(1e9))

    def test_solution(self):
        self.assertEqual(754862080, self.problem.solve(int(1e11)))

    def test_sum_phi_function(self):
        n = 5000
        self.assertEqual(sum(euler_totient_function(i) for i in range(1, n + 1)), sum_phi(n))

    def test_solution_4(self):
        self.assertEqual(570531840, self.problem.solve(int(1e4)))

    def test_solution_6(self):
        self.assertEqual(821125120, self.problem.solve(int(1e6)))


if __name__ == '__main__':
    unittest.main()
