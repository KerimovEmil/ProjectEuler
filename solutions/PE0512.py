"""
PROBLEM

Let phi(n) be Euler's totient function.

Let f(n) = (sum_{i=1}^n phi(n^i)) mod (n + 1).

Let g(n) = sum_{i=1}^n f(i).

g(100) = 2007.

Find g(5 * 10^8).

ANSWER: 50660591862310323
Solve time: ~0.85 seconds

---
MATHEMATICAL DERIVATION:

1. Algebraic Simplification of f(n):
   For any integer n >= 1 and i >= 1, the prime factors of n^i are identical to the prime factors of n.
   Thus:
     phi(n^i) = n^{i-1} * phi(n).
   Summing over i = 1, ..., n:
     sum_{i=1}^n phi(n^i) = phi(n) * sum_{i=1}^n n^{i-1} = phi(n) * (n^n - 1) / (n - 1)   (for n > 1).
   Modulo (n + 1), we have n = -1 mod (n + 1):
     sum_{i=1}^n n^{i-1} = 1 + n + n^2 + ... + n^{n-1}
                         = 1 - 1 + 1 - 1 + ... + (-1)^{n-1} mod (n + 1).
   - If n is even, the sum has an even number n of alternating terms, so:
       sum_{i=1}^n n^{i-1} = 0 mod (n + 1)  ==>  f(n) = 0.
   - If n is odd, the sum has an odd number n of alternating terms, so:
       sum_{i=1}^n n^{i-1} = 1 mod (n + 1)  ==>  f(n) = phi(n) mod (n + 1).
   Since 0 < phi(n) < n + 1 for all n >= 1, f(n) = phi(n) when n is odd, and f(n) = 0 when n is even!

2. Decomposition of g(n):
   Therefore, g(n) is simply the sum of phi(k) over all odd integers 1 <= k <= n:
     g(n) = sum_{1 <= k <= n, k odd} phi(k).
   Expressing any integer k uniquely as k = 2^j * m with m odd:
     sum_{k=1}^n phi(k) = sum_{j >= 0} sum_{m <= floor(n / 2^j), m odd} phi(2^j * m).
   Since phi(2^j * m) = phi(2^j) * phi(m) for odd m, where phi(2^0) = 1 and phi(2^j) = 2^{j-1} for j >= 1:
     sum_{k=1}^n phi(k) = g(n) + sum_{j >= 1} 2^{j-1} * g(floor(n / 2^j)).
   Subtracting the same identity evaluated at floor(n / 2):
     sum_{k=1}^{floor(n / 2)} phi(k) = g(floor(n / 2)) + sum_{j >= 1} 2^{j-1} * g(floor(n / 2^{j+1})).
   Multiplying by 2 and subtracting yields:
     g(n) = sum_{k=1}^n phi(k) - 2 * sum_{k=1}^{floor(n / 2)} phi(k) + g(floor(n / 2)).
   Telescoping over successive divisions by 2:
     g(n) = sum_{j >= 0} ( Phi(floor(n / 2^j)) - 2 * Phi(floor(n / 2^{j+1})) ),
   where Phi(x) = sum_{i=1}^x phi(i) is the totient summatory function.

3. Sublinear Totient Summation (Du's Sieve):
   We precompute a linear phi sieve up to L = 3,500,000 via NumPy.
   For larger arguments, Du's sieve:
     Phi(x) = x * (x + 1) // 2 - sum_{d=2}^x Phi(floor(x / d))
   evaluates Phi(x) using hyperbolic quotient grouping in O(x^(2/3)) time.
   Evaluating g(5 * 10^8) completes in ~0.85 seconds.
"""

import math
import unittest
import numpy as np
from util.utils import timeit


class Problem512:
    def __init__(self, n: int = 500_000_000, sieve_limit: int = 3_500_000):
        self.n = n
        self.sieve_limit = min(n, sieve_limit)
        self.phi_pref = self._build_phi_prefix(self.sieve_limit)
        self.memo: dict[int, int] = {}

    @staticmethod
    def _build_phi_prefix(limit: int) -> np.ndarray:
        phi = np.arange(limit + 1, dtype=np.int64)
        is_prime = np.ones(limit + 1, dtype=bool)
        is_prime[:2] = False
        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                is_prime[i * i::i] = False
        for p in np.nonzero(is_prime)[0]:
            phi[p::p] -= phi[p::p] // p
        return np.cumsum(phi)

    def get_phi(self, x: int) -> int:
        if x <= self.sieve_limit:
            return int(self.phi_pref[x])
        if x in self.memo:
            return self.memo[x]

        total = x * (x + 1) // 2
        sx = math.isqrt(x)
        max_d = x // (sx + 1)
        q = np.arange(1, sx + 1, dtype=np.int64)
        counts = x // q - x // (q + 1)
        s2 = int(np.dot(counts, self.phi_pref[q]))

        d_thresh = x // self.sieve_limit
        s1 = 0
        for d in range(2, min(max_d + 1, d_thresh + 1)):
            s1 += self.get_phi(x // d)

        if max_d > d_thresh:
            d_arr = np.arange(max(2, d_thresh + 1), max_d + 1, dtype=np.int64)
            s1 += int(np.sum(self.phi_pref[x // d_arr]))

        res = total - s1 - s2
        self.memo[x] = res
        return res

    def compute_g(self, n: int) -> int:
        ans = 0
        curr = n
        while curr > 0:
            ans += self.get_phi(curr) - 2 * self.get_phi(curr // 2)
            curr //= 2
        return ans

    @timeit
    def solve(self) -> int:
        return self.compute_g(self.n)


class Solution512(unittest.TestCase):
    def setUp(self):
        self.problem = Problem512()

    def test_sample(self):
        self.assertEqual(2007, self.problem.compute_g(100))

    def test_solution(self):
        self.assertEqual(50660591862310323, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
