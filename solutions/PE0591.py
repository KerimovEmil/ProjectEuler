"""
PROBLEM

Given a non-square integer d, any real x can be approximated arbitrarily close by quadratic integers
a + b*sqrt(d), where a, b are integers. For example, the following inequalities approximate pi with
precision 10^(-13):

4375636191520*sqrt(2) - 6188084046055 < pi < 721133315582*sqrt(2) - 1019836515172

We call BQA_d(x, n) the quadratic integer closest to x with the absolute values of a, b not exceeding n.
We also define the integral part of a quadratic integer as I_d(a + b*sqrt(d)) = a.

You are given that:
  BQA_2(pi, 10) = 6 - 2*sqrt(2)
  BQA_5(pi, 100) = 26*sqrt(5) - 55
  BQA_7(pi, 10^6) = 560323 - 211781*sqrt(7)
  I_2(BQA_2(pi, 10^13)) = -6188084046055

Find the sum of |I_d(BQA_d(pi, 10^13))| for all non-square positive integers less than 100.

ANSWER: 526007984625966
Solve time: ~0.20 seconds

---
MATHEMATICAL DERIVATION:

1. Inhomogeneous Diophantine Approximation:
   We seek integers a, b with |a|, |b| <= N = 10^13 minimizing |a + b*sqrt(d) - pi|.
   Rewriting: b*sqrt(d) - a approx pi, so for a given b, a is chosen close to b*sqrt(d) - pi.
   This is an inhomogeneous approximation problem on the circle: finding b such that b*sqrt(d) mod 1
   is as close as possible to pi mod 1.

2. Continued Fraction Convergents and Semi-Convergents:
   The homogeneous approximations to sqrt(d) are given by the continued fraction convergents p_k / q_k
   and semi-convergents (c*p_k + p_{k-1}) / (c*q_k + q_{k-1}) for 1 <= c <= a_{k+1}.
   At each convergent / semi-convergent p / q:
     p / q approx sqrt(d)  ==>  p - q*sqrt(d) approx 0.

3. Extended Euclidean Algorithm (Burger's Method):
   To approximate pi with denominator q, we set N_val = round(pi * q).
   Using the Extended Euclidean Algorithm on p and q:
     x * p + y * q = g.
   Scaling by N_val // g yields integer solutions to:
     v * p - u * q = N_val.
   Dividing by q gives v*(p/q) - u approx N_val / q approx pi, which corresponds to:
     cand_a = -u,   cand_b = v.
   Searching nearby shifts (k + dk) along the kernel of the modular equation yields the best
   quadratic integer approximation candidate within the box constraint max(|a|, |b|) <= N.

4. Efficiency:
   For N = 10^13, the continued fraction of sqrt(d) reaches the bound in ~60 to 80 terms.
   Iterating over all semi-convergents evaluates BQA_d(pi, 10^13) in ~0.002 seconds per d.
   Summing over all 90 non-squares d < 100 evaluates in ~0.20 seconds total.
"""

from decimal import Decimal, localcontext
import math
from typing import List, Tuple
import unittest
from util.utils import timeit

PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')


class Problem591:
    def __init__(self, n: int = 10**13, max_d: int = 100):
        self.n = n
        self.max_d = max_d

    @staticmethod
    def _egcd(a: int, b: int) -> Tuple[int, int, int]:
        if b == 0:
            return 1, 0, a
        x, y, g = Problem591._egcd(b, a % b)
        return y, x - (a // b) * y, g

    @staticmethod
    def _continued_fraction_sqrt(d: int, max_terms: int = 100) -> List[int]:
        m0, d0, a0 = 0, 1, int(math.isqrt(d))
        m, d_cur, a = m0, d0, a0
        terms = [a0]
        for _ in range(max_terms):
            m = d_cur * a - m
            d_cur = (d - m * m) // d_cur
            a = (a0 + m) // d_cur
            terms.append(a)
        return terms

    def BQA(self, d: int, n_max: int) -> Tuple[int, int]:
        """Compute the quadratic integer a + b*sqrt(d) closest to pi with |a|, |b| <= n_max."""
        with localcontext() as ctx:
            ctx.prec = 100
            sqrt_d = Decimal(d).sqrt()
            terms = self._continued_fraction_sqrt(d, 80)
            p0, p1 = 0, 1
            q0, q1 = 1, 0
            best_a, best_b = 3, 0
            best_err = abs(Decimal(3) - PI)

            for a_t in terms:
                for c in range(1, a_t + 1):
                    p = c * p1 + p0
                    q = c * q1 + q0
                    if q == 0:
                        continue

                    N_val = int(round(PI * q))
                    x, y, g = self._egcd(p, q)
                    if g != 1:
                        p_g, q_g = p // g, q // g
                        N_val_g = int(round(PI * q_g))
                        x_g, y_g, _ = self._egcd(p_g, q_g)
                        v0 = N_val_g * x_g
                        u0 = -N_val_g * y_g
                        q_mod, p_mod = q_g, p_g
                    else:
                        v0 = N_val * x
                        u0 = -N_val * y
                        q_mod, p_mod = q, p

                    k = int(round(v0 / q_mod))
                    for dk in range(-3, 4):
                        v = v0 - (k + dk) * q_mod
                        u = u0 - (k + dk) * p_mod
                        cand_a = -u
                        cand_b = v
                        if abs(cand_a) <= n_max and abs(cand_b) <= n_max:
                            err = abs(cand_a + cand_b * sqrt_d - PI)
                            if err < best_err:
                                best_err = err
                                best_a, best_b = cand_a, cand_b

                p = a_t * p1 + p0
                q = a_t * q1 + q0
                p0, p1 = p1, p
                q0, q1 = q1, q
                if q > 10 * n_max:
                    break

            return best_a, best_b

    def compute_sum(self, n_max: int, max_d: int) -> int:
        squares = {i * i for i in range(1, int(math.isqrt(max_d)) + 2)}
        total = 0
        for d in range(2, max_d):
            if d in squares:
                continue
            a, _ = self.BQA(d, n_max)
            total += abs(a)
        return total

    @timeit
    def solve(self) -> int:
        return self.compute_sum(self.n, self.max_d)


class Solution591(unittest.TestCase):
    def setUp(self):
        self.problem = Problem591()

    def test_sample(self):
        self.assertEqual((6, -2), self.problem.BQA(2, 10))
        self.assertEqual((-55, 26), self.problem.BQA(5, 100))
        self.assertEqual((560323, -211781), self.problem.BQA(7, 10**6))
        self.assertEqual(-6188084046055, self.problem.BQA(2, 10**13)[0])

    def test_solution(self):
        self.assertEqual(526007984625966, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
