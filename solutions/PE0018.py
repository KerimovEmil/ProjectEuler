"""
PROBLEM

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from
top to bottom is 23.

Find the maximum total from top to bottom of the triangle in p018_triangle.txt

ANSWER: 1074
Solve time: ~0.001 seconds
Related Problems: 67
"""

import unittest
from util.utils import timeit
import os


class Problem18:
    def __init__(self, data):
        self.data = data

    def reduce_triangle(self):
        """
        This method replaces the last row of the triangle with the sum of that row and the maximum of the left
        and right paths. This replacement happens for each row of the triangle starting from the bottom until only one
        number is left.
        """
        for i in range(len(self.data[-1]) - 1):
            best_path = max(self.data[-1][i], self.data[-1][i + 1])
            self.data[-2][i] += best_path
        del self.data[-1]

    @timeit
    def solve(self):
        for row in range(len(self.data) - 1):
            self.reduce_triangle()

        return self.data[0][0]


class Solution18(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p018_triangle.txt')
        with open(file_path) as f:
            triangle = [[int(n) for n in s.split()] for s in f.readlines()]

        self.problem = Problem18(triangle)

    def test_solution(self):
        self.assertEqual(1074, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
