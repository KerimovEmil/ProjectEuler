"""
PROBLEM

Jeff eats a pie in an unusual way.

The pie is circular. He starts with slicing an initial cut in the pie along a radius.

While there is at least a given fraction F of pie left, he performs the following procedure:
- He makes two slices from the pie centre to any point of what is remaining of the pie border, any point on the remaining pie border equally likely. This will divide the remaining pie into three pieces.
- Going counterclockwise from the initial cut, he takes the first two pie pieces and eats them.

When less than a fraction F of pie remains, he does not repeat this procedure. Instead, he eats all of the remaining pie.

For x >= 1, let E(x) be the expected number of times Jeff repeats the procedure above with F = 1/x.

It can be verified that E(1) = 1, E(2) ≈ 1.2676536759, and E(7.5) ≈ 2.1215732071.

Find E(40) rounded to 10 decimal places behind the decimal point.

ANSWER: 3.2370342194
Solve time: ~0.00001 seconds

---
MATHEMATICAL DERIVATION:

1. Probability Distribution of Remaining Fraction:
   Suppose the current remaining pie has fraction s >= F.
   Two cuts are made independently and uniformly at random along the remaining arc [0, s]:
   U_1, U_2 ~ Uniform(0, s).
   Moving counterclockwise from the initial cut at 0, the first two pieces span [0, min(U_1, U_2)]
   and [min(U_1, U_2), max(U_1, U_2)].
   Their union is [0, max(U_1, U_2)], which Jeff eats.
   The remaining third piece has length Y = s - max(U_1, U_2).
   The random variable M = max(U_1, U_2) has CDF P(M <= m) = (m / s)^2 for m in [0, s].
   Thus Y = s - M has PDF:
   f_Y(y) = 2(s - y) / s^2, for y in [0, s].

2. Integral Equation to Euler-Cauchy ODE:
   Let E(s) be the expected number of remaining steps when the pie has size s.
   For s < F, E(s) = 0.
   For s >= F:
   E(s) = 1 + int_F^s E(y) * (2(s - y) / s^2) dy
   Multiply by s^2:
   s^2 * E(s) = s^2 + 2 * int_F^s E(y) * (s - y) dy

   Differentiating with respect to s:
   2s * E(s) + s^2 * E'(s) = 2s + 2 * int_F^s E(y) dy
   At s = F: 2F * E(F) + F^2 * E'(F) = 2F. Since E(F) = 1, we get E'(F) = 0.

   Differentiating a second time:
   2 * E(s) + 4s * E'(s) + s^2 * E''(s) = 2 + 2 * E(s)
   => s^2 * E''(s) + 4s * E'(s) = 2.

3. Exact Closed-Form Solution:
   This is an Euler-Cauchy differential equation.
   - Homogeneous solution: r(r - 1) + 4r = r^2 + 3r = 0 => r = 0, r = -3.
     E_h(s) = A + B * (s / F)^(-3).
   - Particular solution: E_p(s) = (2/3) * ln(s / F).
   Applying boundary conditions at s = F (where z = s / F = 1):
   - E(F) = 1 => A + B = 1.
   - E'(F) = 0 => (1 / F) * (-3B + 2/3) = 0 => B = 2/9, A = 7/9.

   Thus, for any s >= F with z = s / F:
   E(s) = 7/9 + (2/9) * (F / s)^3 + (2/3) * ln(s / F).
   Starting with a full pie (s = 1) and F = 1/x, we have s / F = x:
   E(x) = 7/9 + (2/9) * x^(-3) + (2/3) * ln(x).
"""

import math
import unittest
from util.utils import timeit


class Problem394:
    def __init__(self):
        pass

    def expected_repetitions(self, x: float) -> float:
        return 7.0 / 9.0 + (2.0 / 9.0) * (x ** -3) + (2.0 / 3.0) * math.log(x)

    @timeit
    def solve(self) -> str:
        ans = self.expected_repetitions(40.0)
        return f"{ans:.10f}"


class Solution394(unittest.TestCase):
    def setUp(self):
        self.problem = Problem394()

    def test_sample(self):
        self.assertEqual("1.0000000000", f"{self.problem.expected_repetitions(1.0):.10f}")
        self.assertEqual("1.2676536759", f"{self.problem.expected_repetitions(2.0):.10f}")
        self.assertEqual("2.1215732071", f"{self.problem.expected_repetitions(7.5):.10f}")

    def test_solution(self):
        self.assertEqual("3.2370342194", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
