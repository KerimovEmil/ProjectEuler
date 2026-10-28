"""
PROBLEM

We shall define a square lamina to be a square outline with a square "hole" so that the shape possesses
vertical and horizontal symmetry. For example, using exactly thirty-two square tiles we can form two
different square laminae: a 9x9 square with a 7x7 hole, or a 6x6 square with a 2x2 hole.

With one-hundred tiles, and not necessarily using all of the tiles at one time, it is possible to form
forty-one different square laminae.

Using up to one million tiles how many different square laminae can be formed?

ANSWER: 1572729
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Parameterization by Border Thickness and Inner Hole Size:
   Let a square lamina have outer side length a >= 3 and centered inner hole side length b >= 1.
   For the hole to be centered with vertical and horizontal symmetry, the border thickness k = (a - b) / 2
   must be a positive integer (so a = b + 2k with k >= 1, b >= 1).
   The number of tiles t used by the lamina is:
     t = a^2 - b^2 = (b + 2k)^2 - b^2 = 4 * k * (k + b).

2. O(sqrt(N)) Summation over Border Thickness k:
   Given an upper limit N on the number of tiles:
     4 * k * (k + b) <= N   <=>   k * (k + b) <= floor(N / 4).
   Let U = floor(N / 4). Since b >= 1, we must have k * (k + 1) <= U, so 1 <= k <= floor(sqrt(U)).
   For each fixed border thickness k, the number of valid hole sizes b >= 1 is:
     max_b(k) = floor(U / k) - k.
   Summing floor(U / k) - k over all k >= 1 with k * (k + 1) <= U requires at most 500 iterations for N = 10^6.
"""

import math
import unittest
from util.utils import timeit


class Problem173:
    def __init__(self, max_tiles: int = 1_000_000):
        self.max_tiles = max_tiles

    @staticmethod
    def count_laminae(max_tiles: int) -> int:
        u = max_tiles // 4
        total = 0
        k = 1
        while k * (k + 1) <= u:
            total += u // k - k
            k += 1
        return total

    @timeit
    def solve(self) -> int:
        return self.count_laminae(self.max_tiles)


class Solution173(unittest.TestCase):
    def setUp(self):
        self.problem = Problem173()

    def test_sample(self):
        self.assertEqual(41, self.problem.count_laminae(100))
        self.assertEqual(math.isqrt(32 // 4), 2)

    def test_solution(self):
        self.assertEqual(1572729, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
