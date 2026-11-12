r"""
PROBLEM

For a positive integer n, let d(n) be defined as the sum of the digits of n. For example, d(12345) = 15.

Let F(N) be the sum:
  F(N) = \sum_{n=1}^N \frac{n}{d(n)}.

You are given:
  F(10) = 19
  F(123) \approx 1.187764610390e3
  F(12345) \approx 4.855801996238e6

Find F(1234567890123456789).

Write your answer in scientific notation rounded to twelve significant digits after the decimal point.
Use a lowercase e to separate the mantissa and the exponent (e.g. 1.234567890123e18).

ANSWER: 9.627509725002e33
Solve time: ~0.005 seconds

---
MATHEMATICAL DERIVATION:

1. Grouping by Digit Sum:
   Instead of iterating over individual numbers n <= N, we group terms by their sum of digits s = d(n):
     F(N) = sum_{s=1..9K} (1 / s) * sum_{1 <= n <= N, d(n) = s} n.
   For N = 1234567890123456789, K = 19 digits, so the maximum possible digit sum is 9 * 19 = 171.

2. Simultaneous Digit DP:
   We can process the decimal digits of N from most significant to least significant in a single DP pass.
   At each digit position, maintain states parameterized by (is_less, s), where:
     - is_less: boolean indicating whether the prefix is already strictly smaller than the prefix of N.
     - s: sum of digits placed so far.
   For each state, we track:
     - cnt: the number of distinct prefixes reaching this state.
     - sum_val: the sum of the numerical values of these prefixes.

3. State Transitions:
   When appending a new digit d in 0..max_d:
     nxt_less = is_less or (d < limit_digit)
     nxt_s = s + d
     nxt_cnt = cnt
     nxt_val = 10 * sum_val + d * cnt
   Because appending digit d transforms each prefix value v into 10*v + d:
     sum_v (10*v + d) = 10 * sum v + d * sum 1 = 10 * sum_val + d * cnt.

4. Aggregation with High Precision:
   After all K digits are placed, for each digit sum s > 0:
     T(s) = sum_{is_less} sum_val(is_less, s)
   The total is:
     F(N) = sum_{s=1..171} (T(s) / s).
   Using `decimal.localcontext()` with 60 digits of precision prevents floating point roundoff errors
   without modifying global decimal context.
   Finally, format the result in scientific notation with 12 decimal places after the decimal point:
     mantissa * 10^exp -> e.g. "9.627509725002e33".
"""

from decimal import Decimal, localcontext
import unittest

from util.utils import timeit


def format_sci(d: Decimal) -> str:
    """Formats Decimal in scientific notation with 12 digits after the decimal point and lowercase e."""
    s = f"{d:.12e}"
    parts = s.split("e")
    mantissa = parts[0]
    exp = int(parts[1])
    return f"{mantissa}e{exp}"


class Problem776:
    def __init__(self, n: int = 1234567890123456789, precision: int = 60):
        self.n = n
        self.precision = precision

    def compute_F_decimal(self, n: int, precision: int | None = None) -> Decimal:
        if precision is None:
            precision = self.precision

        s_str = str(n)
        dp = {(False, 0): (1, 0)}

        for char in s_str:
            limit_digit = int(char)
            new_dp = {}
            for (is_less, s), (cnt, s_val) in dp.items():
                max_d = 9 if is_less else limit_digit
                for d in range(max_d + 1):
                    nxt_less = is_less or (d < limit_digit)
                    nxt_s = s + d
                    nxt_cnt = cnt
                    nxt_val = 10 * s_val + d * cnt

                    key = (nxt_less, nxt_s)
                    if key in new_dp:
                        prev_c, prev_v = new_dp[key]
                        new_dp[key] = (prev_c + nxt_cnt, prev_v + nxt_val)
                    else:
                        new_dp[key] = (nxt_cnt, nxt_val)
            dp = new_dp

        with localcontext() as ctx:
            ctx.prec = precision
            total = Decimal(0)
            for (is_less, s), (cnt, s_val) in dp.items():
                if s > 0:
                    total += Decimal(s_val) / Decimal(s)
            return +total

    def compute_F_sci(self, n: int) -> str:
        d = self.compute_F_decimal(n)
        return format_sci(d)

    @timeit
    def solve(self) -> str:
        return self.compute_F_sci(self.n)


class Solution776(unittest.TestCase):
    def setUp(self):
        self.problem = Problem776()

    def test_samples(self):
        self.assertEqual(19, int(self.problem.compute_F_decimal(10)))
        self.assertEqual("1.187764610390e3", self.problem.compute_F_sci(123))
        self.assertEqual("4.855801996238e6", self.problem.compute_F_sci(12345))

    def test_solution(self):
        self.assertEqual("9.627509725002e33", self.problem.solve())


if __name__ == "__main__":
    unittest.main()
