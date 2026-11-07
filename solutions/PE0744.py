r"""
PROBLEM

"What? Where? When?" is a TV game show. Two teams, "Experts" and "Viewers",
play against each other.

The game consists of up to 13 rounds: each round a question is presented to
the Experts and they win 1 point if they answer correctly, or the Viewers win
1 point if the Experts answer incorrectly. The game ends when one of the teams
wins 6 points, or at the maximum number of rounds (13).

In each round, the Experts choose a question randomly from remaining available questions.
Assume each question has probability p of being answered correctly by the Experts,
independently of other questions.

Consider a generalized version where the first team to win n points wins the game,
with a maximum of 2n rounds.
Let f(n, p) be the probability that the game ends normally (i.e. one team gets n points).

You are given:
  f(6, 0.5) = 0.2851562500
  f(10, 3/7) = 0.2330040743
  f(10000, 0.3) = 0.2857499982

Find f(10^11, 0.4999).
Give your answer rounded to 10 decimal places (e.g. 0.1234567890).

ANSWER: 0.0001999600
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Game Dynamics:
   Let K be the random variable for the number of rounds until one team reaches n points.
   The game ends at round K = n + m (where 0 <= m < n) if:
   - Experts reach n points at round n + m (meaning they win exactly n - 1 of the first n + m - 1 rounds,
     and win the (n + m)-th round):
       P(Experts win at round n + m) = C(n + m - 1, m) * p^n * q^m.
   - Viewers reach n points at round n + m:
       P(Viewers win at round n + m) = C(n + m - 1, m) * q^n * p^m,
     where q = 1 - p.

2. Normal Termination Condition:
   The game ends normally if one team reaches n points before or at round 2n, and the game does not
   end by running out of questions. By Wald's identity / stopping times on random walks:
   When n is very large (e.g. n = 10^11) and p != 0.5 (here p = 0.4999, q = 0.5001):
   - The bias towards Viewers is:
       delta = q - p = 0.0002.
   - Over 2n rounds, the expected score difference is 2n * delta = 2 * 10^11 * 2 * 10^-4 = 4 * 10^7.
   - The standard deviation is sqrt(2n * p * q) ~ sqrt(5 * 10^10) ~ 2.23 * 10^5.
   - The z-score is 4 * 10^7 / (2.23 * 10^5) > 170.
   - Therefore, Viewers win with probability 1 - O(exp(-170^2 / 2)), which is 1 to hundreds of decimal places.
   - The expected number of rounds for Viewers to reach n points is:
       E[K] = n / q.
   - The probability of normal game end is:
       f(n, p) = 1 - E[K] / (2n + 1)
               = 1 - n / (q * (2n + 1))
               = 1 - 10^11 / (0.5001 * (2 * 10^11 + 1))
               = 1 - 1 / (0.5001 * 2.00000000001)
               = 1 - 1 / (1.000200000005001)
               ~ 0.00019996000799...
   Rounded to 10 decimal places:
     0.0001999600.
"""

from decimal import Decimal, localcontext
from typing import Union
import unittest
from util.utils import timeit


class Problem744:
    def __init__(self, n: int = 10**11, p: Union[float, Decimal] = 0.4999, precision: int = 60):
        self.n = n
        self.p = p
        self.precision = precision

    @staticmethod
    def compute_f(n: int, p_val: Union[float, Decimal], precision: int = 60) -> Decimal:
        """Computes f(n, p), the probability that the game ends normally."""
        with localcontext() as ctx:
            ctx.prec = precision
            p = Decimal(str(p_val)) if not isinstance(p_val, Decimal) else p_val
            q = Decimal(1) - p

            # Check Gaussian z-score for large n
            mu = Decimal(2 * n) * p
            sigma_sq = Decimal(2 * n) * p * q
            z = (Decimal(n) - mu) / sigma_sq.sqrt() if sigma_sq > Decimal(0) else Decimal(0)

            if n > 20_000 and z > Decimal(40):
                # Viewers win with probability 1 to machine precision
                e_k = Decimal(n) / q
            elif n > 20_000 and z < Decimal(-40):
                # Experts win with probability 1 to machine precision
                e_k = Decimal(n) / p
            else:
                # Exact summation for small/moderate n
                t1 = p**n
                t2 = q**n
                total_k = Decimal(0)
                for m in range(n):
                    k = n + m
                    total_k += (t1 + t2) * Decimal(k)
                    if m < n - 1:
                        ratio = Decimal(n + m) / Decimal(m + 1)
                        t1 = t1 * ratio * q
                        t2 = t2 * ratio * p
                e_k = total_k

            res = Decimal(1) - e_k / Decimal(2 * n + 1)
            return +res

    @timeit
    def solve(self) -> str:
        ans = self.compute_f(self.n, self.p, self.precision)
        return f"{ans:.10f}"


class Solution744(unittest.TestCase):
    def setUp(self):
        self.problem = Problem744()

    def test_sample(self):
        self.assertEqual("0.2851562500", f"{Problem744.compute_f(6, 0.5):.10f}")
        self.assertEqual(
            "0.2330040743",
            f"{Problem744.compute_f(10, Decimal(3) / Decimal(7)):.10f}"
        )
        self.assertEqual("0.2857499982", f"{Problem744.compute_f(10000, 0.3):.10f}")

    def test_solution(self):
        self.assertEqual("0.0001999600", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
