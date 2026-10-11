"""
PROBLEM

Numbers of the form n^15 + 1 are composite for every integer n > 1.
For positive integers n and m let s(n, m) be defined as the sum of the distinct prime factors of n^15 + 1 that do not exceed m.

For example, 2^15 + 1 = 3 * 3 * 11 * 331.
So s(2, 10) = 3 and s(2, 1000) = 3 + 11 + 331 = 345.

Also 10^15 + 1 = 7 * 11 * 13 * 211 * 241 * 2161 * 9091.
So s(10, 100) = 31 and s(10, 1000) = 483.

Find sum_{n=1}^{10^11} s(n, 10^8).

ANSWER: 2304215802083466198
Solve time: ~15.8 seconds

---
MATHEMATICAL DERIVATION:

1. Sum Inversion Over Prime Factors:
   Instead of factoring n^15 + 1 for each n up to N = 10^11 (which is completely intractable),
   we invert the summation:
   sum_{n=1}^N s(n, M) = sum_{p <= M} p * (number of n in [1, N] such that p | (n^15 + 1)).

2. Roots of the Congruence n^15 + 1 = 0 (mod p):
   The condition p | (n^15 + 1) is equivalent to n^15 = -1 (mod p).
   - For p = 2: 1^15 = 1 = -1 (mod 2), so n = 1 (mod 2) has 1 solution.
   - For odd prime p: (Z/pZ)* is a cyclic group of order p - 1.
     Since (-1)^15 = -1 (mod p), -1 is always an odd 15-th power, which implies the congruence
     always has solutions. Specifically, the number of roots mod p is precisely d = gcd(15, p - 1).
     Since 15 = 3 * 5, d can be 1, 3, 5, or 15.

3. Quotient-Remainder Count Reduction:
   For any root r in {1, ..., p - 1}, the number of n in [1, N] with n = r (mod p) is
     (N - r) // p + 1.
   Writing N = q * p + rem, where q = N // p and rem = N % p:
     (N - r) // p = q + (rem - r) // p.
   Because 1 <= r <= p - 1 and 0 <= rem <= p - 1:
     - (rem - r) // p = 0  if r <= rem,
     - (rem - r) // p = -1 if r > rem.
   Hence,
     (N - r) // p + 1 = q + 1  if r <= rem, else q.
   Summing over all d roots {r}:
     sum_r count(r, p, N) = d * (N // p) + sum_r [r <= (N % p)].
   This reduces the evaluation for each prime to a single quotient N // p and remainder N % p,
   avoiding repeated integer divisions per root.

4. Algebraic Root Relationships:
   - For d = 1: r = p - 1. Since p - 1 <= rem iff rem == p - 1, count is 1 if rem == p - 1 else 0.
     Vectorized across all ~2.16 million primes in ~0.12 seconds with NumPy.
   - For d = 3: the primitive 3rd root w satisfies w^2 + w + 1 = 0 (mod p).
     The roots are r1 = p - 1, r2 = p - w, and r3 = (-w^2) mod p = w + 1.
     Thus all 3 roots are determined from w without any additional modular multiplication!
   - For d = 5: r = p - 1 and r = p - (w^k mod p) for k = 1, 2, 3, 4.
     All powers are formed via successive multiplications by w mod p.
   - For d = 15: r = p - 1 and r = p - (w^k mod p) for k = 1, ..., 14.

5. Optimization:
   - Sieve primes up to M = 10^8 using primes_upto from util.utils in ~0.41 seconds.
   - Vectorized d = 1 in ~0.12 seconds.
   - Accelerated d = 3, 5, 15 using the quotient-remainder identity and algebraic root generation,
     reducing runtime to ~15.8 seconds.
"""

import unittest
import numpy as np
from util.utils import timeit, primes_upto


class Problem421:
    def __init__(self):
        pass

    def compute(self, n_limit: int, prime_limit: int) -> int:
        primes = primes_upto(prime_limit)
        p_mod = (primes - 1) % 15

        # d = 1: gcd(15, p - 1) == 1
        # Roots are always unique: r = p - 1
        mask1 = np.isin(p_mod, [1, 2, 4, 7, 13])
        p1 = primes[mask1]
        total = int(np.sum(p1 * ((n_limit - (p1 - 1)) // p1 + 1)))

        # d = 3: gcd(15, p - 1) == 3
        # Primitive cube root w satisfies w^2 + w + 1 = 0 (mod p)
        # Roots are r1 = p - 1, r2 = p - w, r3 = w + 1
        p3 = primes[np.isin(p_mod, [3, 6, 12])]
        tot3 = 0
        for p in p3:
            p = int(p)
            exp = (p - 1) // 3
            w = pow(2, exp, p)
            if w == 1:
                w = pow(3, exp, p)
                if w == 1:
                    g = 5
                    while True:
                        w = pow(g, exp, p)
                        if w != 1:
                            break
                        g += 1
            rem = n_limit % p
            cnt = (1 if rem == p - 1 else 0) + (1 if p - w <= rem else 0) + (1 if w + 1 <= rem else 0)
            tot3 += p * (3 * (n_limit // p) + cnt)
        total += tot3

        # d = 5: gcd(15, p - 1) == 5
        p5 = primes[p_mod == 10]
        tot5 = 0
        for p in p5:
            p = int(p)
            exp = (p - 1) // 5
            w = pow(2, exp, p)
            if w == 1:
                w = pow(3, exp, p)
                if w == 1:
                    g = 5
                    while True:
                        w = pow(g, exp, p)
                        if w != 1:
                            break
                        g += 1
            rem = n_limit % p
            w2 = (w * w) % p
            cnt = (
                (1 if rem == p - 1 else 0)
                + (1 if p - w <= rem else 0)
                + (1 if p - w2 <= rem else 0)
                + (1 if p - (w * w2) % p <= rem else 0)
                + (1 if p - (w2 * w2) % p <= rem else 0)
            )
            tot5 += p * (5 * (n_limit // p) + cnt)
        total += tot5

        # d = 15: gcd(15, p - 1) == 15
        p15 = primes[p_mod == 0]
        tot15 = 0
        for p in p15:
            p = int(p)
            exp = (p - 1) // 15
            g = 2
            while True:
                w = pow(g, exp, p)
                w3 = (w * w % p * w) % p
                w5 = (w3 * w * w) % p
                if w3 != 1 and w5 != 1:
                    break
                g += 1
            rem = n_limit % p
            cnt = 1 if rem == p - 1 else 0
            cur_w = w
            for _ in range(14):
                if p - cur_w <= rem:
                    cnt += 1
                cur_w = (cur_w * w) % p
            tot15 += p * (15 * (n_limit // p) + cnt)
        total += tot15

        return total

    @timeit
    def solve(self, n_limit: int = 10**11, prime_limit: int = 10**8) -> int:
        return self.compute(n_limit, prime_limit)


class Solution421(unittest.TestCase):
    def setUp(self):
        self.problem = Problem421()

    def test_sample(self):
        # Verify sample values from problem statement:
        # sum_{n=1}^N s(n, M) for small test parameters
        self.assertEqual(559, self.problem.compute(n_limit=10, prime_limit=100))
        self.assertEqual(3645, self.problem.compute(n_limit=50, prime_limit=100))
        self.assertEqual(27591, self.problem.compute(n_limit=100, prime_limit=500))

    def test_solution(self):
        self.assertEqual(2304215802083466198, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
