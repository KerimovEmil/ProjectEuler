"""
PROBLEM

"What? Where? When?" is a TV game show in which a team of experts attempts to answer questions.
The following is a simplified version of the game:

It begins with 2n + 1 envelopes. 2n of them contain a question and one contains a RED card.
In each round, one of the remaining envelopes is randomly chosen.
If the envelope contains the RED card, the game ends.
If the envelope contains a question, the expert gives their answer. If their answer is correct,
they earn one point; otherwise, the viewers earn one point.
The game ends normally when either the expert obtains n points or the viewers obtain n points.

Assuming that the expert provides the correct answer with a fixed probability p, let f(n, p)
be the probability that the game ends normally (i.e. the RED card never turns up).

You are given (rounded to 10 decimal places):
  f(6, 1/2) = 0.2851562500
  f(10, 3/7) = 0.2330040743
  f(10^4, 0.3) = 0.2857499982

Find f(10^11, 0.4999).
Give your answer rounded to 10 places behind the decimal point.

ANSWER: 0.0001999600
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Permutation of Envelopes & Random Red Card Position:
   There are 2n + 1 envelopes in total: 2n questions and 1 RED card.
   Because envelopes are drawn uniformly at random without replacement, the RED card is
   equally likely to occupy any position R in {1, 2, ..., 2n + 1} with probability 1 / (2n + 1).

2. Normal Termination Condition:
   Let K be the total number of questions answered until either the expert or viewers reach
   n points (assuming no RED card was drawn).
   Since someone must reach n points and the maximum number of questions is 2n - 1 <= 2n:
     n <= K <= 2n - 1.
   The game ends normally if and only if the RED card is NOT drawn during the first K rounds,
   which means the RED card position R satisfies R > K:
     P(R > K | K) = (2n + 1 - K) / (2n + 1) = 1 - K / (2n + 1).
   Taking the expectation over K:
     f(n, p) = E[1 - K / (2n + 1)] = 1 - E[K] / (2n + 1).

3. Exact Expectation via Negative Binomial / Binomial Tail Equivalence:
   The probability that the game ends at question k (where k = n + m with 0 <= m <= n - 1) is:
     P(K = k) = comb(k - 1, n - 1) [ p^n q^(k - n) + q^n p^(k - n) ]
   where q = 1 - p.
   Summing k * P(K = k) and using the identity k * comb(k - 1, n - 1) = n * comb(k, n):
     E[K] = n * [ P(B >= n + 1) / p + P(B <= n - 1) / q ]
   where B ~ Binomial(2n, p).

4. Asymptotic Regime for Large n (n = 10^11, p = 0.4999):
   For B ~ Binomial(2n, p):
     Mean: mu = 2n * p = 9.998 * 10^10 = n - 20,000,000.
     Variance: sigma^2 = 2n * p * q ~ 5 * 10^10, so sigma ~ 223,607.
   The boundary n is:
     z = (n - mu) / sigma = 20,000,000 / 223,607 ~ 89.44 standard deviations above the mean.
   Consequently:
     P(B >= n + 1) < 10^-1700 ~ 0,
     P(B <= n - 1) = 1 - P(B >= n) ~ 1.
   Thus the viewers win with probability virtually 1, and:
     E[K] = n / q = n / (1 - p).
   Therefore, for n = 10^11 and p = 0.4999:
     f(n, p) = 1 - (n / (1 - p)) / (2n + 1)
             = 1 - n / ((2n + 1) * (1 - p))
             = 0.000199960012997...
   Rounded to 10 decimal places:
     0.0001999600.
"""

from decimal import Decimal, getcontext
from typing import Union
import unittest
from util.utils import timeit


class Problem744:
    def __init__(self, n: int = 10**11, p: Union[float, Decimal] = 0.4999):
        self.n = n
        self.p = p

    @staticmethod
    def compute_f(n: int, p_val: Union[float, Decimal]) -> Decimal:
        """Computes f(n, p), the probability that the game ends normally."""
        getcontext().prec = 60
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

        return Decimal(1) - e_k / Decimal(2 * n + 1)

    @timeit
    def solve(self) -> str:
        ans = self.compute_f(self.n, self.p)
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
