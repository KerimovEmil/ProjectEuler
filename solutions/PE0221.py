"""
PROBLEM

We shall call a positive integer "A" an "Alexandrian integer", if there exist integers a, b, c such that:

A = a * b * c
and
1/A = 1/a + 1/b + 1/c

For example, 630 is an Alexandrian integer (a=5, b=-7, c=-18). In fact, 630 is the
6th Alexandrian integer, the first 6 Alexandrian integers being: 6, 42, 120, 156, 420, and 630.

Find the 150000th Alexandrian integer.

ANSWER: 1884161251122450
Solve time: ~0.95 seconds
"""

import math
import unittest
from util.utils import timeit, tonelli_shanks, primes_upto


# MATHEMATICAL DERIVATION:
#
# 1. Algebraic Transformation:
#    The condition 1/A = 1/a + 1/b + 1/c with A = a*b*c is equivalent to:
#      ab + bc + ca = 1.
#    Since A > 0 and ab + bc + ca = 1, exactly two of a, b, c must be negative.
#    Let a > 0, b = -B < 0, c = -C < 0 where B, C > 0.
#    Then -aB + BC - aC = 1 => BC - a(B + C) = 1.
#    Add a^2 to both sides:
#      (B - a)(C - a) = a^2 + 1.
#
# 2. Divisor Factorization:
#    Setting k = a, let p and q be complementary divisors of k^2 + 1 such that p * q = k^2 + 1 with p <= k.
#    Then B = k + p and C = k + q = k + (k^2 + 1) / p, yielding:
#      A = k * B * C = k * (k + p) * (k + (k^2 + 1) / p).
#
# 3. Sieve of k^2 + 1:
#    The 150,000th Alexandrian integer is ~1.88 * 10^15. Since A >= 2 * k^3, k <= 100,000.
#    We sieve prime factors of k^2 + 1 for k <= max_k (~120,000):
#    - For p = 2: k is odd.
#    - For odd primes p = 1 (mod 4): solve r^2 = -1 (mod p) using tonelli_shanks(-1, p).
#      Then p divides k^2 + 1 for k = r (mod p) and k = p - r (mod p).
#    - Factorize each k^2 + 1, generate all divisors p <= k, collect all Alexandrian integers,
#      sort, and select the n-th element.
#    Total runtime is ~0.95s (down from ~660s).


class Problem221:
    def __init__(self, n: int = 150_000):
        self.n = n

    @timeit
    def solve(self, n: int = None) -> int:
        if n is None:
            n = self.n

        # Upper bound estimation for k:
        # A_n ~ O(n log n), 2 * k^3 <= A_n
        if n <= 10:
            max_k = 50
        elif n <= 1000:
            max_k = 2000
        else:
            max_k = int(1.5 * (n ** 0.5) * 200)
            max_k = max(max_k, 120_000)

        # 1. Sieve primes up to max_k
        primes = [int(p) for p in primes_upto(max_k) if p == 2 or p % 4 == 1]

        # 2. Sieve prime factorization of k^2 + 1
        rem = [k * k + 1 for k in range(max_k + 1)]
        prime_factors = [[] for _ in range(max_k + 1)]

        for k in range(1, max_k + 1, 2):
            cnt = 0
            while rem[k] % 2 == 0:
                rem[k] //= 2
                cnt += 1
            prime_factors[k].append((2, cnt))

        for p in primes:
            if p == 2:
                continue
            r = tonelli_shanks(-1, p)
            if r is None:
                continue
            for root in (r, p - r):
                for k in range(root, max_k + 1, p):
                    if rem[k] % p == 0:
                        cnt = 0
                        while rem[k] % p == 0:
                            rem[k] //= p
                            cnt += 1
                        prime_factors[k].append((p, cnt))

        # Remaining factor > 1 must be prime
        for k in range(1, max_k + 1):
            if rem[k] > 1:
                prime_factors[k].append((rem[k], 1))

        # 3. Generate divisors and Alexandrian integers
        alexandrian = []
        for k in range(1, max_k + 1):
            divs = [1]
            for p, count in prime_factors[k]:
                new_divs = []
                p_pow = 1
                for _ in range(count):
                    p_pow *= p
                    for d in divs:
                        new_divs.append(d * p_pow)
                divs.extend(new_divs)

            n_val = k * k + 1
            for p in divs:
                if p <= k:
                    A = k * (k + p) * (k + n_val // p)
                    alexandrian.append(A)

        alexandrian.sort()
        return alexandrian[n - 1]


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem221()

    def test_small_solution(self):
        self.assertEqual(630, self.problem.solve(n=6))

    def test_solution(self):
        self.assertEqual(1884161251122450, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
