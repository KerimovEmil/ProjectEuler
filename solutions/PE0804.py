r"""
PROBLEM

Let g(n) denote the number of ways a positive integer n can be represented in the form:
    x^2 + xy + 41y^2
where x and y are integers.

For example, g(53) = 4 due to:
    (-4)^2 + (-4)(1) + 41(1)^2 = 53
    (-3)^2 + (-3)(-1) + 41(-1)^2 = 53
    (3)^2 + (3)(1) + 41(1)^2 = 53
    (4)^2 + (4)(-1) + 41(-1)^2 = 53

Define T(N) as:
    T(N) = \sum_{n=1}^N g(n)

You are given:
    T(10^3) = 474
    T(10^6) = 492128

Find T(10^16).

ANSWER: 4921370551019052
Solve time: ~2.8 seconds

---
MATHEMATICAL DERIVATION:

1. Completing the Square:
   The binary quadratic form is:
     Q(x, y) = x^2 + xy + 41y^2.
   Multiplying by 4:
     4 Q(x, y) = (2x + y)^2 + 163y^2.

2. Variable Substitution:
   Let u = 2x + y.
   Since u == y (mod 2), any integer pair (u, y) with the same parity uniquely determines
   an integer x = (u - y) / 2.
   The condition 1 <= Q(x, y) <= N is equivalent to:
     1 <= u^2 + 163y^2 <= 4N   subject to   u == y (mod 2).
   The condition Q(x, y) >= 1 simply excludes the origin (u, y) = (0, 0).

3. Counting Lattice Points:
   For a given y:
     u^2 <= 4N - 163y^2 ==> |u| <= floor(sqrt(4N - 163y^2)) =: u_max.
   The number of valid integers u in [-u_max, u_max] with u == y (mod 2) is:
     - If y is even: u in {0, +-2, +-4, ...} ==> 2 * floor(u_max / 2) + 1
     - If y is odd:  u in {+-1, +-3, ...}     ==> 2 * floor((u_max + 1) / 2)

   Both cases can be expressed compactly:
     count(u) = u_max + 1 if (u_max % 2 == y % 2) else u_max.

   By symmetry between y and -y, we sum count(u) over positive y up to y_max = floor(sqrt(4N / 163)),
   multiply by 2, and add the count for y = 0:
     y = 0 ==> u is even, u != 0, |u| <= floor(sqrt(4N)) ==> 2 * floor(floor(sqrt(4N)) / 2).

4. Complexity:
   For N = 10^16, y_max = floor(sqrt(4 * 10^16 / 163)) = 15,665,208.
   Evaluating the square roots takes ~2.8 seconds in Python.
"""

import math
import unittest

from util.utils import timeit


class Problem804:
    def __init__(self, limit: int = 10**16):
        self.limit = limit

    def compute_T(self, n: int) -> int:
        four_n = 4 * n
        max_y = math.isqrt(four_n // 163)
        isqrt = math.isqrt

        ans_pos_y = 0
        for y in range(1, max_y + 1):
            u = isqrt(four_n - 163 * y * y)
            ans_pos_y += (u + 1) if (u & 1) == (y & 1) else u

        ans = 2 * ans_pos_y + 2 * (isqrt(four_n) // 2)
        return ans

    @timeit
    def solve(self) -> int:
        return self.compute_T(self.limit)


class Solution804(unittest.TestCase):
    def setUp(self):
        self.problem = Problem804()

    def test_samples(self):
        self.assertEqual(474, self.problem.compute_T(10**3))
        self.assertEqual(492128, self.problem.compute_T(10**6))

    def test_solution(self):
        self.assertEqual(4921370551019052, self.problem.solve())


if __name__ == "__main__":
    unittest.main()
