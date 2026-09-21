"""
PROBLEM

A triangular pyramid is constructed using spherical balls such that one ball rests on top of three balls of the next lower level.
Then we calculate the number of paths leading from the apex to each position:
A path starts at the apex and progresses down to any of the three spheres directly below the current position.

Consequently, the number of paths to reach a position (i, j, k) at level n (where i + j + k = n) is given by the trinomial coefficient:
n! / (i! * j! * k!)

How many coefficients in the expansion of (x + y + z)^200000 are multiples of 10^12?

ANSWER: 479742450
Solve time: ~8.0 seconds
"""

import unittest
import numpy as np
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Trinomial Coefficients and Paths:
#    At level n of Pascal's pyramid, the position is given by non-negative integers (i, j, k)
#    such that i + j + k = n. The number of paths from the apex to position (i, j, k) is the
#    multinomial coefficient:
#      C(n; i, j, k) = n! / (i! * j! * k!)
#
# 2. Divisibility by 10^12:
#    C(n; i, j, k) is a multiple of 10^12 if and only if:
#      v_2(C(n; i, j, k)) >= 12  and  v_5(C(n; i, j, k)) >= 12
#    where v_p(x) is the p-adic valuation (highest power of prime p dividing x).
#
# 3. Legendre's Formula for Factorial Valuations:
#    By Legendre's formula, the exponent of prime p in m! is:
#      f_p[m] = v_p(m!) = sum_{k=1}^{inf} floor(m / p^k)
#    Therefore:
#      v_p(C(n; i, j, k)) = f_p[n] - f_p[i] - f_p[j] - f_p[k]
#
#    The conditions v_2 >= 12 and v_5 >= 12 are equivalent to:
#      f_2[i] + f_2[j] + f_2[k] <= f_2[n] - 12 = T_2
#      f_5[i] + f_5[j] + f_5[k] <= f_5[n] - 12 = T_5
#
# 4. Symmetry and Search Space Reduction:
#    The trinomial coefficient is symmetric under any permutation of (i, j, k).
#    We can restrict the search to ordered triples 0 <= i <= j <= k:
#      - i ranges from 0 to floor(n / 3).
#      - For a fixed i, j ranges from i to floor((n - i) / 2).
#      - k = n - i - j.
#
#    Each ordered triple (i, j, k) contributes to the total count based on its distinct permutations:
#      - If i < j < k: 3! = 6 permutations.
#      - If i == j < k or i < j == k: 3! / 2! = 3 permutations.
#      - If i == j == k: 3! / 3! = 1 permutation.
#
# 5. Vectorized NumPy Evaluation:
#    For each fixed i, we construct slices for j in [i, floor((n-i)/2)] and k in reverse order.
#    We apply the stricter condition on prime 5 first (since 5^12 is much more restrictive),
#    filter with a boolean mask, then check prime 2, and aggregate the symmetry-weighted counts.


def _get_factorial_valuations(p: int, n: int) -> np.ndarray:
    """Precomputes f_p[m] = v_p(m!) for all 0 <= m <= n using prefix sums."""
    res = np.zeros(n + 1, dtype=np.int32)
    step = p
    while step <= n:
        res[step::step] += 1
        step *= p
    return np.cumsum(res)


class Problem154:
    def __init__(self, n: int = 200000, exponent: int = 12):
        self.n = n
        self.exponent = exponent

    @timeit
    def solve(self, n: int = None, exponent: int = None) -> int:
        if n is None:
            n = self.n
        if exponent is None:
            exponent = self.exponent

        f2 = _get_factorial_valuations(2, n)
        f5 = _get_factorial_valuations(5, n)

        t2 = int(f2[n] - exponent)
        t5 = int(f5[n] - exponent)

        total_count = 0
        max_i = n // 3

        for i in range(max_i + 1):
            rem_5 = t5 - f5[i]
            rem_2 = t2 - f2[i]
            j_end = (n - i) // 2
            if i > j_end:
                continue

            j_arr5 = f5[i: j_end + 1]
            k_arr5 = f5[n - 2 * i: n - i - j_end - 1: -1]

            # Stricter filter on prime 5 first
            mask = (j_arr5 + k_arr5 <= rem_5)
            if not np.any(mask):
                continue

            j_arr2 = f2[i: j_end + 1]
            k_arr2 = f2[n - 2 * i: n - i - j_end - 1: -1]
            mask &= (j_arr2 + k_arr2 <= rem_2)

            if not np.any(mask):
                continue

            # Compute symmetry-weighted permutations
            c = int(np.count_nonzero(mask)) * 6
            if mask[0]:  # j == i
                c -= 3
            if (n - i) % 2 == 0:
                last_idx = j_end - i
                if mask[last_idx]:  # j == k
                    c -= 3
                    if last_idx == 0:  # i == j == k
                        c += 1

            total_count += c

        return total_count


class Solution154(unittest.TestCase):
    def setUp(self):
        self.problem = Problem154()

    def test_solution(self):
        self.assertEqual(479742450, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
