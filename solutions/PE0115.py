"""
PROBLEM

NOTE: This is a more difficult version of Problem 114.

A row measuring n units in length has red blocks with a minimum length of m units placed on it, such that any
two red blocks (which are allowed to be different lengths) are separated by at least one black square.

Let the fill-count function, F(m, n), represent the number of ways that a row can be filled.

For example, F(3, 29) = 673135 and F(3, 30) = 1089155.
That is, for m = 3, it can be seen that n = 30 is the smallest value for which the fill-count function first
exceeds one million.

In the same way, for m = 10, it can be verified that F(10, 56) = 880711 and F(10, 57) = 1148904, so n = 57 is
the least value for which the fill-count function first exceeds one million.

For m = 50, find the least value of n for which the fill-count function first exceeds one million.

ANSWER: 168
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. General Fill-Count Recurrence:
   For a minimum red block length m >= 1 and row length n >= 0:
   - When 0 <= n < m, no red block fits in the row, so F(m, n) = 1 (all black squares).
   - When n = m, either all squares are black or the entire row is one red block of length m, so F(m, m) = 2.
   - When n > m, conditioning on the rightmost tile (either a single black square leaving n - 1 units, or a red
     block of length k in [m, n] preceded by a black square if k < n) yields:
       F(m, n) = F(m, n - 1) + 1 + sum_{j=0}^{n - m - 1} F(m, j).
   Subtracting the equation for n - 1 from the equation for n eliminates the prefix sum:
       F(m, n) = 2 * F(m, n - 1) - F(m, n - 2) + F(m, n - m - 1)   for all n > m.

2. Incremental Search for Threshold Crossing:
   Because F(m, n) is strictly increasing for n >= m, we append terms using the O(1) recurrence step until
   F(m, n) > 1,000,000. For m = 50, this requires only 118 recurrence steps (reaching n = 168 with
   F(50, 168) = 1,053,389).
"""

import unittest
from util.utils import timeit


class Problem115:
    def __init__(self, m: int = 50, threshold: int = 1_000_000):
        self.m = m
        self.threshold = threshold

    @staticmethod
    def fill_count(m: int, n: int) -> int:
        if n < m:
            return 1
        dp = [1] * (n + 1)
        dp[m] = 2
        for i in range(m + 1, n + 1):
            dp[i] = 2 * dp[i - 1] - dp[i - 2] + dp[i - m - 1]
        return dp[n]

    @staticmethod
    def first_exceeding(m: int, threshold: int = 1_000_000) -> int:
        dp = [1] * m + [2]
        n = m
        while dp[n] <= threshold:
            n += 1
            dp.append(2 * dp[n - 1] - dp[n - 2] + dp[n - m - 1])
        return n

    @timeit
    def solve(self) -> int:
        return self.first_exceeding(self.m, self.threshold)


class Solution115(unittest.TestCase):
    def setUp(self):
        self.problem = Problem115()

    def test_sample(self):
        self.assertEqual(673135, self.problem.fill_count(3, 29))
        self.assertEqual(1089155, self.problem.fill_count(3, 30))
        self.assertEqual(30, self.problem.first_exceeding(3, 1_000_000))
        self.assertEqual(880711, self.problem.fill_count(10, 56))
        self.assertEqual(1148904, self.problem.fill_count(10, 57))
        self.assertEqual(57, self.problem.first_exceeding(10, 1_000_000))

    def test_solution(self):
        self.assertEqual(168, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
