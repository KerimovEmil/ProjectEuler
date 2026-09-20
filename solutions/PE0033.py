"""
PROBLEM

The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it
may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing
two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the
denominator.

ANSWER: 100
Solve time: ~0.004 seconds
"""

import unittest
from math import gcd
from util.utils import timeit


class Problem33:
    def __init__(self, limit):
        self.limit = limit
        self.prod_numerator = 1
        self.prod_denominator = 1

    @timeit
    def solve(self):
        for numerator in range(10, self.limit):
            for denominator in range(numerator + 1, self.limit):
                if numerator % 10 == 0 and denominator % 10 == 0:
                    continue

                shared = set(str(numerator)) & set(str(denominator))
                if len(shared) != 1:
                    continue

                digit = shared.pop()
                if (str(numerator).count(digit) > 1
                        or str(denominator).count(digit) > 1):
                    continue

                new_numerator = int(str(numerator).replace(digit, '', 1))
                new_denominator = int(str(denominator).replace(digit, '', 1))
                if new_denominator == 0:
                    continue

                if numerator * new_denominator == denominator * new_numerator:
                    self.prod_numerator *= numerator
                    self.prod_denominator *= denominator

        common = gcd(self.prod_numerator, self.prod_denominator)
        return self.prod_denominator // common


class Solution33(unittest.TestCase):
    def setUp(self):
        self.problem = Problem33(limit=100)

    def test_solution(self):
        self.assertEqual(100, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
