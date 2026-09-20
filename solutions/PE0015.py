"""
PROBLEM

Starting in the top left corner of a 2 x 2 grid, and only being able to move to the right and down, there are
exactly 6 routes to the bottom right corner.

How many such routes are there through a 20 x 20 grid?

ANSWER: 137846528820
Solve time: ~0.005 seconds
"""

import unittest
from util.utils import timeit, combin


class Problem15:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        # number of routes = choose(2n, n)
        return combin(2 * self.n, self.n)


class Solution15(unittest.TestCase):
    def setUp(self):
        self.problem = Problem15(20)

    def test_solution(self):
        self.assertEqual(137846528820, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
