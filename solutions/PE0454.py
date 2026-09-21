"""
PROBLEM

In the following equation x, y, and n are positive integers.
1/x + 1/y = 1/n
For a limit L we define F(L) as the number of solutions which satisfy x < y ≤ L.

We can verify that F(15) = 4 and F(1000) = 1069.
Find F(10^12).

ANSWER: 5435004633092
Solve time: ~7.2 seconds
"""

import math
import unittest
import numpy as np
from util.utils import timeit, mobius_sieve


# MATHEMATICAL DERIVATION:
#
# 1. Connection to Problems 108 and 110:
#    In Problem 108 and Problem 110, the equation 1/x + 1/y = 1/n was studied for a fixed n.
#    Multiplying by xyn gives:
#      (x - n)(y - n) = n^2
#    Let a = x - n and b = y - n. Then a * b = n^2.
#    Since x < y, we have 1 <= a < b.
#    In PE 108 and PE 110, n was fixed and we counted divisors of n^2.
#    In PE 454, n varies freely and we bound y = n + b <= L.
#
# 2. Coprime Parameterization:
#    Let g = gcd(a, b). Then:
#      (a / g) * (b / g) = (n / g)^2
#    Since gcd(a/g, b/g) = 1 and their product is a square, each factor must be a square:
#      a / g = u^2,   b / g = v^2   where gcd(u, v) = 1 and 1 <= u < v.
#    Then:
#      n / g = u * v  ==>  n = g * u * v
#      x = n + a = g * u * v + g * u^2 = g * u * (u + v)
#      y = n + b = g * u * v + g * v^2 = g * v * (u + v)
#
#    This establishes a 1-to-1 bijection between integer solution triples (x, y, n) with x < y
#    and integer triples (g, u, v) such that gcd(u, v) = 1, 1 <= u < v, and g >= 1.
#
# 3. Bounding by y <= L:
#    The condition y <= L becomes:
#      g * v * (u + v) <= L  ==>  g <= floor(L / (v * (u + v)))
#    For a fixed pair (u, v) with gcd(u, v) = 1 and 1 <= u < v, the number of valid g >= 1 is:
#      floor(L / (v * (u + v)))
#
#    Therefore:
#      F(L) = sum_{1 <= u < v, gcd(u, v) = 1, v(u+v) <= L} floor(L / (v * (u + v)))
#
# 4. Möbius Inversion to Remove Coprimality:
#    Applying Möbius inversion sum_{d | gcd(u, v)} mu(d) gives:
#      F(L) = sum_{d=1}^{floor(sqrt(L))} mu(d) * G(floor(L / d^2))
#    where G(M) is the unconstrained sum over all positive integers (w, u, v) with u < v < 2u:
#      G(M) = sum_{w >= 1} sum_{u < v < 2u, w * u * v <= M} 1
#
# 5. 3D Dirichlet Hyperbola Method for G(M) in O(M^(2/3)):
#    To evaluate G(M) in sublinear O(M^(2/3)) time, we partition the region w * u * v <= M
#    by the smallest variable w <= floor(M^(1/3)):
#      - For a fixed w in [1, floor(M^(1/3))]:
#          1. Range 1 (v > w): sum floor(M / (w * v)) for v in [w + 1, 2w - 1].
#          2. Range 2 (k > floor(M^(1/3)) where k = u):
#             For k in [floor(M^(1/3)) + 1, floor(sqrt(M / w))]:
#               add max(0, min(floor(M / (w * k)), 2k - 1) - k).
#             When 2k - 1 <= floor(M / (w * k)) (i.e. k <= floor(sqrt(M / (2w)))),
#             the term is simply (k - 1), which is summed in O(1) via arithmetic progression.
#             The remaining values of k are evaluated using vectorized NumPy operations.
#
#    Across all d >= 1, the total time complexity is:
#      sum_{d >= 1} O((L / d^2)^(2/3)) = O(L^(2/3) * zeta(4/3)) = O(L^(2/3)),
#    which solves L = 10^12 in ~7 seconds.


def _innertriple(limit: int) -> int:
    """Computes G(limit) in O(limit^(2/3)) using the 3D Dirichlet hyperbola method."""
    if limit < 6:
        return 0

    cbrt = int(limit**(1 / 3))
    while (cbrt + 1)**3 <= limit:
        cbrt += 1
    while cbrt**3 > limit:
        cbrt -= 1

    total = 0
    for w in range(1, cbrt + 1):
        limit_w = limit // w

        # Loop 1: sum floor(limit_w / v) for v in [w + 1, 2w - 1]
        if w > 1:
            if w <= 16:
                for v in range(w + 1, 2 * w):
                    total += limit_w // v
            else:
                v = np.arange(w + 1, 2 * w, dtype=np.int64)
                total += int(np.sum(limit_w // v))

        # Loop 2: k in [cbrt + 1, rt]
        rt = math.isqrt(limit_w)
        k_split = math.isqrt(limit_w // 2)

        # Range A: k in [cbrt + 1, min(rt, k_split)] where mini2 = 2k - 1
        k_a_start = cbrt + 1
        k_a_end = min(rt, k_split)
        if k_a_start <= k_a_end:
            n_k = k_a_end - k_a_start + 1
            total += (k_a_start + k_a_end - 2) * n_k // 2

        # Range B: k in [max(cbrt + 1, k_split + 1), rt] where mini2 = limit_w // k
        k_b_start = max(cbrt + 1, k_split + 1)
        k_b_end = rt
        if k_b_start <= k_b_end:
            if k_b_end - k_b_start <= 16:
                for k in range(k_b_start, k_b_end + 1):
                    mini2 = limit_w // k
                    if mini2 >= k:
                        total += mini2 - k
            else:
                k = np.arange(k_b_start, k_b_end + 1, dtype=np.int64)
                mini2 = limit_w // k
                mask = mini2 >= k
                total += int(np.sum(mini2[mask] - k[mask]))

    return total


class Problem454:
    def __init__(self, limit: int = 10**12):
        self.limit = limit

    @timeit
    def solve(self, limit: int = None) -> int:
        if limit is None:
            limit = self.limit

        rt = math.isqrt(limit)
        mu = mobius_sieve(rt)

        ans = 0
        for d in range(1, rt + 1):
            if mu[d] != 0:
                sub_limit = limit // (d * d)
                if sub_limit < 6:
                    break
                ans += mu[d] * _innertriple(sub_limit)

        return ans


class Solution454(unittest.TestCase):
    def setUp(self):
        self.problem = Problem454()

    def test_examples(self):
        self.assertEqual(4, self.problem.solve(limit=15))
        self.assertEqual(1069, self.problem.solve(limit=1000))

    def test_solution(self):
        self.assertEqual(5435004633092, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
