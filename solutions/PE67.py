"""
PROBLEM

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from
top to bottom is 23.

Find the maximum total from top to bottom of the triangle in p067.txt
(a 15K text file containing a triangle with one-hundred rows.)

ANSWER:
7273
Solve time ~0.007 seconds
Related Problems: 18
"""

import unittest
from solutions.PE18 import Problem18


class Solution67(unittest.TestCase):
    def setUp(self):
        with open(r'../problem_data/p067_triangle.txt') as f:
            triangle = [[int(n) for n in s.split()] for s in f.readlines()]

        self.problem = Problem18(triangle)

    def test_solution(self):
        self.assertEqual(7273, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
