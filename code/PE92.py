"""
PROBLEM

A number chain is created by continuously adding the square of the digits in a number to form a new
number until it has been seen before.

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop.
What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
How many starting numbers below ten million will arrive at 89?

ANSWER:
8581146
Solve time ~20 seconds
"""

import functools
from util.utils import timeit
import unittest
import time  # temp debugging

# define s(n) to be the sum of the square of the digits of n
# hence if n = sum_{i=0}^{r} d_i 10^i  then s(n) = sum_{i=0}^{r} d_i^2
# note that if r >= 3 then n > s(n):
# Proof:
# since d_i < 10 for all i, for r >=3
# d_0 + d_r * 10^r >= 1000 >= 162 = 9^2 + 9^2 >= d_0^2 + d_r^2
# hence each new digit added still implies that n > s(n) if there are at least 3 digits (i.e. [1, 999]


# pre-compute squares of strings
dc_dig_square = {str(i): i**2 for i in range(10)}


@functools.lru_cache(maxsize=None, typed=False)
def eighty_nine(d):
    if d == 89:
        return True
    elif d == 1:
        return False
    else:
        return eighty_nine(sum(dc_dig_square[c] for c in str(d)))


class Problem92:
    def __init__(self, n):
        self.n = n
        self.count = 0

    @timeit
    def solve(self):
        # compute all of the sum of squares
        ls_sum_sqr = [sum(dc_dig_square[c] for c in str(d)) for d in range(1, self.n)]  # 18 seconds

        self.count += sum([eighty_nine(i) for i in ls_sum_sqr])  # 2.3 seconds

        return self.count


class Solution92(unittest.TestCase):
    def setUp(self):
        self.problem = Problem92(int(1e7))

    def test_solution(self):
        self.assertEqual(8581146, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
