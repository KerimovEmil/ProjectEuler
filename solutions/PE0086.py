"""
PROBLEM

A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3, and a fly, F, sits in the
opposite corner. By travelling on the surfaces of the room the shortest "straight line" distance
from S to F is 10 and the path is shown on the diagram.

However, there are up to three "shortest" path candidates for any given cuboid and the shortest
route doesn't always have integer length.

It can be shown that there are exactly 2060 distinct cuboids, ignoring rotations, with integer
dimensions, up to a maximum size of M by M by M, for which the shortest route has integer length
when M = 100. This is the least value of M for which the number of solutions first exceeds two
thousand; the number of solutions when M = 99 is 1975.

Find the least value of M such that the number of solutions first exceeds one million.

ANSWER: 1818
Solve time: ~1.8 seconds
"""

import unittest
from math import isqrt

from util.utils import timeit


class Problem86:
    def __init__(self, limit):
        self.limit = limit

    @staticmethod
    def count_upto(max_m):
        total = 0
        for m in range(1, max_m + 1):
            m2 = m * m
            for s in range(2, 2 * m + 1):
                hyp2 = s * s + m2
                r = isqrt(hyp2)
                if r * r == hyp2:
                    lo = s - m if s - m > 1 else 1
                    hi = s // 2
                    if lo <= hi:
                        total += hi - lo + 1
        return total

    @timeit
    def solve(self):
        total = 0
        m = 0
        while total <= self.limit:
            m += 1
            m2 = m * m
            for s in range(2, 2 * m + 1):
                hyp2 = s * s + m2
                r = isqrt(hyp2)
                if r * r == hyp2:
                    lo = s - m if s - m > 1 else 1
                    hi = s // 2
                    if lo <= hi:
                        total += hi - lo + 1
        return m


class Solution86(unittest.TestCase):
    def setUp(self):
        self.problem = Problem86(limit=1_000_000)

    def test_sample(self):
        self.assertEqual(1975, Problem86.count_upto(99))
        self.assertEqual(2060, Problem86.count_upto(100))

    def test_solution(self):
        self.assertEqual(1818, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
