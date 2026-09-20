"""
PROBLEM

The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.
Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.
(Please note that the palindromic number, in either base, may not include leading zeros.)

ANSWER: 872187
Solve time: ~0.216 seconds
"""

import unittest
from util.utils import timeit


def is_palindromic(input_string):
    """Return True if input string is a palindromic"""
    return input_string == input_string[::-1]


class Problem36:
    def __init__(self, max_value):
        self.max_value = max_value
        self.sum = 0

    @timeit
    def solve(self):
        for i in range(self.max_value):
            if is_palindromic(str(i)):
                if is_palindromic(bin(i)[2:]):
                    self.sum += i
        return self.sum


class Solution36(unittest.TestCase):
    def setUp(self):
        self.problem = Problem36(int(1e6))

    def test_solution(self):
        self.assertEqual(872187, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
