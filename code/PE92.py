"""
PROBLEM

A number chain is created by continuously adding the square of the digits in a number to form a new
number until it has been seen before.

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop.
What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
How many starting numbers below ten million will arrive at 89?

ANSWER:
8581146
Solve time ~58 seconds
"""

import functools
from util.utils import timeit
import unittest

# define s(n) to be the sum of the square of the digits of n
# hence if n = sum_{i=0}^{r} d_i 10^i  then s(n) = sum_{i=0}^{r} d_i^2
# note that if r >= 3 then n > s(n):
# Proof:
# since d_i < 10 for all i, for r >=3
# d_0 + d_r * 10^r >= 1000 >= 162 = 9^2 + 9^2 >= d_0^2 + d_r^2
# hence each new digit added still implies that n > s(n) if there are at least 3 digits (i.e. [1, 999]


@functools.lru_cache(maxsize=None, typed=False)
def eighty_nine(d):  # TODO: this is very slow, need to speed up. The slowest part is taking all of the sum of squares
    print(d)
    if d == 89:
        return True
    elif d == 1:
        return False
    else:
        return eighty_nine(sum(int(c) ** 2 for c in str(d)))


class Problem92:
    def __init__(self, n):
        self.n = n
        self.count = 0

    @staticmethod
    def _eighty_nine_no_cache(d):
        return eighty_nine(sum(int(c) ** 2 for c in str(d)))

    @timeit
    def solve(self):
        cut_off = 1000
        # cut_off = self.n
        self.count += sum([eighty_nine(i) for i in range(1, cut_off)])
        # for i in range(1, cut_off):
        #     # print("----------")
        #     self.count += eighty_nine(i)

        self.count += sum([self._eighty_nine_no_cache(i) for i in range(cut_off, self.n)])
        # for i in range(cut_off, self.n):
        #     # print("----------")
        #     self.count += self._eighty_nine_no_cache(i)

        return self.count


class Solution92(unittest.TestCase):
    def setUp(self):
        self.problem = Problem92(int(1e7))

    def test_solution(self):
        self.assertEqual(8581146, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
