r"""
PROBLEM

Let $\{x\}$ denote the fractional part of a real number $x$.

Define $f_N(x)$ to be the minimal value of $\{nx\}$ for integer $n$ satisfying $0 < n \le N$.

Further define $F(N)$ to be the expected value of $f_N(x)$ when $x$ is sampled uniformly in $[0, 1]$.

You are given $F(1) = \frac{1}{2}$, $F(4) = \frac{1}{4}$ and $F(10) \approx 0.1319444444444$.

Find $F(10^4)$ and give your answer rounded to 13 digits after the decimal point.

ANSWER: 0.0003452201133
Solve time: ~0.02 seconds

---
MATHEMATICAL DERIVATION:

1. Farey Sequence Partitioning of [0, 1]:
   The Farey sequence of order N, denoted F_N, is the ascending sequence of irreducible
   fractions a/b with 0 <= a <= b <= N and gcd(a, b) = 1.
   For any two consecutive Farey fractions a_1/b_1 < a_2/b_2:
       a_2 b_1 - a_1 b_2 = 1,  and  b_1 + b_2 > N.
   The open interval (a_1/b_1, a_2/b_2) contains no rational numbers with denominator <= N.
   Consequently, for every integer n in {1, ..., N}, {nx} is a strictly increasing linear
   function without fractional wrapping on (a_1/b_1, a_2/b_2).

2. Identification of the Minimizer Function on Each Farey Interval:
   For x in [a_1/b_1, a_2/b_2], write x = a_1/b_1 + t with t in [0, 1/(b_1 b_2)].
   For n = b_1:
       {b_1 x} = b_1 (x - a_1/b_1) = b_1 t in [0, 1/b_2].
   For any other integer n in {1, ..., N} (n != b_1):
       {n a_1/b_1} >= 1/b_1.
   Since b_1 + b_2 > N, the line {b_1 x} starts at 0 and reaches 1/b_2, strictly below
   the initial height 1/b_1 of any other line. Thus, {b_1 x} is strictly smaller than {nx}
   for all n != b_1 across the entire interval (a_1/b_1, a_2/b_2).
   Therefore, for all x in [a_1/b_1, a_2/b_2]:
       f_N(x) = min_{1 <= n <= N} {nx} = b_1 (x - a_1/b_1).

3. Exact Integral on Farey Intervals:
   The integral of f_N(x) over [a_1/b_1, a_2/b_2] evaluates to:
       \int_{a_1/b_1}^{a_2/b_2} f_N(x) dx = \int_0^{1/(b_1 b_2)} b_1 t dt
                                           = b_1 [t^2 / 2]_0^{1/(b_1 b_2)}
                                           = 1 / (2 b_1 b_2^2).

4. Denominator Pairing & Reflection Symmetry:
   A fundamental property of Farey sequences states that two integers b_1, b_2 <= N appear as
   denominators of adjacent fractions in F_N if and only if gcd(b_1, b_2) = 1 and b_1 + b_2 > N.
   By symmetry (reflecting x <-> 1 - x), every pair (b_1, b_2) with b_1 < b_2 pairs with (b_2, b_1):
       \frac{1}{2 b_1 b_2^2} + \frac{1}{2 b_2 b_1^2} = \frac{b_1 + b_2}{2 b_1^2 b_2^2}.
   Thus, for N >= 2:
       F(N) = \sum_{\substack{1 \le b_1 < b_2 \le N \\ \gcd(b_1, b_2) = 1 \\ b_1 + b_2 > N}} \frac{b_1 + b_2}{2 b_1^2 b_2^2}.

5. Möbius Inversion & O(N log N) Evaluation:
   We eliminate the coprimality condition gcd(b_1, b_2) = 1 using the Möbius identity
   \sum_{d | \gcd(b_1, b_2)} \mu(d) = [\gcd(b_1, b_2) = 1].
   Substituting b_1 = dx, b_2 = dy with 1 <= x < y <= N/d and d(x + y) > N (i.e. x + y > N/d):
       F(N) = \sum_{d=1}^N \frac{\mu(d)}{2 d^3} \sum_{\substack{1 \le x < y \le N/d \\ x + y > N/d}} \frac{x + y}{x^2 y^2}
            = \sum_{d=1}^N \frac{\mu(d)}{2 d^3} \sum_{y=2}^{\lfloor N/d \rfloor} \sum_{x = x_{\min}}^{y - 1} \left( \frac{1}{y x^2} + \frac{1}{y^2 x} \right)
   where x_{\min} = \max(1, \lfloor N/d \rfloor + 1 - y).

   The inner sum over x is evaluated in O(1) time using precomputed prefix harmonic sums:
       H_1(k) = \sum_{x=1}^k \frac{1}{x}, \quad H_2(k) = \sum_{x=1}^k \frac{1}{x^2}.
   The total number of (d, y) pairs is \sum_{d=1}^N \lfloor N/d \rfloor \approx N \ln N.
   For N = 10^4, this requires only ~92,100 operations instead of ~30.4 million Farey intervals,
   reducing the runtime from ~15 seconds to ~0.02 seconds with exact precision via math.fsum.
"""

import math
import unittest
from util.utils import timeit


def compute_f_mobius(n: int) -> float:
    """
    Compute F(N) in O(N log N) time using Möbius inversion and precomputed prefix harmonic sums.
    """
    if n == 1:
        return 0.5

    # Linear sieve for Möbius function mu
    mu = [0] * (n + 1)
    mu[1] = 1
    primes = []
    is_prime = [True] * (n + 1)
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]

    # Precompute prefix sums of 1/x and 1/x^2
    inv = [0.0] * (n + 1)
    inv2 = [0.0] * (n + 1)
    for x in range(1, n + 1):
        inv[x] = inv[x - 1] + 1.0 / x
        inv2[x] = inv2[x - 1] + 1.0 / (x * x)

    terms = []
    for d in range(1, n + 1):
        if mu[d] == 0:
            continue
        d_factor = mu[d] / (2.0 * (d ** 3))
        lim = n // d

        for y in range(2, lim + 1):
            x_min = lim + 1 - y
            if x_min < 1:
                x_min = 1
            x_max = y - 1
            if x_min > x_max:
                continue

            sum_inv2 = inv2[x_max] - inv2[x_min - 1]
            sum_inv1 = inv[x_max] - inv[x_min - 1]
            val = sum_inv2 / y + sum_inv1 / (y * y)
            terms.append(d_factor * val)

    return math.fsum(terms)


def compute_f_farey(n: int) -> float:
    """
    Baseline O(N^2) computation iterating through all consecutive Farey intervals.
    """
    a1, b1, a2, b2 = 0, 1, 1, n
    terms = [(1.0 / (2.0 * b1 * b2 * b2))]

    while not (a2 == 1 and b2 == 1):
        k = (n + b1) // b2
        a1, b1, a2, b2 = a2, b2, k * a2 - a1, k * b2 - b1
        terms.append(1.0 / (2.0 * b1 * b2 * b2))

    return math.fsum(terms)


class Problem965:
    def __init__(self):
        pass

    @timeit
    def solve(self, n: int = 10000) -> str:
        """
        Compute F(n) and return the value rounded to 13 digits after the decimal point.
        """
        val = compute_f_mobius(n)
        return f"{val:.13f}"


class Solution965(unittest.TestCase):
    def setUp(self):
        self.problem = Problem965()

    def test_sample_f1(self):
        self.assertAlmostEqual(0.5, compute_f_mobius(1), places=10)

    def test_sample_f4(self):
        self.assertAlmostEqual(0.25, compute_f_mobius(4), places=10)

    def test_sample_f10(self):
        self.assertAlmostEqual(19.0 / 144.0, compute_f_mobius(10), places=10)

    def test_sample_f10_farey(self):
        self.assertAlmostEqual(19.0 / 144.0, compute_f_farey(10), places=10)

    def test_solution_final(self):
        self.assertEqual("0.0003452201133", self.problem.solve(10000))


if __name__ == '__main__':
    unittest.main()
