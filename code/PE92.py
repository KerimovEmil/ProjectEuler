"""
PROBLEM

A number chain is created by continuously adding the square of the digits in a number to form a new
number until it has been seen before.

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop.
What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
How many starting numbers below ten million will arrive at 89?

ANSWER:
8581146
Solve time ~70 seconds
"""

import functools
from util.utils import timeit
import unittest


@functools.lru_cache(maxsize=None, typed=False)
def eightynine(d):  # TODO: this is very slow, need to speed up
    if d == 89:
        return True
    elif d == 1:
        return False
    else:
        return eightynine(sum(int(c) ** 2 for c in str(d)))


class Problem92:
    def __init__(self, n):
        self.n = n
        self.count = 0

    @timeit
    def solve(self):
        for i in range(1, self.n):
            self.count += eightynine(i)
        return self.count


class Solution92(unittest.TestCase):
    def setUp(self):
        self.problem = Problem92(int(1e7))

    def test_solution(self):
        self.assertEqual(8581146, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
