"""
PROBLEM

The palindromic number 595 is interesting because it can be written as the sum of consecutive squares:
62 + 72 + 82 + 92 + 102 + 112 + 122.

There are exactly eleven palindromes below one-thousand that can be written as consecutive square sums, and the sum of
these palindromes is 4164. Note that 1 = 02 + 12 has not been included as this problem is concerned with the squares
of positive integers.

Find the sum of all the numbers less than 108 that are both palindromic and can be written as the sum of consecutive
squares.

ANSWER: 2906969179
Solve time ~0.99 seconds
"""

import unittest
from util.utils import timeit, is_palindrome


class Problem125:
    """
    Find the sum of all the numbers less than 10^8
    that are both palindromic and can be written as
    the sum of consecutive squares.
    """

    def __init__(self, max_value):
        self.max_value = max_value
        self.sum = 0
        self.ls_consec_sq = []
        self.list_of_is_consec_sq()

    def is_sum_of_consec_sq(self, n):
        return n in self.ls_consec_sq

    @timeit
    def solve(self):
        for i in self.ls_consec_sq:
            if is_palindrome(i):
                self.sum += i
        return self.sum

    def list_of_is_consec_sq(self):
        for n in range(2, int(self.max_value ** 0.5) + 1):
            for a in range(n - 1, 0, -1):
                value = int(n * (n + 1) * (2 * n + 1) / 6 - (a - 1) * a * (2 * a - 1) / 6)
                if value < self.max_value:
                    self.ls_consec_sq.append(value)
                else:
                    break
        self.ls_consec_sq = list(set(self.ls_consec_sq))


class Solution125(unittest.TestCase):
    def setUp(self):
        self.problem = Problem125(max_value=int(1e8))

    def test_solution(self):
        self.assertEqual(2906969179, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
