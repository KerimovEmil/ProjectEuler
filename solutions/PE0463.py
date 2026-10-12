"""
PROBLEM

The function f is defined for all positive integers as follows:
- f(1) = 1
- f(3) = 3
- f(2n) = f(n)
- f(4n + 1) = 2f(2n + 1) - f(n)
- f(4n + 3) = 3f(2n + 1) - 2f(n)

The function S(n) is defined as sum_{i=1}^n f(i).
S(8) = 22 and S(100) = 3604.

Find S(3^37). Give the last 9 digits of your answer.

ANSWER: 808981553
Solve time: ~0.0002 seconds

---
MATHEMATICAL & ALGEBRAIC DERIVATION:

1. Binary Bit-Reversal Interpretation of f(n):
   By induction on the binary representation of n:
   - f(2n) = f(n) strips all trailing zeros until an odd integer is reached.
   - For an odd integer m = (b_k b_{k-1} ... b_1 1)_2, the recurrences
     f(4n + 1) = 2f(2n + 1) - f(n) and f(4n + 3) = 3f(2n + 1) - 2f(n)
     satisfy f((b_k ... b_1 1)_2) = (1 b_1 ... b_k)_2, the binary bit-reversal of the odd part of n.

2. Isolating the Sum of Odd-Indexed Terms:
   Let S(n) = sum_{i=1}^n f(i) with S(0) = 0, S(1) = 1, S(2) = 2, S(3) = 5.
   Splitting S(2m + 1) into even and odd indices:
     S(2m + 1) = f(1) + sum_{k=1}^m f(2k) + sum_{k=1}^m f(2k + 1)
               = 1 + sum_{k=1}^m f(k) + sum_{k=1}^m f(2k + 1)
               = 1 + S(m) + sum_{k=1}^m f(2k + 1).
   Rearranging gives the fundamental odd-sum identity:
     sum_{k=1}^m f(2k + 1) = S(2m + 1) - S(m) - 1.                      (Eq. 1)

3. Four-Term Block Identity:
   For any k >= 1, summing a full block of 4 consecutive terms {4k, 4k + 1, 4k + 2, 4k + 3}:
     f(4k)     = f(2k) = f(k)
     f(4k + 1) = 2f(2k + 1) - f(k)
     f(4k + 2) = f(2k + 1)
     f(4k + 3) = 3f(2k + 1) - 2f(k)
   Adding these four equations together:
     f(4k) + f(4k + 1) + f(4k + 2) + f(4k + 3)
       = [1 - 1 + 0 - 2] f(k) + [0 + 2 + 1 + 3] f(2k + 1)
       = 6f(2k + 1) - 2f(k).                                            (Eq. 2)

4. Closed-Form Recurrences for S(4m + r) (r in {0, 1, 2, 3}):

   - Case r = 3: S(4m + 3)
     Partition {1, ..., 4m + 3} into {1, 2, 3} and blocks {4k, 4k + 1, 4k + 2, 4k + 3} for k = 1..m:
       S(4m + 3) = (f(1) + f(2) + f(3)) + sum_{k=1}^m [6f(2k + 1) - 2f(k)]
                 = 5 + 6 * sum_{k=1}^m f(2k + 1) - 2 * sum_{k=1}^m f(k)
     Substituting (Eq. 1):
       S(4m + 3) = 5 + 6 * [S(2m + 1) - S(m) - 1] - 2 * S(m)
                 = 6 S(2m + 1) - 8 S(m) - 1.                            (Eq. 3)

   - Case r = 0: S(4m)
     Using S(4m) = S(4(m - 1) + 3) + f(4m) and f(4m) = f(m) = S(m) - S(m - 1):
       S(4m) = [6 S(2m - 1) - 8 S(m - 1) - 1] + [S(m) - S(m - 1)]
             = 6 S(2m - 1) + S(m) - 9 S(m - 1) - 1.                     (Eq. 4)

   - Individual terms f(2m + 1) and f(4m + 1) in terms of S:
     Since f(2m) = f(m) = S(m) - S(m - 1), we have:
       f(2m + 1) = S(2m + 1) - S(2m) = S(2m + 1) - S(2m - 1) - f(m)
                 = S(2m + 1) - S(2m - 1) - S(m) + S(m - 1).             (Eq. 5)
     And for f(4m + 1):
       f(4m + 1) = 2f(2m + 1) - f(m)
                 = 2[S(2m + 1) - S(2m - 1) - f(m)] - f(m)
                 = 2 S(2m + 1) - 2 S(2m - 1) - 3 S(m) + 3 S(m - 1).     (Eq. 6)

   - Case r = 1: S(4m + 1)
     Adding (Eq. 4) and (Eq. 6) for S(4m + 1) = S(4m) + f(4m + 1):
       S(4m + 1) = [6 S(2m - 1) + S(m) - 9 S(m - 1) - 1]
                   + [2 S(2m + 1) - 2 S(2m - 1) - 3 S(m) + 3 S(m - 1)]
                 = 2 S(2m + 1) + 4 S(2m - 1) - 2 S(m) - 6 S(m - 1) - 1. (Eq. 7)

   - Case r = 2: S(4m + 2)
     Using f(4m + 2) = f(2m + 1) from (Eq. 5) and adding to (Eq. 7):
       S(4m + 2) = S(4m + 1) + f(2m + 1)
                 = [2 S(2m + 1) + 4 S(2m - 1) - 2 S(m) - 6 S(m - 1) - 1]
                   + [S(2m + 1) - S(2m - 1) - S(m) + S(m - 1)]
                 = 3 S(2m + 1) + 3 S(2m - 1) - 3 S(m) - 5 S(m - 1) - 1. (Eq. 8)

5. Complexity:
   At each level, n = 4m + r branches only into {2m + 1, 2m - 1, m, m - 1}.
   With memoization, evaluating S(3^37) visits only 349 unique states in O(log n) time.
"""

from functools import lru_cache
import unittest
from util.utils import timeit


class Problem463:
    def __init__(self):
        pass

    @staticmethod
    @lru_cache(maxsize=None)
    def compute_s(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 2
        if n == 3:
            return 5

        m, r = divmod(n, 4)
        if r == 0:
            return 6 * Problem463.compute_s(2 * m - 1) + Problem463.compute_s(m) - 9 * Problem463.compute_s(m - 1) - 1
        elif r == 1:
            return (
                2 * Problem463.compute_s(2 * m + 1)
                + 4 * Problem463.compute_s(2 * m - 1)
                - 2 * Problem463.compute_s(m)
                - 6 * Problem463.compute_s(m - 1)
                - 1
            )
        elif r == 2:
            return (
                3 * Problem463.compute_s(2 * m + 1)
                + 3 * Problem463.compute_s(2 * m - 1)
                - 3 * Problem463.compute_s(m)
                - 5 * Problem463.compute_s(m - 1)
                - 1
            )
        else:
            return 6 * Problem463.compute_s(2 * m + 1) - 8 * Problem463.compute_s(m) - 1

    @timeit
    def solve(self) -> int:
        return self.compute_s(3**37) % (10**9)


class Solution463(unittest.TestCase):
    def setUp(self):
        self.problem = Problem463()

    def test_sample(self):
        self.assertEqual(22, self.problem.compute_s(8))
        self.assertEqual(3604, self.problem.compute_s(100))

    def test_solution(self):
        self.assertEqual(808981553, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
