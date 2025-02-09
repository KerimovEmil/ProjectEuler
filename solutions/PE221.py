"""
PROBLEM

We shall call a positive integer A an "Alexandrian integer", if there exist integers a,b,c such that:

A = a*b*c
and
1/A = 1/a + 1/b + 1/c

For example, 630 is an Alexandrian integer (a=5, b=-7, c=-18). In fact, 630 is the
6th Alexandrian integer, the first 6 Alexandrian integers being: 6,42,120,156,420, and 630.

Find the 150000th Alexandrian integer

ANSWER:
Solve time:
"""
from util.utils import timeit, is_int
import unittest


# a*b + b*c + a*c = 1
# (a+b+c)^2 = a^2 + b^2 + c^2 + 2

# if a = b then
# a^2 + 2*a*c = 1
# c = (1-a^2) / (2a)
# (2a+c)^2 = 2*a^2 + c^2 + 2

# wlog let a >= b >= c


class Problem221:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem221(n=150_000)

    def test_small_solution(self):
        self.assertEqual(630, Problem221(n=6).solve())

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

