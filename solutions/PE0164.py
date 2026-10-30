"""
PROBLEM

How many 20 digit numbers n (without any leading zero) exist such that no three consecutive digits of n
have a sum greater than 9?

ANSWER: 378158756814587
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Dynamic Programming over Last Two Digits:
   Whether a new digit d_k in {0, ..., 9} can be appended to a valid (k - 1)-digit prefix depends only on the
   last two digits (d_{k-2}, d_{k-1}) of the prefix, since the three-digit sum constraint is:
     d_{k-2} + d_{k-1} + d_k <= 9   <=>   0 <= d_k <= 9 - d_{k-2} - d_{k-1}.

2. State Space and Transitions:
   Let DP(k, a, b) be the number of valid k-digit prefixes ending with consecutive digits (a, b), where
   0 <= a, b <= 9 and a + b <= 9.
   - Base case (k = 2):
     Since the leading digit a cannot be 0, DP(2, a, b) = 1 for all 1 <= a <= 9 and 0 <= b <= 9 - a,
     and 0 when a = 0.
   - Transition (from length k - 1 to k, for k = 3, ..., N):
     For each pair (a, b) with a + b <= 9 and each next digit c in {0, ..., 9 - a - b}:
       DP(k, b, c) += DP(k - 1, a, b).
   - Alternatively, noticing that the valid range for c depends only on the sum s = a + b, we can sum
     S(k - 1, b) = sum_{a=0}^{9-b} DP(k - 1, a, b) = DP(k, b, 0), and since c <= 9 - a - b <=> a <= 9 - (b + c),
     DP(k, b, c) depends only on b + c! Specifically:
       DP(k, b, c) = sum_{a=0}^{9 - b - c} DP(k - 1, a, b).
   With only 55 valid pairs (a, b) satisfying a + b <= 9, evaluating up to N = 20 takes ~0.0001 seconds.
"""

import math
import unittest
from util.utils import timeit


class Problem164:
    def __init__(self, num_digits: int = 20, max_sum: int = 9):
        self.num_digits = num_digits
        self.max_sum = max_sum

    @staticmethod
    def count_valid_numbers(num_digits: int, max_sum: int = 9) -> int:
        if num_digits <= 0:
            return 0
        if num_digits == 1:
            return min(9, max_sum)

        dp = [[0] * 10 for _ in range(10)]
        for d1 in range(1, min(9, max_sum) + 1):
            for d2 in range(min(9, max_sum - d1) + 1):
                dp[d1][d2] = 1

        for _ in range(3, num_digits + 1):
            next_dp = [[0] * 10 for _ in range(10)]
            for d1 in range(min(9, max_sum) + 1):
                for d2 in range(min(9, max_sum - d1) + 1):
                    ways = dp[d1][d2]
                    if ways:
                        for d3 in range(min(9, max_sum - d1 - d2) + 1):
                            next_dp[d2][d3] += ways
            dp = next_dp

        return sum(sum(row) for row in dp)

    @timeit
    def solve(self) -> int:
        return self.count_valid_numbers(self.num_digits, self.max_sum)


class Solution164(unittest.TestCase):
    def setUp(self):
        self.problem = Problem164()

    def test_sample(self):
        # For 2 digits: d1 in 1..9, d2 in 0..(9-d1) -> 9 + 8 + ... + 1 = 45
        self.assertEqual(45, self.problem.count_valid_numbers(2))
        # For 3 digits: stars and bars for d1 + d2 + d3 <= 9 with d1 >= 1 is comb(9 - 1 + 3, 3) = comb(11, 3) = 165
        self.assertEqual(math.comb(11, 3), self.problem.count_valid_numbers(3))

    def test_solution(self):
        self.assertEqual(378158756814587, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
