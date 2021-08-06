"""
PROBLEM

2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000?

ANSWER:
1366
Solve time ~0.003 seconds
"""

import unittest
from util.utils import timeit


class Problem16:
    def __init__(self, base, expo):
        self.base = base
        self.expo = expo

    @timeit
    def solve(self):
        return sum(map(int, str(self.base ** self.expo)))


class Solution16(unittest.TestCase):
    def setUp(self):
        self.problem = Problem16(base=2, expo=1000)

    def test_solution(self):
        self.assertEqual(1366, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
