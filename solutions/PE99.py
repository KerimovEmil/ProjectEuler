"""
PROBLEM

Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file containing
one thousand lines with a base/exponent pair on each line,
determine which line number has the greatest numerical value.

NOTE: The first two lines in the file represent the numbers in the example given above.

ANSWER: 709
Solve time ~0.006 seconds
"""


import math
import os
import unittest
from util.utils import timeit


class Problem99:
    def __init__(self, data_path):
        self.problem_data = []
        self.load_data(data_path)
        self.max_num = 0

    def load_data(self, data_path):
        with open(data_path) as input_file:
            for line in input_file:
                self.problem_data.append(line.strip().split(','))

    @timeit
    def solve(self):
        max_i = None
        for i, line in enumerate(self.problem_data):
            num = int(line[1]) * math.log(int(line[0]))
            if num > self.max_num:
                max_i = i + 1
                self.max_num = num

        return max_i


class Solution99(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p099_base_exp.txt')
        self.problem = Problem99(file_path)

    def test_solution(self):
        self.assertEqual(709, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
