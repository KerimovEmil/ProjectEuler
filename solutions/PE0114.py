"""
PROBLEM

A row measuring seven units in length has red blocks with a minimum length of three units placed on it, such that
any two red blocks (which are allowed to be different lengths) are separated by at least one grey square. There are
exactly seventeen ways of doing this.

How many ways can a row measuring fifty units in length be filled?

NOTE: Although the example above does not lend itself to the possibility, in general it is permitted to mix block
sizes. For example, on a row measuring eight units in length you could use red (3), grey (1), and red (4).

ANSWER: 16475640049
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Dynamic Programming Recurrence:
   Let F(m, n) denote the number of valid tilings of a row of length n using red blocks of length >= m separated
   by at least one grey square (here m = 3).
   - For 0 <= n < m, no red block can fit, so the only tiling is all grey squares: F(m, n) = 1.
   - For n >= m, consider the rightmost element of the row:
     * Case 1: The last unit is a grey square. The remaining n - 1 units can be tiled in F(m, n - 1) ways.
     * Case 2: The row ends with a red block of length k (m <= k <= n).
       - If k = n, the entire row is a single red block (1 way).
       - If m <= k < n, the red block must be immediately preceded by at least one grey square, leaving n - k - 1
         units that can be tiled in F(m, n - k - 1) ways.
   Combining both cases gives:
     F(m, n) = F(m, n - 1) + 1 + sum_{j=0}^{n - m - 1} F(m, j).

2. Constant-Time Difference Reduction:
   Taking the first difference F(m, n) - F(m, n - 1) for n > m:
     F(m, n) - F(m, n - 1) = F(m, n - 1) - F(m, n - 2) + F(m, n - m - 1),
   which simplifies to the linear recurrence:
     F(m, n) = 2 * F(m, n - 1) - F(m, n - 2) + F(m, n - m - 1)   for n > m,
   with F(m, m) = 2. This evaluates F(3, 50) in O(n) arithmetic operations.
"""

import unittest
from util.utils import timeit


class Problem114:
    def __init__(self, m: int = 3, n: int = 50):
        self.m = m
        self.n = n

    @staticmethod
    def fill_count(m: int, n: int) -> int:
        if n < m:
            return 1
        dp = [1] * (n + 1)
        dp[m] = 2
        for i in range(m + 1, n + 1):
            dp[i] = 2 * dp[i - 1] - dp[i - 2] + dp[i - m - 1]
        return dp[n]

    @timeit
    def solve(self) -> int:
        return self.fill_count(self.m, self.n)


class Solution114(unittest.TestCase):
    def setUp(self):
        self.problem = Problem114()

    def test_sample(self):
        self.assertEqual(17, self.problem.fill_count(3, 7))

    def test_solution(self):
        self.assertEqual(16475640049, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
