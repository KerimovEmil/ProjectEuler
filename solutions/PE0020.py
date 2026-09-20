"""
PROBLEM

n! means n x (n - 1) x ... x 3 x 2 x 1

For example, 10! = 10 x 9 x ... x 3 x 2 x 1 = 3628800,
and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.

Find the sum of the digits in the number 100!

ANSWER: 648
Solve time: ~0.0001 seconds
"""

import unittest
from util.utils import timeit, basic_factorial


class Problem20:
    def __init__(self, n):
        self.n = n
        self.factorial = basic_factorial(n)

    @timeit
    def solve(self):
        return sum(int(d) for d in str(self.factorial))


class Solution20(unittest.TestCase):
    def setUp(self):
        self.problem = Problem20(100)

    def test_solution(self):
        self.assertEqual(648, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
