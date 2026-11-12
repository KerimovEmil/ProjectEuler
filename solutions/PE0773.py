r"""
PROBLEM

Let S_k be the set containing 2, 5, and the first k primes that end in 7.
For example, S_3 = {2, 5, 7, 17, 37}.

Define an S_k-Ruff number to be a positive integer that is not divisible by any element in S_k.

Let M_k be the product of all the numbers in S_k.
Define F(k) to be the sum of all S_k-Ruff numbers less than M_k that have a last digit of 7.

You are given:
  F(3) = 76101452

Find F(97), and give your answer modulo 1,000,000,007.

ANSWER: 556206950
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Reduction:
   Let p_1, ..., p_k be the first k primes ending in 7, and P = prod_{i=1}^k p_i.
   Then M_k = 10 P.
   Any integer x ending in 7 (i.e. x == 7 mod 10) is automatically coprime to 2 and 5.
   Thus x is not divisible by any element in S_k if and only if gcd(x, P) == 1.
   We seek:
     F(k) = sum_{0 < x < 10P, x == 7 (mod 10), gcd(x, P) == 1} x.

2. Inclusion-Exclusion via Mobius Inversion:
   Using sum_{d | gcd(x, P)} mu(d) = [gcd(x, P) == 1]:
     F(k) = sum_{d | P} mu(d) * sum_{0 < x < 10P, x == 7 (mod 10), d | x} x.

3. Chinese Remainder Theorem:
   For any squarefree divisor d | P, all prime factors of d end in 7, so gcd(d, 10) == 1.
   Since d == 7^omega(d) (mod 10), the inverse modulo 10 is d^(-1) == 3^omega(d) (mod 10).
   The system x == 0 (mod d) and x == 7 (mod 10) has a unique solution modulo 10d:
     r_d = q * d, where q = (7 * 3^omega(d)) mod 10 in {1, 3, 7, 9}.
   The multiples of d ending in 7 in the range (0, 10P) are:
     x = r_d + 10d * j   for j = 0, 1, ..., L - 1, where L = P / d.
   Summing this arithmetic progression:
     sum_{j=0}^{L-1} (r_d + 10d * j) = L * r_d + 10d * L * (L - 1) / 2
                                     = (P / d) * (q * d) + 5P * (L - 1)
                                     = P * q + 5P * (P / d - 1)
                                     = P * (q - 5) + 5P^2 / d.

4. Closed-form Summation:
   Summing over all divisors d | P:
     F(k) = 5P^2 * sum_{d | P} (mu(d) / d) + P * sum_{d | P} mu(d) * (q(omega(d)) - 5).

   - First term:
       5P^2 * (phi(P) / P) = 5P * prod_{i=1}^k (p_i - 1).

   - Second term:
       Notice that mu(d) * (q(omega(d)) - 5) depends solely on m = omega(d):
         c(m) = (-1)^m * (q(m) - 5).
       Evaluating c(m) for m mod 4:
         m = 0: (+1) * (7 - 5) = 2
         m = 1: (-1) * (1 - 5) = 4
         m = 2: (+1) * (3 - 5) = -2
         m = 3: (-1) * (9 - 5) = -4
       Thus c(m) is 4-periodic: [2, 4, -2, -4].
       The second term is:
         P * sum_{m=0}^k C(k, m) * c(m mod 4).

   Both terms evaluate in O(k) time modulo 1,000,000,007!
"""

import math
import unittest

from util.utils import timeit


def get_first_k_primes_ending_in_7(k: int) -> list[int]:
    """Generates the first k primes whose decimal representation ends in 7."""
    primes = []
    x = 7
    while len(primes) < k:
        if x % 10 == 7:
            if all(x % d != 0 for d in range(3, math.isqrt(x) + 1, 2)):
                primes.append(x)
        x += 2
    return primes


class Problem773:
    def __init__(self, k: int = 97, mod: int = 1000000007):
        self.k = k
        self.mod = mod

    def compute_F(self, k: int, mod: int | None = None) -> int:
        if mod is None:
            mod = self.mod
        primes = get_first_k_primes_ending_in_7(k)

        p_prod = 1
        phi_prod = 1
        for p in primes:
            p_prod = (p_prod * (p % mod)) % mod
            phi_prod = (phi_prod * ((p - 1) % mod)) % mod

        term1 = (5 * p_prod * phi_prod) % mod

        # c(m) = (-1)^m (q(m) - 5) mod 4 pattern: [2, 4, -2, -4]
        c = [2, 4, -2, -4]
        binom = 1
        term2_inner = 0
        for m in range(k + 1):
            term2_inner = (term2_inner + binom * c[m % 4]) % mod
            binom = (binom * (k - m) * pow(m + 1, -1, mod)) % mod

        term2 = (p_prod * term2_inner) % mod
        return (term1 + term2) % mod

    @timeit
    def solve(self) -> int:
        return self.compute_F(self.k, self.mod)


class Solution773(unittest.TestCase):
    def setUp(self):
        self.problem = Problem773()

    def test_samples(self):
        self.assertEqual(76101452, self.problem.compute_F(3))

    def test_solution(self):
        self.assertEqual(556206950, self.problem.solve())


if __name__ == "__main__":
    unittest.main()
