"""
PROBLEM

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers
is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.

ANSWER: 906609
Solve time: ~ 0.76 seconds
"""

from itertools import product

import unittest
from util.utils import timeit


class Problem4:
    def __init__(self, num_digits):
        self.lower = 10 ** (num_digits - 1) - 1
        self.upper = 10 ** num_digits - 1

    @staticmethod
    def is_palindrome(num):
        return str(num) == str(num)[::-1]

    @timeit
    def solve(self):
        pds = []
        for i, j in product(range(self.lower, self.upper), repeat=2):
            if self.is_palindrome(i * j):
                pds.append(i * j)
        return max(pds)


class Solution4(unittest.TestCase):
    def setUp(self):
        self.problem = Problem4(3)

    def test_solution(self):
        self.assertEqual(906609, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
