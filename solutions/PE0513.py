"""
PROBLEM

ABC is an integral sided triangle with sides a <= b <= c.

m_C is the median connecting C and the midpoint of AB.

F(n) is the number of such triangles with c <= n for which m_C has integral length as well.

F(10) = 3 and F(50) = 165.

Find F(100000).

ANSWER: 2925619196
Solve time: ~7.5 seconds

---
MATHEMATICAL DERIVATION:

1. Apollonius' Median Theorem:
   For triangle ABC with sides a, b, c and median m_C to side c:
     2 * a^2 + 2 * b^2 = c^2 + 4 * m_C^2.
   Since c^2 must be even, c must be even: let c = 2k with 1 <= k <= floor(n / 2).
   Then:
     a^2 + b^2 = 2 * (k^2 + m_C^2).
   Since a^2 + b^2 is even, a and b must have the same parity: a = b mod 2.
   Let u = (a + b) / 2 and t = (b - a) / 2, so that u, t are non-negative integers with:
     a = u - t,  b = u + t  (0 <= t < u).
   Substituting into Apollonius' relation:
     (u - t)^2 + (u + t)^2 = 2 * (u^2 + t^2) = 2 * (k^2 + m_C^2)
     ==> u^2 - k^2 = m_C^2 - t^2.
   Factoring as differences of squares:
     (u - m_C) * (u + m_C) = (k - t) * (k + t).

2. Divisor Product Formulation:
   Let p = k - t and q = k + t. Since 0 <= t < k, 1 <= p <= q and p + q = 2k <= n.
   Also let d = u - m_C and d' = u + m_C.
   Since m_C is a positive integer, 1 <= d < d' and d * d' = p * q.
   To satisfy the strict triangle inequality a + b > c (i.e. 2u > 2k ==> u > k):
     d + d' = 2u > 2k = p + q  ==>  d < p <= q < d'.
   Furthermore, b <= c requires u + t <= 2k:
     (d + d') / 2 + (q - p) / 2 <= p + q  <==>  d + d' <= 3p + q.

3. Coprime Multipliers:
   Setting g = gcd(p, d), write p = r * s, d = r * y with gcd(s, y) = 1.
   Then 1 <= y < s, and since d * d' = p * q:
     (r * y) * d' = (r * s) * q  ==>  y * d' = s * q  ==>  q = x * y,  d' = s * x
   for an integer x >= 1.
   The conditions become:
   - p <= q  <==>  r * s <= x * y
   - d + d' <= 3p + q  <==>  x * (s - y) <= r * (3s - y)
   - p + q <= 2 * floor(n / 2)  <==>  r * s + x * y <= 2 * floor(n / 2)
   - Parity: p = q mod 2 and d = d' mod 2.
     * Case 1: s, y both odd  ==>  r and x have the same parity (r = x mod 2).
     * Case 2: s, y opposite parity  ==>  r and x must both be even (r = 2*r1, x = 2*x1).

4. Vectorized Sieve over s:
   For each s <= floor(n / 2), the coprime y values are extracted via a fast prime-factor sieve on s.
   The range of valid x for each r is a contiguous interval of integers of the required parity,
   which is counted in vectorized O(1) arithmetic operations, achieving ~7.5 seconds for n = 100,000.
"""

import math
import unittest
import numpy as np
from util.utils import timeit


class Problem513:
    def __init__(self, n: int = 100_000):
        self.n = n

    @staticmethod
    def count_triangles(n: int) -> int:
        half_k = n // 2
        two_k = 2 * half_k
        total = 0

        odd_pf: list[list[int]] = [[] for _ in range(half_k + 1)]
        for p in range(3, half_k + 1, 2):
            if not odd_pf[p]:
                for m in range(p, half_k + 1, p):
                    odd_pf[m].append(p)

        # Case 1: s and y both odd, 1 <= y < s <= half_k, gcd(s, y) = 1
        for s in range(3, half_k + 1, 2):
            y_min = max(1, 2 * s - math.isqrt(3 * s * s))
            if (y_min & 1) == 0:
                y_min += 1
            y_max = min(s - 2, (two_k - s) // 3)
            if y_min > y_max:
                continue
            length = (y_max - y_min) // 2 + 1
            mask = np.ones(length, dtype=bool)
            for p in odd_pf[s]:
                rem = y_min % p
                first = y_min if rem == 0 else y_min + (p - rem)
                if (first & 1) == 0:
                    first += p
                if first <= y_max:
                    mask[(first - y_min) // 2::p] = False
            y = (y_min + 2 * np.nonzero(mask)[0]).astype(np.int32)
            if len(y) == 0:
                continue
            diff_sy = s - y
            three_s_minus_y = 3 * s - y
            r_max = min(half_k // s, (two_k - 2 * int(y[0])) // (s + int(y[0])))
            if r_max == 1:
                x_lo = (s + y - 1) // y
                x_hi = np.minimum((two_k - s) // y, three_s_minus_y // diff_sy)
                x_lo += (x_lo & 1) ^ 1
                total += int(np.sum(np.maximum(0, (x_hi - x_lo + 2) >> 1)))
            else:
                r = np.arange(1, r_max + 1, dtype=np.int32)[:, None]
                y_row = y[None, :]
                x_lo = (r * s + y_row - 1) // y_row
                x_hi = np.minimum((two_k - r * s) // y_row, (r * three_s_minus_y[None, :]) // diff_sy[None, :])
                x_lo += (x_lo & 1) ^ (r & 1)
                total += int(np.sum(np.maximum(0, (x_hi - x_lo + 2) >> 1)))

        # Case 2: s and y have opposite parity, r = 2*r1, x = 2*x1
        quarter_k = half_k // 2
        for s in range(2, quarter_k + 1):
            y_min = max(1, 2 * s - math.isqrt(3 * s * s))
            if (y_min & 1) == (s & 1):
                y_min += 1
            y_max = min(s - 1, (half_k - s) // 2)
            if y_min > y_max:
                continue
            length = (y_max - y_min) // 2 + 1
            mask = np.ones(length, dtype=bool)
            for p in odd_pf[s]:
                rem = y_min % p
                first = y_min if rem == 0 else y_min + (p - rem)
                if (first & 1) != (y_min & 1):
                    first += p
                if first <= y_max:
                    mask[(first - y_min) // 2::p] = False
            y = (y_min + 2 * np.nonzero(mask)[0]).astype(np.int32)
            if len(y) == 0:
                continue
            diff_sy = s - y
            three_s_minus_y = 3 * s - y
            r1_max = min(quarter_k // s, (half_k - int(y[0])) // (s + int(y[0])))
            if r1_max == 1:
                x1_lo = (s + y - 1) // y
                x1_hi = np.minimum((half_k - s) // y, three_s_minus_y // diff_sy)
                total += int(np.sum(np.maximum(0, x1_hi - x1_lo + 1)))
            else:
                r1 = np.arange(1, r1_max + 1, dtype=np.int32)[:, None]
                y_row = y[None, :]
                x1_lo = (r1 * s + y_row - 1) // y_row
                x1_hi = np.minimum((half_k - r1 * s) // y_row, (r1 * three_s_minus_y[None, :]) // diff_sy[None, :])
                total += int(np.sum(np.maximum(0, x1_hi - x1_lo + 1)))

        return total

    @timeit
    def solve(self) -> int:
        return self.count_triangles(self.n)


class Solution513(unittest.TestCase):
    def setUp(self):
        self.problem = Problem513()

    def test_sample(self):
        self.assertEqual(3, self.problem.count_triangles(10))
        self.assertEqual(165, self.problem.count_triangles(50))

    def test_solution(self):
        self.assertEqual(2925619196, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
