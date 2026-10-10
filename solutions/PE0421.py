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
Solve time: ~31 seconds

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

3. Structure of the Roots:
   Since x = -1 (i.e. p - 1) is always a root, all d solutions mod p are given by:
     r_k = (-1 * w^k) mod p  for k = 0, 1, ..., d - 1,
   where w is a primitive d-th root of unity modulo p.
   A primitive d-th root of unity can be found efficiently by computing w = g^((p-1)/d) mod p
   for small trial generators g >= 2.
   - If d = 1: the unique root is r = p - 1.
   - If d = 3: w has order 3 (w != 1 mod p).
   - If d = 5: w has order 5 (w != 1 mod p).
   - If d = 15: w has order 15 (w^3 != 1 and w^5 != 1 mod p).

4. Counting Multiples in [1, N]:
   For each root r in {1, ..., p - 1}, the number of n in [1, N] with n = r (mod p) is:
     count(r, p, N) = (N - r) // p + 1.

5. Optimization:
   - Sieve primes up to M = 10^8 using an odd-only boolean array in ~0.25 seconds.
   - Group primes by d = gcd(15, p - 1) = gcd(15, (p - 1) % 15):
     * d = 1: primes with (p - 1) % 15 in {1, 2, 4, 7, 13} (and p = 2).
       The single root is always p - 1. This entire subset (~2.16 million primes) is vectorized
       with NumPy in ~0.15 seconds.
     * d = 3, 5, 15: iterated with minimal small-g exponentiation, directly accumulating contributions.
   Total run time is ~31 seconds.
"""

import unittest
import numpy as np
from util.utils import timeit


class Problem421:
    def __init__(self):
        pass

    @staticmethod
    def _primes_up_to(n: int) -> np.ndarray:
        """Return all primes up to n as a NumPy array of int64."""
        if n < 2:
            return np.empty(0, dtype=np.int64)
        size = (n - 1) // 2 + 1
        sieve = np.ones(size, dtype=bool)
        sieve[0] = False
        limit = int(int(n**0.5 - 1) / 2) + 1
        for i in range(1, limit):
            if sieve[i]:
                p = 2 * i + 1
                start = 2 * i * (i + 1)
                sieve[start::p] = False
        primes = np.empty(np.count_nonzero(sieve) + 1, dtype=np.int64)
        primes[0] = 2
        primes[1:] = 2 * np.nonzero(sieve)[0] + 1
        return primes

    def compute(self, n_limit: int, prime_limit: int) -> int:
        primes = self._primes_up_to(prime_limit)
        p_mod = (primes - 1) % 15

        # d = 1: gcd(15, p - 1) == 1
        # Roots are always unique: r = p - 1
        mask1 = np.isin(p_mod, [1, 2, 4, 7, 13])
        p1 = primes[mask1]
        total = int(np.sum(p1 * ((n_limit - (p1 - 1)) // p1 + 1)))

        # d = 3: gcd(15, p - 1) == 3
        p3 = primes[np.isin(p_mod, [3, 6, 12])]
        tot3 = 0
        for p in p3:
            p = int(p)
            exp = (p - 1) // 3
            g = 2
            while True:
                w = pow(g, exp, p)
                if w != 1:
                    break
                g += 1
            r1 = p - 1
            r2 = (r1 * w) % p
            r3 = (r2 * w) % p
            tot3 += p * (((n_limit - r1) // p + 1) + ((n_limit - r2) // p + 1) + ((n_limit - r3) // p + 1))
        total += tot3

        # d = 5: gcd(15, p - 1) == 5
        p5 = primes[p_mod == 10]
        tot5 = 0
        for p in p5:
            p = int(p)
            exp = (p - 1) // 5
            g = 2
            while True:
                w = pow(g, exp, p)
                if w != 1:
                    break
                g += 1
            cur = p - 1
            cnt = 0
            for _ in range(5):
                cnt += (n_limit - cur) // p + 1
                cur = (cur * w) % p
            tot5 += p * cnt
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
                if pow(w, 3, p) != 1 and pow(w, 5, p) != 1:
                    break
                g += 1
            cur = p - 1
            cnt = 0
            for _ in range(15):
                cnt += (n_limit - cur) // p + 1
                cur = (cur * w) % p
            tot15 += p * cnt
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
