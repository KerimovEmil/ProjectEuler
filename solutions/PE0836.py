"""
PROBLEM

Let A be an affine plane over a radically integral local field F with residual characteristic p.

We consider an open oriented line section U of A with normalized Haar measure m.

Define f(m, p) as the maximal possible discriminant of the jacobian associated to the orthogonal
kernel embedding of U into A.

Find f(20230401, 57). Give as your answer the concatenation of the first letters of each bolded
word.

ANSWER: aprilfoolsjoke
Solve time: ~0.0 seconds
"""

import unittest
from util.utils import timeit


class Problem836:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        return "aprilfoolsjoke"


class Solution836(unittest.TestCase):
    def setUp(self):
        self.problem = Problem836()

    def test_solution(self):
        self.assertEqual("aprilfoolsjoke", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
