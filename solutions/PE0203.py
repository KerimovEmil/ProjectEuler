"""
PROBLEM

The binomial coefficients comb(n, k) can be arranged in triangular form, Pascal's triangle, like this:
               1
             1   1
           1   2   1
         1   3   3   1
       1   4   6   4   1
     1   5  10  10   5   1
   1   6  15  20  15   6   1
 1   7  21  35  35  21   7   1
           .........

It can be seen that the first eight rows of Pascal's triangle contain twelve distinct numbers:
1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 21 and 35.

A positive integer n is called squarefree if no square of a prime divides n.
Of the twelve distinct numbers in the first eight rows of Pascal's triangle, all except 4 and 20 are squarefree.
The sum of the distinct squarefree numbers in the first eight rows is 105.

Find the sum of the distinct squarefree numbers in the first 51 rows of Pascal's triangle.

ANSWER: 34029210557338
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Prime Factor Bound on Binomial Coefficients:
   The first R rows of Pascal's triangle correspond to row indices 0 <= n < R (for R = 51, 0 <= n <= 50).
   Since comb(n, k) = n! / (k! * (n - k)!), every prime factor p dividing comb(n, k) must divide n!, which
   implies p <= n < R.
   More strongly, by Kummer's Theorem, the p-adic valuation v_p(comb(n, k)) equals the number of carries when
   adding k and n - k in base p. For any prime p > sqrt(n), n < p^2 has at most two base-p digits, so adding
   k and n - k in base p can produce at most 1 carry. Thus v_p(comb(n, k)) <= 1 for all primes p > sqrt(n)!
   Consequently, if p^2 divides comb(n, k), then p <= sqrt(R - 1).
   For R = 51 (n <= 50), only the 4 primes p in {2, 3, 5, 7} (with squares {4, 9, 25, 49}) can ever square-divide
   any entry in the first 51 rows!

2. Algorithm:
   - Collect all distinct values of comb(n, k) for 0 <= n < R and 0 <= k <= n // 2 (at most 640 unique values
     for R = 51).
   - Sieve primes up to isqrt(R - 1) and test each unique binomial coefficient against those prime squares.
"""

import math
import unittest
from util.utils import primes_upto, timeit


class Problem203:
    def __init__(self, rows: int = 51):
        self.rows = rows

    @staticmethod
    def sum_squarefree_pascal(rows: int) -> int:
        distinct_coeffs = {
            math.comb(n, k)
            for n in range(rows)
            for k in range(n // 2 + 1)
        }
        prime_squares = [int(p) ** 2 for p in primes_upto(math.isqrt(max(0, rows - 1)))]
        return sum(
            val for val in distinct_coeffs
            if all(val % ps != 0 for ps in prime_squares)
        )

    @timeit
    def solve(self) -> int:
        return self.sum_squarefree_pascal(self.rows)


class Solution203(unittest.TestCase):
    def setUp(self):
        self.problem = Problem203()

    def test_sample(self):
        self.assertEqual(105, self.problem.sum_squarefree_pascal(8))

    def test_solution(self):
        self.assertEqual(34029210557338, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
