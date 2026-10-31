"""
PROBLEM

Two positive integers a and b are 2-friendly when gcd(a, b) = 2^t, t > 0.
For example, 24 and 40 are 2-friendly because gcd(24, 40) = 8 = 2^3 while 24 and 36 are not
because gcd(24, 36) = 12 = 2^2 * 3 is not a power of 2.

Let f(n) be the number of pairs, (p, q), of positive integers with 1 <= p < q <= n
such that p and q are 2-friendly.
You are given f(10^2) = 1031 and f(10^6) = 321418433 modulo 1 000 000 007.

Find f(10^11) modulo 1 000 000 007.

ANSWER: 968274154
Solve time: ~2.4 seconds

---
MATHEMATICAL DERIVATION:

1. Reformulation in terms of Coprime Pairs:
   We seek the number of pairs 1 <= p < q <= n such that gcd(p, q) = 2^t for some integer t >= 1.
   For any fixed power of 2, d = 2^t, we can write:
     p = d * x,   q = d * y
   where 1 <= x < y <= floor(n / d) and gcd(x, y) = 1.

   The number of coprime pairs (x, y) with 1 <= x < y <= M is:
     sum_{y=2}^M phi(y) = (sum_{y=1}^M phi(y)) - phi(1) = Phi(M) - 1,
   where Phi(M) = sum_{k=1}^M phi(k) is the totient summatory function.

2. Summing Over All Powers of 2:
   Since the gcd values 2^1, 2^2, 2^3, ... are mutually disjoint:
     f(n) = sum_{t=1}^{floor(log_2(n))} ( Phi(floor(n / 2^t)) - 1 ).

   Thus, computing f(n) reduces directly to evaluating Phi(m) for values of m of the form floor(n / 2^t).

3. Sublinear Evaluation of Totient Summatory Function (Du's Sieve):
   By Dirichlet hyperbola convolution on phi * 1 = id:
     Phi(m) = m * (m + 1) // 2 - sum_{d=2}^m Phi(floor(m / d)).

   To evaluate this efficiently for m <= 5 * 10^10:
   - Precompute phi(k) and prefix sums Phi(k) up to L = 5,000,000 using a linear sieve and NumPy.
   - For larger m, partition the sum into two ranges:
       (a) d <= m // (isqrt(m) + 1): evaluated recursively (or via precomputed sieve when floor(m / d) <= L).
       (b) q = floor(m / d) <= isqrt(m): vectorized dot product with counts floor(m / q) - floor(m / (q + 1)).
   - Memoize recursive calls to Phi(m).
"""

import math
import unittest
import numpy as np
from util.utils import timeit


class Problem643:
    def __init__(self, n: int = 100_000_000_000, mod: int = 1_000_000_007, sieve_limit: int = 5_000_000):
        self.n = n
        self.mod = mod
        self.sieve_limit = min(n // 2, sieve_limit)
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

    def compute_f(self, n: int) -> int:
        ans = 0
        curr = n // 2
        while curr > 0:
            ans = (ans + self.get_phi(curr) - 1) % self.mod
            curr //= 2
        return ans

    @timeit
    def solve(self) -> int:
        return self.compute_f(self.n)


class Solution643(unittest.TestCase):
    def setUp(self):
        self.problem = Problem643()

    def test_sample(self):
        self.assertEqual(1031, self.problem.compute_f(100))
        self.assertEqual(321418433, self.problem.compute_f(1_000_000))

    def test_solution(self):
        self.assertEqual(968274154, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
