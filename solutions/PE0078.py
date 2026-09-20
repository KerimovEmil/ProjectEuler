"""
PROBLEM

Let p(n) represent the number of different ways in which n coins can be separated into piles.
For example, five coins can be separated into piles in exactly seven different ways, so p(5)=7.

OOOOO
OOOO O
OOO OO
OOO O O
OO OO O
OO O O O
O O O O O
Find the least value of n for which p(n) is divisible by one million.

ANSWER: 55374
Solve time: ~11.3 seconds
"""
from util.utils import timeit, partition_number
import unittest


class Problem78:
    def __init__(self):
        pass

    @timeit
    def solve(self, div=1_000_000):
        p = 1
        n = 2
        while p != 0:
            n += 1
            p = partition_number(n, mod=div)
        return n


class Solution78(unittest.TestCase):
    def setUp(self):
        self.problem = Problem78()

    def test_solution(self):
        self.assertEqual(55374, self.problem.solve(div=1_000_000))


if __name__ == '__main__':
    unittest.main()
