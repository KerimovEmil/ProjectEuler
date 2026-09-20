"""
PROBLEM

Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more
interesting is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of
8/13 ~ 62%.

If one complete new layer is added to the spiral with the above side length of 9, will this fraction of
primes along both diagonals continue to fall below 10%?

What is the side length of the square spiral for which the ratio of primes along both diagonals first
falls below 10%?

ANSWER: 26241
Solve time: ~0.358 seconds
"""

import unittest
from util.utils import timeit


class Problem58:
    def __init__(self, ratio):
        self.ratio = ratio
        self.bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    @staticmethod
    def _power(x, y, mod):
        result = 1
        x %= mod
        while y:
            if y & 1:
                result = (result * x) % mod
            x = (x * x) % mod
            y >>= 1
        return result

    def is_prime(self, n):
        if n < 2:
            return False
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if n % p == 0:
                return n == p

        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1

        for a in self.bases:
            x = self._power(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True

    @timeit
    def solve(self):
        prime_count = 0
        layer = 0
        while True:
            layer += 1
            side = 2 * layer + 1
            squared = side * side
            offsets = (2, 4, 6)
            corners = (squared,) + tuple(squared - i * layer for i in offsets)
            for corner in corners:
                if self.is_prime(corner):
                    prime_count += 1

            total = 4 * layer + 1
            if prime_count / total < self.ratio:
                return side


class Solution58(unittest.TestCase):
    def setUp(self):
        self.problem = Problem58(ratio=0.1)

    def test_solution(self):
        self.assertEqual(26241, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
