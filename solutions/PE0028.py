"""
PROBLEM

Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?

ANSWER: 669171001
Solve time: ~0.001 seconds
"""

import unittest
from util.utils import timeit


class Problem28:
    def __init__(self, size):
        self.size = size

    @timeit
    def solve(self):
        # The four corners of each successive ring are k^2, k^2-(k-1), k^2-2(k-1), k^2-3(k-1)
        total = 1
        for k in range(3, self.size + 1, 2):
            corner_sum = 4 * k * k - 6 * (k - 1)
            total += corner_sum
        return total


class Solution28(unittest.TestCase):
    def setUp(self):
        self.problem = Problem28(1001)

    def test_solution(self):
        self.assertEqual(669171001, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
