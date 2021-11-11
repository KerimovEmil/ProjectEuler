"""
PROBLEM

Find the minimal path sum, in matrix.txt (right click and "Save Link/Target As..."),
a 31K text file containing a 80 by 80 matrix, from the left column to the right column.

ANSWER:
260324
Solve time ~2.2 seconds
Related problems: 81
"""

import copy
import os
import unittest
from util.utils import timeit


class Problem82:
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
        a = self.problem_data
        B = self.working_matrix
        n = len(self.problem_data)

        for j in range(n - 1):  # loop over n-1 cols
            col = n - 2 - j  # dynamic programming
            # Loop over all rows
            for i in range(n):
                row = i

                # right
                m = B[row][col + 1]

                for loop_row in range(n):
                    s = B[loop_row][col + 1]

                    if loop_row > row:  # upper
                        for sum_row in range(row + 1, loop_row + 1):
                            s += a[sum_row][col]
                    elif loop_row < row:  # lower
                        for sum_row in range(loop_row, row):
                            s += a[sum_row][col]

                    m = min(m, s)

                B[row][col] += m

        return min([x[0] for x in B])


class Solution81(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p082_matrix.txt')
        self.problem = Problem82(file_path)

    def test_solution(self):
        self.assertEqual(260324, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
