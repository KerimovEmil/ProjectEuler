"""
PROBLEM

It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a
different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.

ANSWER: 142857
Solve time: ~0.140 seconds
"""

import unittest
from util.utils import timeit


class Problem52:
    def __init__(self):
        pass

    @staticmethod
    def is_permuted(n):
        digits = set(str(n))
        for multiplier in range(2, 7):
            if set(str(multiplier * n)) != digits:
                return False
        return True

    @timeit
    def solve(self):
        x = 1
        while True:
            if self.is_permuted(x):
                return x
            x += 1


class Solution52(unittest.TestCase):
    def setUp(self):
        self.problem = Problem52()

    def test_solution(self):
        self.assertEqual(142857, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
