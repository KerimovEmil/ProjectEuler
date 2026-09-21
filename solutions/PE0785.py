"""
PROBLEM

Consider the following Diophantine equation:
 15(x^2 + y^2 + z^2) = 34(xy + xz + yz)
where x, y and z are positive integers.

Let S(N) be the sum of all solutions, (x, y, z), of this equation such that,
1 <= x <= y <= z <= N and gcd(x, y, z) = 1.

For N = 100, there are three such solutions - (1, 7, 16), (8, 9, 39), (11, 21, 72).
So S(100) = 184.

Find S(10^9).

ANSWER: 29526986315080920
Solve time: ~0.15 seconds
"""

import math
import unittest
from util.utils import timeit, mobius_sieve


# MATHEMATICAL DERIVATION:
#
# 1. Algebraic Transformation:
#    Let s = x + y + z.
#    Using (x + y + z)^2 = x^2 + y^2 + z^2 + 2(xy + xz + yz), we have:
#      2(xy + xz + yz) = s^2 - (x^2 + y^2 + z^2)
#      34(xy + xz + yz) = 17s^2 - 17(x^2 + y^2 + z^2)
#    Substituting into the original equation:
#      15(x^2 + y^2 + z^2) = 17s^2 - 17(x^2 + y^2 + z^2)
#      32(x^2 + y^2 + z^2) = 17s^2
#      32(x^2 + y^2 + z^2) = 17(x + y + z)^2
#
# 2. Centered Coordinates and Eisenstein Norm:
#    Let U = 3x - s, V = 3y - s, W = 3z - s, so that U + V + W = 0 and W = -(U + V).
#    Expressing x^2 + y^2 + z^2 in terms of U, V, W:
#      32 [ 3(s/3)^2 + (U^2 + V^2 + W^2)/9 ] = 17s^2
#      32/3 s^2 + 32/9 (U^2 + V^2 + (U+V)^2) = 17s^2
#      64/9 (U^2 + UV + V^2) = 19/3 s^2
#      64 (U^2 + UV + V^2) = 57 s^2
#
#    Since 57 is square-free (57 = 3 * 19), 64 | s^2 => 8 | s.
#    Letting s = 8k, we obtain the binary quadratic form:
#      U^2 + UV + V^2 = 57 k^2
#
# 3. Factorization in the Eisenstein Integers Z[omega]:
#    Here, Q(U, V) = U^2 + UV + V^2 = N(U - V*omega), where omega = (-1 + sqrt(-3))/2.
#    In Z[omega], 57 factors into primes as:
#      57 = 3 * 19 = N(1 - omega) * N(3 - 2*omega) = N((1 - omega)(3 - 2*omega)) = N(1 - 7*omega)
#    Every primitive solution corresponds to k = N(a - b*omega) = a^2 + ab + b^2 with gcd(a, b) = 1.
#    Multiplying the generator gamma = (8 + 7*omega) by (a - b*omega)^2 yields closed-form polynomials for (x, y, z):
#      x = b(3b - 2a)
#      y = a(5a + 2b)
#      z = (3a + 5b)(a + b) = 3a^2 + 8ab + 5b^2
#      s = x + y + z = 8(a^2 + ab + b^2)
#
# 4. Positivity, Ordering, and Primality Conditions:
#    - For positive x, y, z:
#      y > 0 and z > 0 hold for all positive integers a, b.
#      x = b(3b - 2a) > 0 requires b > 2a/3 (i.e. b >= floor(2a/3) + 1).
#      When b > 2a/3, z is always the maximum coordinate: z = 3a^2 + 8ab + 5b^2.
#    - Primality condition gcd(x, y, z) = 1:
#      Given gcd(a, b) = 1, gcd(x, y, z) divides 19.
#      Specifically, 19 | gcd(x, y, z) if and only if b ≡ 7a (mod 19).
#      Hence, primitive solutions are precisely those with b not ≡ 7a (mod 19).
#    - Bound:
#      5b^2 + 8ab + (3a^2 - N) <= 0 => b <= (-4a + sqrt(a^2 + 5N)) / 5.
#
# 5. Fast Summation via Mobius Inversion:
#    To compute S(N) = sum_{gcd(a, b)=1, b > 2a/3, b not= 7a mod 19, z <= N} 8(a^2 + ab + b^2):
#    We apply Mobius inversion over d = gcd(a, b):
#      S(N) = sum_{d >= 1, gcd(d, 19)=1} mu(d) * d^2 * sum_{a' >= 1} sum_{b'} 8((a')^2 + a'b' + (b')^2)
#    where b' ranges over [b_min(a'), b_max(a')] under 3(a')^2 + 8a'b' + 5(b')^2 <= floor(N / d^2).
#    For each a', the sum over b' is computed in O(1) time using polynomial sum formulas and
#    arithmetic progression sums modulo 19, achieving sub-second runtime for N = 10^9.


def _sum_poly(n: int):
    """Returns sum_{i=1}^n 1, sum_{i=1}^n i, sum_{i=1}^n i^2."""
    if n < 0:
        return 0, 0, 0
    return n, n * (n + 1) // 2, n * (n + 1) * (2 * n + 1) // 6


def _sum_range(b1: int, b2: int):
    """Returns count, sum(b), sum(b^2) for b in [b1, b2]."""
    if b1 > b2:
        return 0, 0, 0
    cnt = b2 - b1 + 1
    sum_b = (b1 + b2) * cnt // 2
    if b1 >= 0:
        _, _, sq2 = _sum_poly(b2)
        _, _, sq1 = _sum_poly(b1 - 1)
        sum_b2 = sq2 - sq1
    elif b2 <= 0:
        _, _, sq1 = _sum_poly(-b1)
        _, _, sq2 = _sum_poly(-b2 - 1)
        sum_b2 = sq1 - sq2
    else:
        _, _, sq2 = _sum_poly(b2)
        _, _, sq1 = _sum_poly(-b1)
        sum_b2 = sq2 + sq1
    return cnt, sum_b, sum_b2


def _sum_ap(b1: int, b2: int, rem: int, mod: int = 19):
    """Returns count, sum(b), sum(b^2) for b in [b1, b2] with b ≡ rem (mod mod)."""
    if b1 > b2:
        return 0, 0, 0
    j_min = math.ceil((b1 - rem) / mod)
    j_max = math.floor((b2 - rem) / mod)
    if j_min > j_max:
        return 0, 0, 0
    cnt, sum_j, sum_j2 = _sum_range(j_min, j_max)
    sum_b = rem * cnt + mod * sum_j
    sum_b2 = rem * rem * cnt + 2 * rem * mod * sum_j + mod * mod * sum_j2
    return cnt, sum_b, sum_b2


class Problem785:
    def __init__(self, max_n: int = 10**9):
        self.max_n = max_n

    @timeit
    def solve(self, n: int = None) -> int:
        if n is None:
            n = self.max_n

        max_d = int(math.isqrt(9 * n // 95))
        if max_d < 1:
            return 0

        mu = mobius_sieve(max_d)
        total_sum = 0

        for d in range(1, max_d + 1):
            if mu[d] == 0 or d % 19 == 0:
                continue

            m = n // (d * d)
            max_a = int(math.isqrt(9 * m // 95))

            d_sum = 0
            for a in range(1, max_a + 1):
                min_b = (2 * a) // 3 + 1
                disc = a * a + 5 * m
                max_b = int((math.isqrt(disc) - 4 * a) // 5)
                if max_b < min_b:
                    continue

                # Total sums over [min_b, max_b]
                cnt_all, sum_b_all, sum_b2_all = _sum_range(min_b, max_b)

                # Exclude arithmetic progression b ≡ 7a (mod 19)
                rem = (7 * a) % 19
                cnt_sub, sum_b_sub, sum_b2_sub = _sum_ap(min_b, max_b, rem, 19)

                cnt = cnt_all - cnt_sub
                sum_b = sum_b_all - sum_b_sub
                sum_b2 = sum_b2_all - sum_b2_sub

                # f(a, b) = 8(a^2 + ab + b^2)
                term = 8 * (a * a * cnt + a * sum_b + sum_b2)
                d_sum += term

            total_sum += mu[d] * (d * d) * d_sum

        return total_sum


class Solution785(unittest.TestCase):
    def setUp(self):
        self.problem = Problem785()

    def test_solution_small_100(self):
        """S(100) = 184"""
        self.assertEqual(184, self.problem.solve(n=100))

    def test_solution_small_1000(self):
        """S(1000) = 28176"""
        self.assertEqual(28176, self.problem.solve(n=1000))

    def test_solution_small_5000(self):
        """S(5000) = 731352"""
        self.assertEqual(731352, self.problem.solve(n=5000))

    def test_solution(self):
        self.assertEqual(29526986315080920, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
