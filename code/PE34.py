"""
PROBLEM

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.

ANSWER:
40730
Solve time ~7.3  seconds
"""

# https://en.wikipedia.org/wiki/Factorion
# only four such numbers exist: 1,2, 145, 40585.
# since 1 and 2 are not sums as the question stated then the answer is 145+40585 = 40730

from util.utils import timeit
import unittest

factorials_0_to_9 = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]


class Problem34:
    def __init__(self, max_x):
        self.max_x = max_x
        self.sum = 0

    @staticmethod
    def sum_of_factorial_of_digits(number):
        """Sum of the factorial of digits"""
        return sum([factorials_0_to_9[int(i)] for i in str(number)])

    @timeit
    def solve(self):
        for i in range(3, self.max_x):  # to not consider 1 and 2 as solutions
            if Problem34.sum_of_factorial_of_digits(i) == i:
                self.sum += i
        return self.sum


class Solution34(unittest.TestCase):
    def setUp(self):
        # upper bound is 7 x 9!, because all 8-digit numbers (10,000,000 to 99,999,999) are greater than the maximum
        # possible result of any 8-digit number
        # since 9! = 362880, 7*9! = 2540160
        self.problem = Problem34(max_x=2540160)

    def test_solution(self):
        self.assertEqual(40730, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
