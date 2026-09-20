"""
PROBLEM

Find the minimal path sum, in matrix.txt (right click and "Save Link/Target As..."),
a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by only moving right and down.

ANSWER: 427337
Solve time: ~0.012 seconds
Related problems: 82, 83
"""

import copy
import os
import unittest
from util.utils import timeit


class Problem81:
    def __init__(self, data_path):
        self.problem_data = self.load_data(data_path)
        self.working_matrix = copy.deepcopy(self.problem_data)

    @staticmethod
    def load_data(data_path):
        with open(data_path, 'r') as f:
            problem_data = [[int(n) for n in s.split(',')] for s in f.readlines()]
        return problem_data

    @timeit
    def solve(self):
        B = self.working_matrix
        n = len(self.working_matrix)

        # Calculate the right side and bottom side
        for i in range(n):
            B[n - 1][n - 2 - i] += B[n - 1][n - 2 - i + 1]
            B[n - 2 - i][n - 1] += B[n - 2 - i + 1][n - 1]

        # All other numbers
        for i in range(n - 1):
            for j in range(n - 1):
                B[n - 2 - i][n - 2 - j] += min(B[n - 1 - i][n - 2 - j], B[n - 2 - i][n - 1 - j])

        return B[0][0]


class Solution81(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p081_matrix.txt')
        self.problem = Problem81(file_path)

    def test_solution(self):
        self.assertEqual(427337, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
