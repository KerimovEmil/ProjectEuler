"""
PROBLEM

The Fibonacci numbers {f_n, n >= 0} are defined recursively as f_n = f_n-1 + f_n-2
with base cases f_0 = 0 and f_1 = 1.

Define the polynomials {F_n, n >= 0} as F_n(x) = sum of f_i * x^i for 0 <= i <= n.

For example, F_7(x) = x + x^2 + 2x^3 + 3x^4 + 5x^5 + 8x^6 + 13x^7, and
F_7(11) = 268357683.

Let n = 10^15. Find the sum over 0 <= x <= 100 of F_n(x) mod 1307674368000 (= 15!).

ANSWER: 252541322550
Solve time: ~0.064 seconds
"""

import unittest
from util.utils import timeit


class Problem435:
    def __init__(self, n, mod):
        self.n = n
        self.mod = mod

    def mat_mul(self, a, b):
        mod = self.mod
        return [[sum(a[r][k] * b[k][c] for k in range(3)) % mod for c in range(3)]
                for r in range(3)]

    def mat_pow(self, m, exp):
        result = [[1 if r == c else 0 for c in range(3)] for r in range(3)]
        while exp:
            if exp & 1:
                result = self.mat_mul(result, m)
            m = self.mat_mul(m, m)
            exp >>= 1
        return result

    def f_n_at(self, x):
        """Return F_n(x) mod self.mod using the 3x3 recurrence state."""
        if x == 0:
            return 0
        mod = self.mod
        x %= mod
        x_sq = x * x % mod
        transition = [[0, 1, 0], [x_sq, x, 0], [x_sq, x, 1]]
        power = self.mat_pow(transition, self.n - 1)
        return ((power[2][1] + power[2][2]) * x) % mod

    @timeit
    def solve(self):
        return sum(self.f_n_at(x) for x in range(101)) % self.mod


class Solution435(unittest.TestCase):
    def setUp(self):
        mod = 1307674368000
        self.problem = Problem435(n=10 ** 15, mod=mod)

    def test_solution(self):
        self.assertEqual(252541322550, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
