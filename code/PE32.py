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
Solve time ~2.14 seconds
"""

from util.utils import timeit
import unittest


class Problem32:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.sum = 0

    @timeit
    def solve(self):
        t = []
        for i in range(self.max_x):
            for j in range(self.max_y):
                if Problem32.pandigital(i, j):
                    if i*j not in t:
                        t.append(i * j)
                        self.sum += i * j

        return self.sum

    @staticmethod
    def pandigital(a, b):
        """Return True is a*b=c is all pandigital"""
        x = Problem32.check(a)  # check if a is pandigital
        if x is False:
            return False
        y = Problem32.check(b, x)
        if y is False:
            return False
        z = Problem32.check(a * b, y)
        if z is False:
            return False
        if len(z) == 9:
            return True
        return False

    @staticmethod
    def check(num, a=None):
        s = set() if a is None else a

        for i in str(num):
            if i in s:
                return False
            else:
                if i == '0':
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
