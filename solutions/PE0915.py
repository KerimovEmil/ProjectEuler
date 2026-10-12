"""
PROBLEM

The function s(n) is defined recursively for positive integers by
s(1) = 1 and s(n + 1) = (s(n) - 1)^3 + 2 for n >= 1.
The sequence begins: s(1) = 1, s(2) = 2, s(3) = 3, s(4) = 10, ...

For positive integers N, define
  T(N) = sum_{a=1}^N sum_{b=1}^N gcd(s(s(a)), s(s(b))).
You are given T(3) = 12, T(4) = 24881925 and T(100) = 14416749 both modulo 123456789.

Find T(10^8). Give your answer modulo 123456789.

ANSWER: 55601924
Solve time: ~0.45 seconds

---
MATHEMATICAL & ALGEBRAIC DERIVATION:

1. Strong Divisibility Property of s(n):
   Consider the polynomial f(x) = (x - 1)^3 + 2 in Z[x].
   Extending the sequence to n = 0 by setting s(0) = 0, we observe that:
     f(s(0)) = f(0) = (0 - 1)^3 + 2 = 1 = s(1),
   so s(n) = f^(n)(0) is the n-th iterate of 0 under the integer polynomial f(x).
   For any polynomial f(x) in Z[x], u === v (mod d) implies f(u) === f(v) (mod d).
   Specifically, for any k >= 0 and m >= 0, since s(k) === 0 (mod s(k)):
     s(k + m) = f^(m)(s(k)) === f^(m)(0) = s(m) (mod s(k)).
   Therefore:
     gcd(s(k + m), s(k)) = gcd(s(m), s(k)).
   By the Euclidean algorithm on the indices (A, B), it follows immediately that:
     gcd(s(A), s(B)) = s(gcd(A, B))   for all A, B >= 1.

2. Nested Application to gcd(s(s(a)), s(s(b))):
   Applying the strong divisibility identity twice:
     gcd(s(s(a)), s(s(b))) = s(gcd(s(a), s(b))) = s(s(gcd(a, b))).

3. Double Cycle Reduction Modulo M = 123456789:
   Let A(g) = s(s(g)) mod M.
   - Iterating x -> ((x - 1)^3 + 2) mod M from s(1) = 1 enters a cycle at index mu_1 = 54 with period
     lambda_1 = 33,705. Thus, for any n >= 54, s(n) mod M depends only on (n - 54) mod 33,705.
   - Next, iterating x -> ((x - 1)^3 + 2) mod 33,705 from s(1) = 1 enters a cycle at index mu_2 = 3 with period
     lambda_2 = 420.
   - Since s(g) >= s(5) = 731 >= 54 for all g >= 5, and g >= 3, the sequence A(g) = s(s(g)) mod M is strictly
     periodic with period lambda_2 = 420 for all g >= 5!
   This allows O(1) evaluation of prefix sums P_A(x) = sum_{g=1}^x A(g) mod M for any x.

4. Sublinear Summation via Totient Summatory Function:
   Grouping pairs (a, b) in {1, ..., N}^2 by g = gcd(a, b):
     T(N) = sum_{g=1}^N A(g) * (2 * Phi(floor(N / g)) - 1) (mod M),
   where Phi(m) = sum_{k=1}^m phi(k).
   Using quotient grouping over floor(N / g) (2 * sqrt(N) = 20,000 intervals) together with O(N^(2/3)) evaluation
   of Phi(m) computes T(10^8) in ~0.45 seconds.
"""

from itertools import accumulate
import math
import unittest
from util.utils import timeit


class Problem915:
    MOD = 123456789

    def __init__(self, sieve_limit: int = 250000):
        self.mu1, self.lam1, self.seq1 = self._find_cycle(self.MOD)
        self.mu2, self.lam2, self.seq2 = self._find_cycle(self.lam1)

        s_exact = [0, 1, 2, 3, 10, 731]
        self.p_small = [0] * 5
        for g in range(1, 5):
            val = self._s_mod1(s_exact[g])
            self.p_small[g] = (self.p_small[g - 1] + val) % self.MOD

        self.cycle_p = [0] * (self.lam2 + 1)
        for i in range(self.lam2):
            val = self._eval_a_ge5(5 + i)
            self.cycle_p[i + 1] = (self.cycle_p[i] + val) % self.MOD
        self.cycle_sum = self.cycle_p[self.lam2]

        self.sieve_limit = sieve_limit
        phi = list(range(sieve_limit + 1))
        for i in range(2, sieve_limit + 1):
            if phi[i] == i:
                phi[i::i] = [x - x // i for x in phi[i::i]]
        self.phi_prefix = [x % self.MOD for x in accumulate(phi)]
        self.memo_phi: dict[int, int] = {}

    @staticmethod
    def _find_cycle(mod: int) -> tuple[int, int, list[int]]:
        seen: dict[int, int] = {}
        x = 1
        n = 1
        seq = [0]
        while x not in seen:
            seen[x] = n
            seq.append(x)
            x = ((x - 1) ** 3 + 2) % mod
            n += 1
        mu = seen[x]
        lam = n - mu
        return mu, lam, seq

    def _s_mod1(self, n: int) -> int:
        if n < self.mu1:
            return self.seq1[n]
        return self.seq1[self.mu1 + (n - self.mu1) % self.lam1]

    def _eval_a_ge5(self, g: int) -> int:
        rem = self.seq2[g] if g < self.mu2 else self.seq2[self.mu2 + (g - self.mu2) % self.lam2]
        idx = self.mu1 + (rem - self.mu1) % self.lam1
        return self.seq1[idx]

    def sum_a(self, x: int) -> int:
        if x <= 4:
            return self.p_small[x]
        q, r = divmod(x - 4, self.lam2)
        return (self.p_small[4] + q * self.cycle_sum + self.cycle_p[r]) % self.MOD

    def get_phi_sum(self, m: int) -> int:
        if m <= self.sieve_limit:
            return self.phi_prefix[m]
        if m in self.memo_phi:
            return self.memo_phi[m]

        res = m * (m + 1) // 2
        s = math.isqrt(m)
        for d in range(2, s + 1):
            q = m // d
            res -= self.phi_prefix[q] if q <= self.sieve_limit else self.get_phi_sum(q)
        max_q = m // (s + 1)
        for q in range(1, max_q + 1):
            res -= (m // q - m // (q + 1)) * self.phi_prefix[q]

        res %= self.MOD
        self.memo_phi[m] = res
        return res

    def compute_t(self, n: int) -> int:
        total = 0
        l = 1
        while l <= n:
            q = n // l
            r = n // q
            coprime_pairs = (2 * self.get_phi_sum(q) - 1) % self.MOD
            sum_a_interval = (self.sum_a(r) - self.sum_a(l - 1)) % self.MOD
            total = (total + sum_a_interval * coprime_pairs) % self.MOD
            l = r + 1
        return total

    @timeit
    def solve(self) -> int:
        return self.compute_t(10**8)


class Solution915(unittest.TestCase):
    def setUp(self):
        self.problem = Problem915()

    def test_sample(self):
        self.assertEqual(12, self.problem.compute_t(3))
        self.assertEqual(24881925, self.problem.compute_t(4))
        self.assertEqual(14416749, self.problem.compute_t(100))

    def test_solution(self):
        self.assertEqual(55601924, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
