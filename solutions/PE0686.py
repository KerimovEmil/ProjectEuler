"""
PROBLEM

2^7 = 128 is the first power of two whose leading digits are "12".
The next power of two whose leading digits are "12" is 2^80.

Define p(L, n) to be the nth-smallest positive integer j such that the base 10 representation of 2^j begins with the
digits of L.
So p(12, 1) = 7 and p(12, 2) = 80.

You are also given that p(123, 45) = 12710.

Find p(123, 678910).

ANSWER: 193060223
Solve time: ~0.12 seconds
"""

import unittest
from decimal import ROUND_CEILING, Decimal, localcontext

import numpy as np

from util.utils import timeit


class Problem686:
    DEC_PREC = 80
    TOL = 1e-7
    CHUNK = 1 << 20

    with localcontext() as ctx:
        ctx.prec = 80
        _LOG10_2 = Decimal(2).ln() / Decimal(10).ln()
        _LO = Decimal("1.23").ln() / Decimal(10).ln()
        _HI = Decimal("1.24").ln() / Decimal(10).ln()

    A = float(_LOG10_2)
    INV_A = 1.0 / A
    LO = float(_LO)
    HI = float(_HI)
    W = HI - LO

    def __init__(self, target_index):
        self.target_index = target_index

    @classmethod
    def _candidate_j(cls, m):
        """High-precision candidate exponent j = ceil((m + log10(1.23)) / log10(2))."""
        with localcontext() as ctx:
            ctx.prec = cls.DEC_PREC
            ctx.rounding = ROUND_CEILING
            return int(((Decimal(m) + cls._LO) / cls._LOG10_2).to_integral_value())

    @classmethod
    def _is_hit(cls, j):
        """Return True if 2**j begins with the digits 123 (verified to high precision)."""
        with localcontext() as ctx:
            ctx.prec = cls.DEC_PREC
            frac = (Decimal(j) * cls._LOG10_2) % 1
            return cls._LO <= frac < cls._HI

    @timeit
    def solve(self):
        target = self.target_index
        found = 0
        m0 = 0
        chunk = self.CHUNK
        lo = self.LO
        inv_a = self.INV_A
        a = self.A
        w = self.W
        tol = self.TOL

        while True:
            m = np.arange(m0, m0 + chunk, dtype=np.float64)
            s = m + lo
            u = s * inv_a
            j = np.ceil(u)
            r = j * a - s
            hit = r < w
            border = (r < tol) | (np.abs(r - w) < tol) | (np.abs(u - np.rint(u)) < tol)
            if border.any():
                truth = hit.copy()
                for k in np.nonzero(border)[0]:
                    truth[int(k)] = self._is_hit(self._candidate_j(int(m[int(k)])))
                hit = truth
            n_chunk = int(hit.sum())
            if found + n_chunk >= target:
                need = target - found
                pos = np.nonzero(hit)[0]
                k = int(pos[need - 1])
                return self._candidate_j(int(m[k]))
            found += n_chunk
            m0 += chunk


class Solution686(unittest.TestCase):
    def setUp(self):
        self.problem = Problem686(target_index=678910)

    def test_sample(self):
        self.assertEqual(12710, Problem686(target_index=45).solve())

    def test_solution(self):
        self.assertEqual(193060223, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
