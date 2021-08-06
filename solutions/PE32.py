"""
PROBLEM

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example,
the 5-digit number, 15234, is 1 through 5 pandigital.
The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1
through 9 pandigital.
Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.

ANSWER:
45228
Solve time ~1.8 seconds
"""

import unittest
from util.utils import timeit


class Problem32:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.sum = 0

    @timeit
    def solve(self):
        t = []
        for i in range(1, self.max_x):
            for j in range(1, self.max_y):
                if Problem32.pandigital(i, j):
                    if i * j not in t:
                        t.append(i * j)
                        self.sum += i * j

        return self.sum

    @staticmethod
    def pandigital(a, b):
        """Return True is a*b=c is all pandigital"""
        used_digits = {'0'}
        # check if a is pandigital without using the digit of 0
        used_digits = Problem32.check(a, used_digits)
        if used_digits is not False:
            # check if b is pandigital without using the digits in a
            used_digits = Problem32.check(b, used_digits)
            if used_digits is not False:
                # check if a*b is pandigital without using the digits in a or b
                used_digits = Problem32.check(a * b, used_digits)

        if (used_digits is False) or (len(used_digits) != 10):
            return False
        return True

    @staticmethod
    def check(num, s):
        for i in str(num):
            if i in s:
                return False
            else:
                s.add(i)
        return s


class Solution32(unittest.TestCase):
    def setUp(self):
        self.problem = Problem32(max_x=100, max_y=10000)

    def test_solution(self):
        self.assertEqual(45228, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
