r"""
PROBLEM

Let $\{x\}$ denote the fractional part of a real number $x$.

Define $f_N(x)$ to be the minimal value of $\{nx\}$ for integer $n$ satisfying $0 < n \le N$.

Further define $F(N)$ to be the expected value of $f_N(x)$ when $x$ is sampled uniformly in $[0, 1]$.

You are given $F(1) = \frac{1}{2}$, $F(4) = \frac{1}{4}$ and $F(10) \approx 0.1319444444444$.

Find $F(10^4)$ and give your answer rounded to 13 digits after the decimal point.

ANSWER: 0.0003452201133
Solve time: ~15 seconds

---
MATHEMATICAL DERIVATION:

1. Farey Sequence Partitioning of [0, 1]:
   The Farey sequence of order N, denoted F_N, is the ascending sequence of irreducible
   fractions a/b with 0 <= a <= b <= N and gcd(a, b) = 1.
   For any two consecutive Farey fractions a_1/b_1 < a_2/b_2:
       a_2 b_1 - a_1 b_2 = 1,  and  b_1 + b_2 > N.
   The open interval (a_1/b_1, a_2/b_2) contains no rational numbers with denominator <= N.
   Consequently, for every integer n in {1, ..., N}, {nx} is a strictly increasing linear
   function without fractional wrapping on (a_1/b_1, a_2/b_2).

2. Identification of the Minimizer Function on Each Farey Interval:
   For x in [a_1/b_1, a_2/b_2], write x = a_1/b_1 + t with t in [0, 1/(b_1 b_2)].
   For n = b_1:
       {b_1 x} = b_1 (x - a_1/b_1) = b_1 t in [0, 1/b_2].
   For any other integer n in {1, ..., N} (n != b_1):
       {n a_1/b_1} >= 1/b_1.
   Since b_1 + b_2 > N, the line {b_1 x} starts at 0 and reaches 1/b_2, strictly below
   the initial height 1/b_1 of any other line. Thus, {b_1 x} is strictly smaller than {nx}
   for all n != b_1 across the entire interval (a_1/b_1, a_2/b_2).
   Therefore, for all x in [a_1/b_1, a_2/b_2]:
       f_N(x) = min_{1 <= n <= N} {nx} = b_1 (x - a_1/b_1).

3. Exact Integral on Farey Intervals:
   The integral of f_N(x) over [a_1/b_1, a_2/b_2] evaluates to:
       \int_{a_1/b_1}^{a_2/b_2} f_N(x) dx = \int_0^{1/(b_1 b_2)} b_1 t dt
                                           = b_1 [t^2 / 2]_0^{1/(b_1 b_2)}
                                           = 1 / (2 b_1 b_2^2).

4. Total Expectation Summation:
   Summing across all consecutive pairs in F_N gives the exact expected value:
       F(N) = \int_0^1 f_N(x) dx = \sum_{(a_1/b_1, a_2/b_2) \in F_N} \frac{1}{2 b_1 b_2^2}.

5. Algorithmic Complexity:
   The number of Farey intervals is |F_N| - 1 = \sum_{k=1}^N \phi(k) \approx \frac{3}{\pi^2} N^2.
   For N = 10^4, there are ~30.4 million intervals.
   Using the standard O(1)-memory Farey recurrence:
       k = (N + b_1) // b_2,  (a_3, b_3) = (k a_2 - a_1, k b_2 - b_1)
   and Kahan compensated summation to eliminate floating-point precision loss across 30 million
   terms, F(10^4) computes in ~15 seconds with full 13-digit precision.
"""

import unittest
from util.utils import timeit


def compute_f_farey(n: int) -> float:
    """
    Compute F(N) = sum_{(a_1/b_1, a_2/b_2) in Farey(N)} 1 / (2 * b_1 * b_2^2)
    using Kahan compensated summation.
    """
    a1, b1, a2, b2 = 0, 1, 1, n
    total = 0.0
    c = 0.0  # Kahan compensation accumulator

    # First term: [0/1, 1/n]
    y = (1.0 / (2.0 * b1 * b2 * b2)) - c
    t = total + y
    c = (t - total) - y
    total = t

    while not (a2 == 1 and b2 == 1):
        k = (n + b1) // b2
        a1, b1, a2, b2 = a2, b2, k * a2 - a1, k * b2 - b1
        y = (1.0 / (2.0 * b1 * b2 * b2)) - c
        t = total + y
        c = (t - total) - y
        total = t

    return total


class Problem965:
    def __init__(self):
        pass

    @timeit
    def solve(self, n: int = 10000) -> str:
        """
        Compute F(n) and return the value rounded to 13 digits after the decimal point.
        """
        val = compute_f_farey(n)
        return f"{val:.13f}"


class Solution965(unittest.TestCase):
    def setUp(self):
        self.problem = Problem965()

    def test_sample_f1(self):
        self.assertAlmostEqual(0.5, compute_f_farey(1), places=10)

    def test_sample_f4(self):
        self.assertAlmostEqual(0.25, compute_f_farey(4), places=10)

    def test_sample_f10(self):
        self.assertAlmostEqual(19.0 / 144.0, compute_f_farey(10), places=10)

    def test_solution_final(self):
        self.assertEqual("0.0003452201133", self.problem.solve(10000))


if __name__ == '__main__':
    unittest.main()
