"""
PROBLEM

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
a^2 + b^2 = c^2

For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.

ANSWER: 31875000
Solve time: ~0.006 seconds
"""

import unittest
from util.utils import timeit


class Problem9:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        for a in range(1, 999):
            for b in range(a + 1, 999):
                c = 1000 - a - b
                if a ** 2 + b ** 2 == c ** 2:
                    return a * b * c


class Solution9(unittest.TestCase):
    def setUp(self):
        self.problem = Problem9()

    def test_solution(self):
        self.assertEqual(31875000, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
