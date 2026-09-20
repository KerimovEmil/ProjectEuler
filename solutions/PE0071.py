"""
PROBLEM

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a
reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d <= 1,000,000 in ascending order of size, find the
numerator of the fraction immediately to the left of 3/7.

ANSWER: 428570
Solve time: ~0.283 seconds
"""

import unittest
from util.utils import timeit


class Problem71:
    def __init__(self, limit):
        self.limit = limit
        self.ans = None

    @timeit
    def solve(self):
        best_numerator = 0
        best_denominator = 1

        for denominator in range(2, self.limit + 1):
            numerator = (3 * denominator - 1) // 7
            if numerator * 7 < 3 * denominator:
                if numerator * best_denominator > best_numerator * denominator:
                    best_numerator = numerator
                    best_denominator = denominator

        self.ans = best_numerator
        return self.ans

    def get_solution(self):
        return self.ans


class Solution71(unittest.TestCase):
    def setUp(self):
        self.problem = Problem71(limit=1000000)

    def test_solution(self):
        self.assertEqual(428570, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
