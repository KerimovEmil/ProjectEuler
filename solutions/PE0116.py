"""
A row of five grey square tiles is to have a number of its tiles replaced with coloured oblong tiles chosen from
 red (length two), green (length three), or blue (length four).

How many different ways can the grey tiles in a row measuring fifty units in length be replaced if colours cannot be
 mixed and at least one coloured tile must be used?

ANSWER: 20492570929
Solve time: ~0.001 seconds
"""

from util.utils import timeit, combin
import unittest


class Problem116:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        n = self.n

        red = 0
        for i in range(1, n // 2 + 1):
            red += combin(n - i, n - 2 * i)

        green = 0
        for i in range(1, n // 3 + 1):
            green += combin(n - 2 * i, n - 3 * i)

        blue = 0
        for i in range(1, n // 4 + 1):
            blue += combin(n - 3 * i, n - 4 * i)

        return red + blue + green


class Solution116(unittest.TestCase):
    def setUp(self):
        self.problem = Problem116(n=50)

    def test_solution(self):
        self.assertEqual(20492570929, self.problem.solve())

    def test_small_solution(self):
        problem = Problem116(n=5)
        self.assertEqual(12, problem.solve())


if __name__ == '__main__':
    unittest.main()
