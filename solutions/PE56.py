"""
PROBLEM

A googol (10^100) is a massive number: one followed by one-hundred zeros;
100^100 is almost unimaginably large: one followed by two-hundred zeros.
Despite their size, the sum of the digits in each number is only 1.

Considering natural numbers of the form, a^b, where a, b < 100, what is the maximum digital sum?

ANSWER: 972
Solve time: ~ 0.35 seconds
"""
import unittest
from util.utils import timeit


def sum_digits(n: int) -> int:
    """Returns the sum of the digits of n"""
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


class Problem56:
    def __init__(self, max_value):
        self.max_value = max_value
        self.max_dig_sum = 0

    @timeit
    def solve(self):
        for a in range(1, self.max_value):
            for b in range(1, self.max_value):
                num = a ** b
                dig_sum = sum_digits(num)
                if dig_sum > self.max_dig_sum:
                    self.max_dig_sum = dig_sum
        return self.max_dig_sum


class Solution56(unittest.TestCase):
    def setUp(self):
        self.problem = Problem56(100)

    def test_solution(self):
        self.assertEqual(972, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
