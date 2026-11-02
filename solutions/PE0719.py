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
Solve time: ~7.0 seconds

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
   values of s to test up to 10^6. We generate these directly (s = 9k and s = 9k + 1) without checking
   modulo 9 on every integer.

3. Recursive Suffix Partitioning with Monotonic and Zero-Duplicate Pruning:
   - For subproblems checking if `num` can be partitioned to sum to `target`:
       if num < target: return False
       if num == target: return True
   - Monotonic bound: As d in (10, 100, 1000, ...) increases, r = num % d is non-decreasing.
     If r >= target, any larger power of 10 will produce an even larger remainder >= target,
     so we return False immediately without testing larger powers of 10.
   - Zero-Duplicate Elimination: If num % 10^(k+1) == num % 10^k, the (k+1)-th digit is 0.
     Taking that 0 yields the exact same remainder value and reduces the quotient, a state space
     already covered by the branch that took the zero digit in the previous cut. Skipping
     identical remainders eliminates millions of duplicate recursive calls.
   - For s >= 2, s^2 > s, so can_split(s * s, s) is guaranteed to make at least one partition cut
     (producing >= 2 parts), allowing a unified, direct recursive search.
"""

import math
import unittest
from util.utils import timeit


def can_split(num: int, target: int) -> bool:
    """Recursively checks whether `num` can be partitioned into parts summing to `target`."""
    if num < target:
        return False
    if num == target:
        return True

    r = num % 10
    if r >= target:
        return False
    if can_split(num // 10, target - r):
        return True

    r2 = num % 100
    if r2 >= target:
        return False
    if r2 != r and can_split(num // 100, target - r2):
        return True

    r3 = num % 1000
    if r3 >= target:
        return False
    if r3 != r2 and can_split(num // 1000, target - r3):
        return True

    r4 = num % 10000
    if r4 >= target:
        return False
    if r4 != r3 and can_split(num // 10000, target - r4):
        return True

    r5 = num % 100000
    if r5 >= target:
        return False
    if r5 != r4 and can_split(num // 100000, target - r5):
        return True

    r6 = num % 1000000
    if r6 >= target:
        return False
    return r6 != r5 and can_split(num // 1000000, target - r6)


class Problem719:
    def __init__(self, limit: int = 10**12):
        self.limit = limit

    @staticmethod
    def is_s_number(s: int) -> bool:
        """Checks if s^2 is an S-number with square root s."""
        if s < 2:
            return False
        rem = s % 9
        if rem != 0 and rem != 1:
            return False
        return can_split(s * s, s)

    def compute_T(self, limit: int) -> int:
        limit_s = math.isqrt(limit)
        total = 0
        max_k = limit_s // 9
        for k in range(1, max_k + 1):
            s = 9 * k
            if can_split(s * s, s):
                total += s * s
            s = 9 * k + 1
            if s <= limit_s and can_split(s * s, s):
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
