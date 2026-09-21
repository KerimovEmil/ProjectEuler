"""
PROBLEM

A root or zero of a polynomial P(x) is a solution to the equation P(x) = 0.
Define P_n as the polynomial whose coefficients are the digits of n.
For example, P_5703(x) = 5x^3 + 7x^2 + 3.

We can see that:
* P_n(0) is the last digit of n,
* P_n(1) is the sum of the digits of n,
* P_n(10) is n itself.

Define Z(k) as the number of positive integers, n <= k, for which the polynomial P_n has at least one integer root.

It can be verified that:
Z(100) = 33,
Z(10^5) = 14696.

Find Z(10^16).

ANSWER: 1311109198529286
Solve time: ~0.08 seconds
"""

import itertools
import math
import unittest
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Root Constraints for Digit Polynomials:
#    Let n have base-10 digits d_{L-1} ... d_1 d_0 with d_{L-1} > 0 and d_i in [0, 9].
#    The polynomial is P_n(x) = d_{L-1} x^{L-1} + ... + d_1 x + d_0.
#
#    - Positive roots: For x > 0, since all coefficients are non-negative and d_{L-1} > 0,
#      P_n(x) >= d_{L-1} x^{L-1} > 0. Hence, there are NO positive roots.
#    - Zero root: P_n(0) = d_0 = 0. Therefore, x = 0 is a root if and only if n ends in 0.
#      Among positive integers n <= 10^L, exactly 10^{L-1} numbers end in 0 (including 10^L).
#    - Negative integer roots: By the Rational Root Theorem, any integer root r must divide
#      the constant term d_0. Since d_0 in {1, 2, ..., 9}, the only possible negative integer
#      roots are r in {-1, -2, ..., -9} such that |r| divides d_0.
#
# 2. Carry Dynamic Programming for a Single Root r = -k:
#    The condition P_n(-k) = d_0 - k*d_1 + k^2*d_2 - ... + (-k)^{L-1}*d_{L-1} = 0
#    can be evaluated from right to left (least significant to most significant digit)
#    using a carry variable:
#      c_1 = d_0 / k  (valid only if k | d_0)
#      At step m >= 1 with digit d_m in [0, 9]:
#        requires (d_m - c_m) ≡ 0 (mod k)
#        c_{m+1} = (d_m - c_m) / k
#      A number satisfies P_n(-k) = 0 if and only if the final carry c_L = 0.
#
#    Because d_m in [0, 9], the carries c_m remain strictly bounded in a small interval
#    (e.g., |c_m| <= 9 / (k - 1) for k >= 2, and |c_m| <= 9 for k = 1).
#
# 3. Multiple Roots & Principle of Inclusion-Exclusion (PIE):
#    To find the number of integers having AT LEAST ONE integer root among K(d_0) = {k : k | d_0}:
#    We apply PIE:
#      Count(d_0) = sum_{empty != T subset K(d_0)} (-1)^{|T|-1} * Count(d_0, T)
#    where Count(d_0, T) is the number of digit sequences with last digit d_0 where P_n(-k) = 0
#    for ALL k in T simultaneously.
#
#    For a subset T = {k_1, k_2, ..., k_r}, the DP state is the tuple of carries (c_{k_1}, ..., c_{k_r}).
#    We group all initial conditions across different d_0 that share the same root subset T,
#    allowing us to compute the DP for all 35 distinct subsets in under 0.1 seconds.


class Problem269:
    def __init__(self, max_n: int = 10**16):
        self.max_n = max_n

    @timeit
    def solve(self, max_n: int = None) -> int:
        if max_n is None:
            max_n = self.max_n

        # Determine number of digits L such that max_n = 10^L
        length = int(round(math.log10(max_n)))

        divisors_map = {
            1: [1],
            2: [1, 2],
            3: [1, 3],
            4: [1, 2, 4],
            5: [1, 5],
            6: [1, 2, 3, 6],
            7: [1, 7],
            8: [1, 2, 4, 8],
            9: [1, 3, 9]
        }

        # 1. Integers with root = 0 (ending in 0, up to 10^L)
        total = 10 ** (length - 1)

        # 2. Group subsets T of roots across all d0 in 1..9 for PIE
        subset_map = {}
        for d0 in range(1, 10):
            divs = divisors_map[d0]
            for r in range(1, len(divs) + 1):
                for t in itertools.combinations(divs, r):
                    sign = (-1) ** (r - 1)
                    if t not in subset_map:
                        subset_map[t] = []
                    subset_map[t].append((d0, sign))

        # 3. Run carry DP for each distinct subset T
        for t, d0_list in subset_map.items():
            dp = {}
            for d0, sign in d0_list:
                init_carries = tuple(d0 // k for k in t)
                dp[init_carries] = dp.get(init_carries, 0) + sign

            for step in range(1, length):
                new_dp = {}
                for carries, count in dp.items():
                    if count == 0:
                        continue
                    for d in range(10):
                        valid = True
                        next_carries = []
                        for idx, k in enumerate(t):
                            c = carries[idx]
                            if (d - c) % k != 0:
                                valid = False
                                break
                            next_carries.append((d - c) // k)
                        if valid:
                            next_tup = tuple(next_carries)
                            new_dp[next_tup] = new_dp.get(next_tup, 0) + count
                dp = new_dp

            zero_carries = tuple(0 for _ in t)
            total += dp.get(zero_carries, 0)

        return total


class Solution269(unittest.TestCase):
    def setUp(self):
        self.problem = Problem269()

    def test_solution_100(self):
        """Z(100) = 33"""
        self.assertEqual(33, self.problem.solve(max_n=100))

    def test_solution_100000(self):
        """Z(10^5) = 14696"""
        self.assertEqual(14696, self.problem.solve(max_n=100000))

    def test_solution(self):
        self.assertEqual(1311109198529286, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
