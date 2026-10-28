"""
PROBLEM

We shall define a square lamina to be a square outline with a square "hole" so that the shape possesses
vertical and horizontal symmetry.

Given eight tiles it is possible to form a lamina in only one way: 3x3 square with a 1x1 hole in the middle.
However, using thirty-two tiles it is possible to form two distinct laminae.

If t represents the number of tiles used, we shall say that t = 8 is type L(1) and t = 32 is type L(2).

Let N(n) be the number of t <= 1000000 such that t is type L(n); for example, N(15) = 832.

What is sum_{n=1}^{10} N(n)?

ANSWER: 209566
Solve time: ~0.04 seconds

---
MATHEMATICAL DERIVATION:

1. Factorizations of Reduced Tile Count:
   Every symmetric square lamina with outer side a and inner hole side b has border thickness k = (a - b) / 2 >= 1
   and uses:
     t = a^2 - b^2 = 4 * k * (k + b)   tiles,   where k >= 1 and b >= 1.
   Setting u = t / 4 <= floor(1,000,000 / 4) = 250,000, the number of distinct laminae formed by exactly t tiles
   equals the number of factorizations u = k * m with 1 <= k < m (where m = k + b >= k + 1).

2. Harmonic Sieve over u = t / 4:
   For U = floor(T_max / 4) = 250,000, we maintain an array `ways[1..U]` initialized to 0.
   For each k >= 1 with k * (k + 1) <= U, we increment `ways[u]` for every multiple u in
   {k(k + 1), k(k + 2), ..., floor(U / k) * k}.
   The total number of inner-loop operations is bounded by U * sum_{k=1}^{sqrt(U)} 1/k = O(U log U),
   and N(n) is simply the count of indices u in [1, U] with `ways[u] == n`.
"""

import math
import unittest
from util.utils import timeit


class Problem174:
    def __init__(self, max_tiles: int = 1_000_000):
        self.max_tiles = max_tiles
        self._ways: list[int] | None = None

    def _get_ways(self) -> list[int]:
        if self._ways is not None:
            return self._ways
        u_max = self.max_tiles // 4
        ways = [0] * (u_max + 1)
        for k in range(1, math.isqrt(u_max) + 1):
            for u in range(k * (k + 1), u_max + 1, k):
                ways[u] += 1
        self._ways = ways
        return ways

    def count_type(self, n: int) -> int:
        return sum(1 for w in self._get_ways() if w == n)

    def sum_types(self, min_n: int = 1, max_n: int = 10) -> int:
        return sum(1 for w in self._get_ways() if min_n <= w <= max_n)

    @timeit
    def solve(self) -> int:
        return self.sum_types(1, 10)


class Solution174(unittest.TestCase):
    def setUp(self):
        self.problem = Problem174()

    def test_sample(self):
        self.assertEqual(832, self.problem.count_type(15))

    def test_solution(self):
        self.assertEqual(209566, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
