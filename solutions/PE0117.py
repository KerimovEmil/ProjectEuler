"""
PROBLEM

Using a combination of grey square tiles and oblong tiles chosen from: red tiles (measuring two units), green
tiles (measuring three units), and blue tiles (measuring four units), it is possible to tile a row measuring
five units in length in exactly fifteen different ways.

How many ways can a row measuring fifty units in length be tiled?

NOTE: This is related to Problem 116.

ANSWER: 100808458960497
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Combinatorial Reduction to Tetranacci Numbers:
   Let T(n) denote the number of ways to tile a row of length n using tiles of lengths 1 (grey), 2 (red),
   3 (green), and 4 (blue).
   For any n >= 1, partitioning all valid tilings by the length k in {1, 2, 3, 4} of the last tile placed at the
   right end of the row gives the 4th-order linear homogeneous recurrence:
     T(n) = T(n - 1) + T(n - 2) + T(n - 3) + T(n - 4)   for n >= 4,
   with initial values:
     T(0) = 1  (empty tiling),
     T(1) = 1  ([1]),
     T(2) = 2  ([1,1], [2]),
     T(3) = 4  ([1,1,1], [1,2], [2,1], [3]).

2. Complexity:
   Evaluating the recurrence iteratively up to n = 50 (or via companion matrix exponentiation in O(log n) using
   `LinearHomogeneousRecurrence([1, 1, 1, 1], [4, 2, 1, 1])`) computes T(50) = 100,808,458,960,497 in ~0.0001s.
"""

import unittest
from util.utils import LinearHomogeneousRecurrence, timeit


class Problem117:
    def __init__(self, n: int = 50):
        self.n = n
        self.recurrence = LinearHomogeneousRecurrence([1, 1, 1, 1], [4, 2, 1, 1])

    def count_tilings(self, n: int) -> int:
        return self.recurrence.get(n)

    @timeit
    def solve(self) -> int:
        return self.count_tilings(self.n)


class Solution117(unittest.TestCase):
    def setUp(self):
        self.problem = Problem117()

    def test_sample(self):
        self.assertEqual(15, self.problem.count_tilings(5))

    def test_solution(self):
        self.assertEqual(100808458960497, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
