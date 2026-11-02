"""
PROBLEM

We define an S-number to be a natural number, n, that is a perfect square and its square root can be
obtained by splitting the decimal representation of n into 2 or more numbers then adding the numbers.

For example, 81 is an S-number because sqrt(81) = 8 + 1.
6724 is an S-number: sqrt(6724) = 6 + 72 + 4.
8281 is an S-number: sqrt(8281) = 8 + 2 + 81 = 82 + 8 + 1.
9801 is an S-number: sqrt(9801) = 98 + 0 + 1.

Further we define T(N) to be the sum of all S numbers n <= N. You are given T(10^4) = 41333.

Find T(10^12).

ANSWER: 128088830547982
Solve time: ~10.0 seconds

---
MATHEMATICAL DERIVATION:

1. Search Space Reduction:
   Since n <= N = 10^12 is a perfect square, we iterate over its square root s = sqrt(n).
   For N = 10^12, 2 <= s <= 10^6. Thus n = s^2 and s has at most 6 digits.

2. Modulo 9 Filter:
   Let d_1, d_2, ..., d_k be a valid split of the decimal representation of n.
   Because any decimal partition of an integer preserves its sum modulo 9:
     n = sum_{i=1}^k d_i mod 9.
   Since the partition sums to s, we have:
     n = s mod 9.
   Substituting n = s^2:
     s^2 = s mod 9  ==>  s(s - 1) = 0 mod 9.
   Since gcd(s, s - 1) = 1, 9 must divide either s or s - 1:
     s = 0 mod 9  or  s = 1 mod 9.
   This single modular constraint eliminates 7/9 (~77.8%) of all candidates, leaving only ~222,222
   values of s to test up to 10^6.

3. Recursive Suffix Splitting with Branch-and-Bound:
   For each candidate s:
   - To ensure at least 2 parts, the first split cannot take the entire number.
   - For subproblems checking if `num` can be split into parts summing to `target`:
       if num < target: return False
       if num == target: return True
       for d in (10, 100, 1000, ...):
         r = num % d
         if r > target: break  # Because larger powers of 10 yield larger remainders
         if can_split(num // d, target - r): return True
   - Pruning stops branches almost immediately, evaluating the entire search space in ~10 seconds
     in pure Python.
"""

import math
import unittest
from util.utils import timeit

POW10 = (
    10,
    100,
    1000,
    10_000,
    100_000,
    1_000_000,
    10_000_000,
    100_000_000,
    1_000_000_000,
    10_000_000_000,
    100_000_000_000,
)


class Problem719:
    def __init__(self, limit: int = 10**12):
        self.limit = limit

    @staticmethod
    def _can_split(num: int, target: int) -> bool:
        if num < target:
            return False
        if num == target:
            return True
        for d in POW10:
            if d > num:
                break
            r = num % d
            if r > target:
                break
            if Problem719._can_split(num // d, target - r):
                return True
        return False

    @staticmethod
    def is_s_number(s: int) -> bool:
        num = s * s
        for d in POW10:
            if d > num:
                break
            r = num % d
            if r > s:
                break
            if Problem719._can_split(num // d, s - r):
                return True
        return False

    def compute_T(self, limit: int) -> int:
        limit_s = math.isqrt(limit)
        total = 0
        for s in range(2, limit_s + 1):
            rem = s % 9
            if rem != 0 and rem != 1:
                continue
            if self.is_s_number(s):
                total += s * s
        return total

    @timeit
    def solve(self) -> int:
        return self.compute_T(self.limit)


class Solution719(unittest.TestCase):
    def setUp(self):
        self.problem = Problem719()

    def test_sample(self):
        self.assertTrue(self.problem.is_s_number(9))      # 81
        self.assertTrue(self.problem.is_s_number(82))     # 6724
        self.assertTrue(self.problem.is_s_number(91))     # 8281
        self.assertTrue(self.problem.is_s_number(99))     # 9801
        self.assertEqual(41333, self.problem.compute_T(10**4))

    def test_solution(self):
        self.assertEqual(128088830547982, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
