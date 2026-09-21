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
from util.utils import timeit, is_prime


class Problem58:
    def __init__(self, ratio):
        self.ratio = ratio

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
                if is_prime(corner):
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
