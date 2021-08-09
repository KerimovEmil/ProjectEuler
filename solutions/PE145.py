"""
PROBLEM

Some positive integers n have the property that the sum [ n + reverse(n) ] consists entirely of odd (decimal) digits.
For instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409, and 904 are
reversible. Leading zeroes are not allowed in either n or reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?

ANSWER:
608720
Solve time ~ 0.003s seconds
"""
import math

import unittest
from util.utils import timeit


class Problem145:
    def __init__(self, n):
        self.n = n
        self.count = 0

    @timeit
    def solve(self):
        """See xiangpeng's comment in https://projecteuler.net/thread=145;page=5"""
        max_dig = int(math.log10(int(self.n)))
        for d in range(1, max_dig + 1):
            if (d % 2) == 0:
                self.count += 20 * int(30 ** (d / 2 - 1))
            elif (d % 4) == 3:
                self.count += 100 * int(500 ** ((d + 1) / 4 - 1))
        return self.count

    @timeit
    def solve_basic(self):  # Solve time ~ 376 seconds
        for i in range(1, self.n, 2):  # every last number should be odd, and times the solution by 2
            if i % 10 == 0:  # removing leading 0's
                continue
            rev_i = int(str(i)[::-1])
            i_sum = i + rev_i
            if all([int(x) % 2 == 1 for x in str(i_sum)]):
                self.count += 2
                # print(i)
        return self.count


class Solution145(unittest.TestCase):
    def test_solution(self):
        self.assertEqual(608720, Problem145(n=int(1e9)).solve())


if __name__ == '__main__':
    unittest.main()
