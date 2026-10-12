"""
PROBLEM

Let g(n) be a sequence defined as follows:
g(4) = 13,
g(n) = g(n-1) + gcd(n, g(n-1)) for n > 4.

The first few values are:
n:    4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20 ...
g(n): 13  14  16  17  18  27  28  29  30  31  32  33  34  51  54  55  60 ...

You are given that g(1,000) = 2524 and g(1,000,000) = 2624152.

Find g(10^15).

ANSWER: 2744233049300770
Solve time: ~0.06 seconds

---
MATHEMATICAL DERIVATION:

1. Constant Offset Along Unit-GCD Intervals:
   Suppose we are at index n with value g(n). For subsequent steps m > n, as long as gcd(k, g(k-1)) = 1 for all
   n < k < m, the sequence increments by 1 at each step:
   g(m - 1) = g(n) + (m - 1 - n) = m + (g(n) - n - 1).

2. Next Non-Trivial GCD Jump via Prime Factorization:
   Using the property gcd(a, b) = gcd(a, b - a), the GCD at step m is:
   gcd(m, g(m - 1)) = gcd(m, m + g(n) - n - 1) = gcd(m, g(n) - n - 1).
   Let Delta = g(n) - n - 1. Then gcd(m, g(m - 1)) > 1 if and only if m shares a prime factor p with Delta.
   For any prime factor p | Delta, the smallest multiple of p strictly greater than n is:
   m_p = (floor(n / p) + 1) * p.
   Therefore, the very next index m > n where gcd(m, g(m - 1)) > 1 is:
   m_next = min_{p | Delta} ((floor(n / p) + 1) * p).

3. Fast Factorization with Miller-Rabin and Pollard's Brent-Rho:
   At each jump (such as when g(n) = 3n and Delta = 2n - 1), n roughly doubles within a small number of steps,
   requiring only 590 jumps to reach N = 10^15. Factoring Delta <= 3 * 10^15 at each jump using deterministic
   64-bit Miller-Rabin and Pollard's Brent-Rho completes the entire calculation in ~0.06 seconds.
"""

import math
import unittest
from util.utils import timeit


class Problem443:
    SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

    def __init__(self):
        pass

    @classmethod
    def is_prime(cls, n: int) -> bool:
        if n < 2:
            return False
        for p in cls.SMALL_PRIMES:
            if n == p:
                return True
            if n % p == 0:
                return False
        d = n - 1
        s = (d & -d).bit_length() - 1
        d >>= s
        for a in cls.MR_BASES:
            if a % n == 0:
                continue
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True

    @classmethod
    def pollard_rho(cls, n: int) -> int:
        if n % 2 == 0:
            return 2
        if cls.is_prime(n):
            return n
        for c in range(1, 100):
            y = 2
            m = 128
            g = 1
            r = 1
            q = 1
            ys = 2
            x = 2
            while g == 1:
                x = y
                for _ in range(r):
                    y = (y * y + c) % n
                k = 0
                while k < r and g == 1:
                    ys = y
                    for _ in range(min(m, r - k)):
                        y = (y * y + c) % n
                        q = (q * abs(x - y)) % n
                    g = math.gcd(q, n)
                    k += m
                r <<= 1
            if g == n:
                g = 1
                while g == 1:
                    ys = (ys * ys + c) % n
                    g = math.gcd(abs(x - ys), n)
            if g < n:
                return g
        return n

    @classmethod
    def prime_factors(cls, n: int) -> list[int]:
        factors = set()
        for p in cls.SMALL_PRIMES:
            if n % p == 0:
                factors.add(p)
                while n % p == 0:
                    n //= p
        stack = [n] if n > 1 else []
        while stack:
            curr = stack.pop()
            if curr <= 1:
                continue
            if cls.is_prime(curr):
                factors.add(curr)
            else:
                d = cls.pollard_rho(curr)
                stack.append(d)
                stack.append(curr // d)
        return list(factors)

    def compute_g(self, target_n: int) -> int:
        n = 4
        g = 13
        while n < target_n:
            delta = g - n - 1
            if delta <= 1:
                n += 1
                g += math.gcd(n, g)
                continue
            p_factors = self.prime_factors(delta)
            next_n = min((n // p + 1) * p for p in p_factors)
            if next_n > target_n:
                g += target_n - n
                break
            g += (next_n - 1) - n
            n = next_n
            g += math.gcd(n, g)
        return g

    @timeit
    def solve(self) -> int:
        return self.compute_g(10**15)


class Solution443(unittest.TestCase):
    def setUp(self):
        self.problem = Problem443()

    def test_sample(self):
        self.assertEqual(13, self.problem.compute_g(4))
        self.assertEqual(27, self.problem.compute_g(9))
        self.assertEqual(51, self.problem.compute_g(17))
        self.assertEqual(60, self.problem.compute_g(20))
        self.assertEqual(2524, self.problem.compute_g(1000))
        self.assertEqual(2624152, self.problem.compute_g(10**6))

    def test_solution(self):
        self.assertEqual(2744233049300770, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
