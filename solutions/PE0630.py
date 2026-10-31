"""
PROBLEM

Given a set, L, of unique lines, let M(L) be the number of lines in the set and let S(L) be the
sum over every line of the number of times that line is crossed by another line in the set.

For example, two sets of three lines are shown:
In both cases M(L) is 3 and S(L) is 6: each of the three lines is crossed by two other lines.
Note that even if the lines cross at a single point, all of the separate crossings of lines are counted.

Consider points (T_{2k-1}, T_{2k}), for integer k >= 1, generated in the following way:
  S_0 = 290797
  S_{n+1} = S_n^2 mod 50515093
  T_n = (S_n mod 2000) - 1000

For example, the first three points are: (527, 144), (-488, 732), (-454, -947).
Given the first n points generated in this manner, let L_n be the set of unique lines that can be
formed by joining each point with every other point, the lines being extended indefinitely in both
directions. We can then define M(L_n) and S(L_n) as described above.

For example, M(L_3) = 3 and S(L_3) = 6. Also M(L_100) = 4948 and S(L_100) = 24477690.

Find S(L_2500).

ANSWER: 9669182880384
Solve time: ~8.3 seconds

---
MATHEMATICAL DERIVATION:

1. Intersection Criteria for Lines:
   Two lines in the 2D plane intersect at a unique point if and only if they are not parallel.
   Two lines are parallel if and only if they have the identical reduced slope (dx, dy).
   Overlapping identical lines are represented uniquely in the set L.

2. Crossing Count S(L):
   Let M be the total number of unique lines in L.
   Group lines by their slope direction into equivalence classes C_1, C_2, ..., C_k, where |C_i| = c_i.
   Any line in class C_i is parallel to exactly c_i - 1 other lines in the set.
   Therefore, it crosses every line not in its class, which is M - c_i lines.
   Summing across all lines:
     S(L) = sum_{i=1}^k c_i * (M - c_i) = M * sum_{i=1}^k c_i - sum_{i=1}^k c_i^2
          = M^2 - sum_{i=1}^k c_i^2 = 2 * sum_{1 <= i < j <= k} c_i * c_j.

3. Canonical Line Representation:
   For any two distinct points (x1, y1) and (x2, y2):
     dx = x2 - x1, dy = y2 - y1.
     g = gcd(dx, dy), dx //= g, dy //= g.
     Standardize direction so dx > 0 or (dx == 0 and dy > 0).
   The line equation is: dy * x - dx * y = c, where c = dy * x1 - dx * y1.
   A line is uniquely identified by the triple (dx, dy, c), and its slope is the pair (dx, dy).
   We map each slope (dx, dy) to a set of distinct intercept values c.
"""

from collections import defaultdict
import math
from typing import List, Tuple
import unittest
from util.utils import timeit


class Problem630:
    def __init__(self, n_points: int = 2500):
        self.n_points = n_points

    @staticmethod
    def generate_points(n: int) -> List[Tuple[int, int]]:
        s = 290797
        mod = 50515093
        points = []
        for _ in range(n):
            s = (s * s) % mod
            t1 = (s % 2000) - 1000
            s = (s * s) % mod
            t2 = (s % 2000) - 1000
            points.append((t1, t2))
        return points

    def compute_MS(self, n: int) -> Tuple[int, int]:
        points = self.generate_points(n)
        slopes = defaultdict(set)
        gcd = math.gcd

        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                dx = x2 - x1
                dy = y2 - y1
                g = gcd(dx, dy)
                dx //= g
                dy //= g
                if dx < 0 or (dx == 0 and dy < 0):
                    dx = -dx
                    dy = -dy
                c = dy * x1 - dx * y1
                slopes[(dx, dy)].add(c)

        counts = [len(intercepts) for intercepts in slopes.values()]
        m = sum(counts)
        s_l = sum(c * (m - c) for c in counts)
        return m, s_l

    @timeit
    def solve(self) -> int:
        _, s_l = self.compute_MS(self.n_points)
        return s_l


class Solution630(unittest.TestCase):
    def setUp(self):
        self.problem = Problem630()

    def test_sample(self):
        m3, s3 = self.problem.compute_MS(3)
        self.assertEqual(3, m3)
        self.assertEqual(6, s3)

        m100, s100 = self.problem.compute_MS(100)
        self.assertEqual(4948, m100)
        self.assertEqual(24477690, s100)

    def test_solution(self):
        self.assertEqual(9669182880384, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
