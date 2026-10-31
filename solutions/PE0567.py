"""
PROBLEM

Tom has built a random generator that is connected to a row of n light bulbs. Whenever the random
generator is activated each of the n lights is turned on with the probability of 1/2, independently
of its former state or the state of the other light bulbs.

While discussing with his friend Jerry how to use his generator, they invent two different games,
they call the reciprocal games:

Both games consist of n turns. Each turn is started by choosing a number k randomly between
(and including) 1 and n, with equal probability of 1/n for each number, while the possible win
for that turn is the reciprocal of k, that is 1/k.

In game A, Tom activates his random generator once in each turn. If the number of lights turned on
is the same as the previously chosen number k, Jerry wins and gets 1/k, otherwise he will receive
nothing for that turn. Jerry's expected win after playing the total game A consisting of n turns
is called J_A(n). For example J_A(6) = 0.39505208, rounded to 8 decimal places.

For each turn in game B, after k has been randomly selected, Tom keeps reactivating his random
generator until exactly k lights are turned on. After that Jerry takes over and reactivates the
random generator until he, too, has generated a pattern with exactly k lights turned on. If this
pattern is identical to Tom's last pattern, Jerry wins and gets 1/k, otherwise he will receive
nothing. Jerry's expected win after the total game B consisting of n turns is called J_B(n).
For example J_B(6) = 0.43333333, rounded to 8 decimal places.

Let S(m) = sum_{n=1}^m (J_A(n) + J_B(n)). For example S(6) = 7.58932292, rounded to 8 decimal places.

Find S(123456789), rounded to 8 decimal places.

ANSWER: 75.44817535
Solve time: ~0.000 seconds

---
MATHEMATICAL DERIVATION:

1. Expected Win for Game A:
   In a single turn of Game A, given chosen k, the probability of obtaining exactly k heads in n
   independent coin tosses is C(n, k) * 2^(-n). Jerry receives 1/k on winning.
   Summed over n turns where k is uniformly distributed over {1, ..., n}:
     J_A(n) = n * sum_{k=1}^n (1/n) * C(n, k) * 2^(-n) * (1/k)
            = 2^(-n) * sum_{k=1}^n C(n, k) / k.
   Using the integral representation 1/k = int_0^1 x^(k-1) dx:
     sum_{k=1}^n C(n, k) / k = int_0^1 ((1 + x)^n - 1) / x dx
                             = sum_{j=1}^n (2^j - 1) / j.
   Thus:
     J_A(n) = 2^(-n) * sum_{j=1}^n (2^j - 1) / j.

2. Expected Win for Game B:
   Given k, both Tom and Jerry condition on generating a pattern with exactly k lights on.
   Each of the C(n, k) subsets of size k is equally likely, so the probability that Jerry's
   pattern matches Tom's pattern is 1 / C(n, k).
   Jerry's expected win over n turns:
     J_B(n) = n * sum_{k=1}^n (1/n) * (1 / (k * C(n, k)))
            = sum_{k=1}^n 1 / (k * C(n, k)).
   Using k * C(n, k) = n * C(n - 1, k - 1):
     J_B(n) = (1/n) * sum_{j=0}^{n-1} 1 / C(n - 1, j).
   By the well-known combinatorial identity:
     sum_{j=0}^N 1 / C(N, j) = ((N + 1) / 2^(N + 1)) * sum_{k=1}^{N + 1} 2^k / k.
   Setting N = n - 1:
     J_B(n) = 2^(-n) * sum_{k=1}^n 2^k / k.

3. Combining J_A(n) and J_B(n):
   Adding the two expressions:
     J_A(n) + J_B(n) = 2^(-n) * sum_{k=1}^n (2^k - 1) / k + 2^(-n) * sum_{k=1}^n 2^k / k
                     = 2^(1 - n) * sum_{k=1}^n 2^k / k - 2^(-n) * H_n,
   where H_n = sum_{k=1}^n 1/k is the n-th harmonic number.

4. Summation S(m) and Order Interchange:
   Summing over n = 1 to m:
     S(m) = sum_{n=1}^m (J_A(n) + J_B(n))
          = sum_{k=1}^m (1/k) * [ 4 - 2^(-(k-1)) - 2^(k - m + 1) + 2^(-m) ].
   Separating the terms:
     S(m) = 4 * H_m - 2 * sum_{k=1}^m 2^(-k) / k - sum_{j=0}^{m-1} 2^(1 - j) / (m - j) + 2^(-m) * H_m.

5. Asymptotics for m = 123456789:
   - 4 * H_m is evaluated to arbitrary precision via the Euler-Maclaurin expansion:
       H_m = ln(m) + gamma + 1/(2m) - 1/(12m^2) + 1/(120m^4) - ...
   - sum_{k=1}^m 2^(-k) / k = -ln(1 - 1/2) - sum_{k=m+1}^infinity 2^(-k) / k = ln(2), with error < 2^(-m) = 0.
   - sum_{j=0}^{m-1} 2^(1 - j) / (m - j) converges exponentially fast: the first 70 terms suffice for 10^(-20).
   - 2^(-m) * H_m is identically 0.
   Evaluation is instantaneous in ~0.000 seconds.
"""

from decimal import Decimal, localcontext
import unittest
from util.utils import timeit


# Euler-Mascheroni constant
GAMMA = Decimal('0.577215664901532860606512090082402431042159335939923598805767234884867726777664670936947063')


class Problem567:
    def __init__(self, m: int = 123456789):
        self.m = m

    @staticmethod
    def harmonic(n: int) -> Decimal:
        if n <= 1000:
            return sum(Decimal(1) / Decimal(k) for k in range(1, n + 1))
        dec_n = Decimal(n)
        return (
            dec_n.ln()
            + GAMMA
            + Decimal(1) / (2 * dec_n)
            - Decimal(1) / (12 * dec_n**2)
            + Decimal(1) / (120 * dec_n**4)
            - Decimal(1) / (252 * dec_n**6)
        )

    def compute_JA(self, n: int) -> float:
        with localcontext() as ctx:
            ctx.prec = 50
            val = Decimal(2)**(-n) * sum((Decimal(2)**j - 1) / Decimal(j) for j in range(1, n + 1))
            return round(float(val), 8)

    def compute_JB(self, n: int) -> float:
        with localcontext() as ctx:
            ctx.prec = 50
            val = Decimal(2)**(-n) * sum(Decimal(2)**k / Decimal(k) for k in range(1, n + 1))
            return round(float(val), 8)

    def compute_S(self, m: int) -> float:
        with localcontext() as ctx:
            ctx.prec = 50
            if m <= 20:
                val = sum(
                    Decimal(4 - 2**(-(k - 1)) - 2**(k - m + 1) + 2**(-m)) / Decimal(k)
                    for k in range(1, m + 1)
                )
                return round(float(val), 8)

            term1 = 4 * self.harmonic(m)
            term2 = 2 * Decimal(2).ln()
            term3 = sum(Decimal(2**(1 - j)) / Decimal(m - j) for j in range(min(m, 80)))
            return round(float(term1 - term2 - term3), 8)

    @timeit
    def solve(self) -> float:
        return self.compute_S(self.m)


class Solution567(unittest.TestCase):
    def setUp(self):
        self.problem = Problem567()

    def test_sample(self):
        self.assertAlmostEqual(0.39505208, self.problem.compute_JA(6), places=8)
        self.assertAlmostEqual(0.43333333, self.problem.compute_JB(6), places=8)
        self.assertAlmostEqual(7.58932292, self.problem.compute_S(6), places=8)

    def test_solution(self):
        self.assertEqual(75.44817535, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
