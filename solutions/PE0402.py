"""
PROBLEM

It can be shown that the polynomial n^4 + 4n^3 + 2n^2 + 5n is a multiple of 6 for every integer n.
It can also be shown that 6 is the largest integer satisfying this property.

Define M(a, b, c) as the maximum m such that n^4 + an^3 + bn^2 + cn is a multiple of m for all integers n.
For example, M(4, 2, 5) = 6.

Also, define S(N) as the sum of M(a, b, c) for all 0 < a, b, c ≤ N.

We can verify that S(10) = 1972 and S(10000) = 2024258331114.

Let F_k be the Fibonacci sequence:
F_0 = 0, F_1 = 1 and
F_k = F_{k-1} + F_{k-2} for k ≥ 2.

Find the last 9 digits of ∑ S(F_k) for 2 ≤ k ≤ 1234567890123.

ANSWER: 356019862
Solve time: ~0.02 seconds

---
MATHEMATICAL DERIVATION:

1. Divisibility of Polynomial P(n) = n^4 + a n^3 + b n^2 + c n:
   Any integer-valued polynomial that vanishes at 0 can be represented in the binomial basis:
   P(n) = c_1 binom(n, 1) + c_2 binom(n, 2) + c_3 binom(n, 3) + 24 binom(n, 4).
   Hence, m divides P(n) for all integer n iff m divides 24 and all intermediate values.
   Therefore, M(a, b, c) = gcd_{1 <= n <= 24} (P(n) mod 24).
   In particular, M(a, b, c) is completely periodic with period 24 in a, b, and c.

2. Piecewise Cubic Structure of S(N):
   Let N = 24q + r. The count of elements in 1..N congruent to i mod 24 is q + [i <= r].
   Substituting cnt[i] = N/24 + ( [i <= r] - r/24 ) into:
   S(N) = sum_{a=1}^24 sum_{b=1}^24 sum_{c=1}^24 M(a, b, c) cnt[a] cnt[b] cnt[c]
   shows that for each fixed residue r = N mod 24, S(N) is an exact degree-3 polynomial in N:
   S(N) = (I_3(r) N^3 + I_2(r) N^2 + I_1(r) N + I_0(r)) / 24^3, with integer coefficients I_p(r).

3. Summing S(F_k) over Fibonacci Numbers via Matrix Exponentiation:
   The Fibonacci sequence modulo 24 has Pisano period pi(24) = 24.
   For each fixed residue j in 0..23, r_k = F_k mod 24 is constant for all k = 24m + j.
   The state vector v_n = (F_{n+1}^3, F_{n+1}^2 F_n, ..., 1)^T of size 10 evolves linearly as v_{n+1} = T v_n.
   Setting A = T^24, we have v_{24(m+1) + j} = A v_{24m + j}.
   The sum of states sum_{m=0}^{M-1} v_{24m + j} is computed in O(log M) using the 20x20 block matrix:
   [[A, 0], [I, I]]^M.
   Summing across all 24 residue classes gives the total sum modulo 10^9 in milliseconds.
"""

from fractions import Fraction
import math
import unittest
from util.utils import timeit


def is_module(a, b, c, m):
    """Check if n^4 + a n^3 + b n^2 + c n is divisible by m for all n."""
    for n in range(1, m + 1):
        p = n * (n * (n * (n + a) + b) + c)
        if p % m != 0:
            return False
    return True


def max_int(a, b, c):
    """Get max divisor integer m dividing P(n) for all n."""
    g = 24
    for n in range(1, 25):
        val = n * (n * (n * (n + a) + b) + c)
        g = math.gcd(g, val)
    return g


M = max_int


def build_transition_matrix():
    """Build 10x10 transition matrix for Fibonacci powers up to degree 3."""
    return [
        [1, 3, 3, 1, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]


def mat_mul(a_mat, b_mat, mod):
    n, m, p = len(a_mat), len(b_mat[0]), len(b_mat)
    c_mat = [[0] * m for _ in range(n)]
    for i in range(n):
        for k in range(p):
            aik = a_mat[i][k]
            if aik == 0:
                continue
            for j in range(m):
                c_mat[i][j] = (c_mat[i][j] + aik * b_mat[k][j]) % mod
    return c_mat


def mat_pow(a_mat, p, mod):
    n = len(a_mat)
    res = [[int(i == j) for j in range(n)] for i in range(n)]
    base = a_mat
    while p > 0:
        if p & 1:
            res = mat_mul(res, base, mod)
        base = mat_mul(base, base, mod)
        p >>= 1
    return res


class Problem402:
    def __init__(self):
        self.denom = 24**3
        self.mod = 10**9
        self.mod_big = self.mod * self.denom
        self.m_table = self._build_m_table()
        self.int_polys = self._build_polynomials()
        self.t10 = build_transition_matrix()
        self.t24 = mat_pow(self.t10, 24, self.mod_big)
        self.block_matrix = self._build_block_matrix()

    def _build_m_table(self):
        m_table = [[[0] * 24 for _ in range(24)] for _ in range(24)]
        for a in range(24):
            for b in range(24):
                for c in range(24):
                    m_table[a][b][c] = max_int(a, b, c)
        return m_table

    def _build_block_matrix(self):
        block = [[0] * 20 for _ in range(20)]
        for i in range(10):
            for j in range(10):
                block[i][j] = self.t24[i][j]
            block[i + 10][i] = 1
            block[i + 10][i + 10] = 1
        return block

    def s(self, max_coeff):
        """Compute S(max_coeff) exactly using 24x24x24 residue block counting."""
        q, r = divmod(max_coeff, 24)
        cnt = [q + (1 if (i if i != 0 else 24) <= r else 0) for i in range(24)]
        total = 0
        for a in range(24):
            ca = cnt[a]
            if not ca:
                continue
            for b in range(24):
                cab = ca * cnt[b]
                if not cab:
                    continue
                for c in range(24):
                    total += self.m_table[a][b][c] * cab * cnt[c]
        return total

    def _build_polynomials(self):
        int_polys = []
        for r in range(24):
            pts = [r + 24 * k for k in range(4)]
            vals = [self.s(x) for x in pts]
            v_mat = [[x**p for p in range(4)] for x in pts]
            mat = [[Fraction(v_mat[i][j]) for j in range(4)] + [Fraction(vals[i])] for i in range(4)]
            for i in range(4):
                piv = mat[i][i]
                for j in range(5):
                    mat[i][j] /= piv
                for k in range(4):
                    if k != i:
                        factor = mat[k][i]
                        for j in range(5):
                            mat[k][j] -= factor * mat[i][j]
            int_polys.append([int(mat[i][4] * self.denom) for i in range(4)])
        return int_polys

    def _get_start_vectors(self):
        fib = [0, 1]
        for _ in range(30):
            fib.append(fib[-1] + fib[-2])
        v_list = []
        for j in range(24):
            f1, f0 = fib[j + 1], fib[j]
            v_list.append([
                (f1**3) % self.mod_big, (f1**2 * f0) % self.mod_big, (f1 * f0**2) % self.mod_big, (f0**3) % self.mod_big,
                (f1**2) % self.mod_big, (f1 * f0) % self.mod_big, (f0**2) % self.mod_big,
                f1 % self.mod_big, f0 % self.mod_big,
                1
            ])
        return fib, v_list

    def _sum_residue_class(self, j, k_max, fib, v_list):
        m_min = 0 if j >= 2 else 1
        m_max = (k_max - j) // 24
        if m_max < m_min:
            return 0
        num_terms = m_max - m_min + 1

        if m_min == 0:
            v_start = v_list[j]
        else:
            t_shift = mat_pow(self.t24, m_min, self.mod_big)
            v_start = [sum(t_shift[a][b] * v_list[j][b] for b in range(10)) % self.mod_big for a in range(10)]

        block_p = mat_pow(self.block_matrix, num_terms, self.mod_big)
        sum_vec = [0] * 10
        for i in range(10):
            s = 0
            for k in range(10):
                s = (s + block_p[10 + i][k] * v_start[k]) % self.mod_big
            sum_vec[i] = s

        r = fib[j] % 24
        i0, i1, i2, i3 = self.int_polys[r]
        term = (i3 * sum_vec[3] + i2 * sum_vec[6] + i1 * sum_vec[8] + i0 * sum_vec[9]) % self.mod_big
        return term

    @timeit
    def solve(self, k_max=1234567890123):
        fib, v_list = self._get_start_vectors()
        total_scaled_sum = 0
        for j in range(24):
            term = self._sum_residue_class(j, k_max, fib, v_list)
            total_scaled_sum = (total_scaled_sum + term) % self.mod_big
        return (total_scaled_sum // self.denom) % self.mod


class Solution402(unittest.TestCase):
    def setUp(self):
        self.problem = Problem402()

    def test_is_modular(self):
        self.assertEqual(True, is_module(a=4, b=2, c=5, m=6))

    def test_max_multiple(self):
        self.assertEqual(6, max_int(a=4, b=2, c=5))

    def test_solution_small(self):
        self.assertEqual(1972, self.problem.s(10))

    def test_solution_medium(self):
        self.assertEqual(2024258331114, self.problem.s(10000))

    def test_solution_final(self):
        self.assertEqual(356019862, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
