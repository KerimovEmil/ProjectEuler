"""
PROBLEM

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9.
The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

ANSWER: 233168
Solve time ~ 0.002 seconds
"""

import unittest
from util.utils import timeit


class Problem1:
    def __init__(self, limit):
        self.limit = limit

    @timeit
    def solve(self):
        gen = (i for i in range(1, self.limit) if not (i % 3 and i % 5))
        return sum(gen)


class Solution1(unittest.TestCase):
    def setUp(self):
        self.problem = Problem1(1000)

    def test_solution(self):
        self.assertEqual(233168, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
