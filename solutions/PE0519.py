"""
PROBLEM

An arrangement of coins in one or more rows with the bottom row being a block without gaps and every coin in a
higher row touching exactly two coins in the row below is called a fountain of coins. Let f(n) be the number of
possible fountains with n coins. For 4 coins there are three possible arrangements, so f(4) = 3 while f(10) = 78.

Let T(n) be the number of all possible colourings with three colours for all f(n) different fountains with n coins,
given the condition that no two touching coins have the same colour. For 4 coins, T(4) = 48 and T(10) = 17760.

Find the last 9 digits of T(20000).

ANSWER: 804739330
Solve time: ~0.58 seconds

---
MATHEMATICAL DERIVATION:

1. Coin Fountains as Up-Down Paths / Column Heights:
   A coin fountain with base length k can be uniquely decomposed into k columns along the diagonal coordinate axes.
   Let h_1, h_2, ..., h_k be the heights of the columns (from left to right).
   The structural condition that every coin in row r > 1 rests on two coins in row r - 1 implies:
     h_1 = 1,  and  1 <= h_{i+1} <= h_i + 1   for all 1 <= i < k,
   where the total number of coins is n = sum_{i=1}^k h_i.

2. 3-Coloring Multiplier:
   For any valid fountain, the dual graph of touching coins is a triangulated planar graph (a chordal graph).
   When adding the (i+1)-th column of height h_{i+1} adjacent to column i of height h_i:
   - For any coin at elevation y >= 2, it is adjacent to the coin below it in the same column (elevation y - 1)
     and to a coin in the preceding column, having 2 already-colored neighbors, which forces exactly 3 - 2 = 1
     valid color choice.
   - For the base coin at elevation y = 1:
     * If h_i = 1 or h_{i+1} = 1, it has only 1 adjacent constraint from the preceding column, providing
       3 - 1 = 2 valid color choices.
     * If h_i >= 2 and h_{i+1} >= 2, the triangle of contacts between adjacent columns constrains the base coin,
       leaving only 1 valid color choice.
   Thus, the transition multiplier from height h to height h_next is:
     mult(h, h_next) = 2  if (h == 1 or h_next == 1),  and  1  otherwise.

3. Dynamic Programming with Suffix Sums:
   Let dp[n, h] be the total 3-colored ways to form a fountain of n coins ending with column height h.
   Then:
     dp[n, h_next] = sum_{h >= h_next - 1} dp[n - h_next, h] * mult(h, h_next).
   Maintaining suffix sums suf[m, k] = sum_{j >= k} dp[m, j] mod 10^9 allows each step dp[n, h] to be computed in
   O(1) time.
   Since h <= sqrt(2n), the total complexity to evaluate T(20000) mod 10^9 is O(n^(3/2)) operations (~0.58 seconds).
"""

import math
import unittest
from util.utils import timeit


class Problem519:
    def __init__(self, n: int = 20_000, mod: int = 1_000_000_000):
        self.n = n
        self.mod = mod

    @staticmethod
    def count_colored_fountains(n_max: int, mod: int = 1_000_000_000) -> int:
        if n_max <= 0:
            return 0
        if n_max == 1:
            return 3 % mod

        max_h = math.isqrt(2 * n_max) + 2
        suf = [[0] * (max_h + 2) for _ in range(n_max + 1)]
        suf[1][1] = 3 % mod

        for n in range(2, n_max + 1):
            h_lim = (math.isqrt(8 * n + 1) - 1) // 2
            row_suf = suf[n]
            acc = 0
            for h in range(h_lim, 2, -1):
                acc = (acc + suf[n - h][h - 1]) % mod
                row_suf[h] = acc
            if h_lim >= 2:
                m2 = n - 2
                dp2 = (2 * suf[m2][1] - suf[m2][2]) % mod
                acc = (acc + dp2) % mod
                row_suf[2] = acc
            dp1 = (2 * suf[n - 1][1]) % mod
            row_suf[1] = (acc + dp1) % mod

        return suf[n_max][1]

    @timeit
    def solve(self) -> int:
        return self.count_colored_fountains(self.n, self.mod)


class Solution519(unittest.TestCase):
    def setUp(self):
        self.problem = Problem519()

    def test_sample(self):
        self.assertEqual(48, self.problem.count_colored_fountains(4))
        self.assertEqual(17760, self.problem.count_colored_fountains(10))

    def test_solution(self):
        self.assertEqual(804739330, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
