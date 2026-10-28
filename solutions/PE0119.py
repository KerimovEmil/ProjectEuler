"""
PROBLEM

The number 512 is interesting because it is equal to the sum of its digits raised to some power:
5 + 1 + 2 = 8, and 8^3 = 512. Another example of a number with this property is 614656 = 28^4.

We shall define a_n to be the n-th term of this sequence and insist that a number must contain at least two
digits to have a sum.

You are given that a_2 = 512 and a_10 = 614656.

Find a_30.

ANSWER: 248155780267521
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Inverted Search Space via Base (Digit Sum) and Exponent:
   Testing every integer k >= 10 directly to check whether k is a power of its digit sum S(k) is intractable
   because a_30 ~ 2.48 * 10^14.
   Instead, observe that any valid term satisfies k = b^e where b = S(k) >= 2 and e >= 2 (since b^1 = b < 10^d
   for any d >= 2-digit number).
   For a candidate number k with d digits (k < 10^d), its digit sum is bounded by:
     b = S(k) <= 9 * d.
   Even for d <= 20 digits (k < 10^20), the base b cannot exceed 9 * 20 = 180.

2. Candidate Enumeration and Verification:
   Iterating over bases 2 <= b <= 100 and exponents e >= 2 such that b^e < 10^20 requires checking fewer than
   1,500 candidate powers (b, e). For each candidate k = b^e >= 10, we verify whether digits_sum(k) == b,
   collect all valid k into a sorted set, and return the 30th element.
"""

import unittest
from util.utils import digits_sum, timeit


class Problem119:
    def __init__(self, target_index: int = 30):
        self.target_index = target_index
        self._sequence: list[int] | None = None

    def get_sequence(self, limit_exp10: int = 20) -> list[int]:
        if self._sequence is not None:
            return self._sequence

        upper_bound = 10 ** limit_exp10
        max_base = 9 * limit_exp10
        terms: set[int] = set()

        for b in range(2, max_base + 1):
            val = b * b
            while val < upper_bound:
                if val >= 10 and digits_sum(val) == b:
                    terms.add(val)
                val *= b

        self._sequence = sorted(terms)
        return self._sequence

    def get_term(self, n: int) -> int:
        return self.get_sequence()[n - 1]

    @timeit
    def solve(self) -> int:
        return self.get_term(self.target_index)


class Solution119(unittest.TestCase):
    def setUp(self):
        self.problem = Problem119()

    def test_sample(self):
        self.assertEqual(512, self.problem.get_term(2))
        self.assertEqual(614656, self.problem.get_term(10))

    def test_solution(self):
        self.assertEqual(248155780267521, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
