"""
PROBLEM

In the following equation x, y, and n are positive integers.
1/x + 1/y = 1/n
For a limit L we define F(L) as the number of solutions which satisfy x < y ≤ L.

We can verify that F(15) = 4 and F(1000) = 1069.
Find F(10^12).

ANSWER: 5435004633092
Solve time: ~85.0 seconds
"""

import math
import unittest
from util.utils import timeit


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
#      F(L) = sum_{v >= 2} sum_{1 <= u < v, gcd(u, v) = 1, v(u+v) <= L} floor(L / (v * (u + v)))
#
# 4. Substitution and Summation:
#    Let s = u + v. Since 1 <= u < v, we have v < s < 2v (i.e. s in [v + 1, 2v - 1]).
#    Also, gcd(u, v) = gcd(s - v, v) = gcd(s, v) = 1.
#    So:
#      F(L) = sum_{v >= 2} sum_{s=v+1, gcd(s, v)=1}^{min(2v-1, floor(L/v))} floor(L / (v * s))
#
# 5. Dual Summation via Square-free Counting:
#    Notice that summing floor(L / (v * (u + v))) over gcd(u, v) = 1 is equivalent to:
#      F(L) = sum_{k=1}^{floor(L/6)} |mu(k)| * T(floor(L / k))
#    where T(N) is the number of pairs (x, y) with 1 <= x < y and y * (x + y) <= N.
#    Swapping the order of summation gives:
#      F(L) = sum_{1 <= x < y, y(x+y) <= L} Q(floor(L / (y * (x + y))))
#    where Q(X) = sum_{k=1}^X |mu(k)| is the number of square-free integers up to X.
#
# 6. Fast Evaluation with Quotient Chunking:
#    Let s = x + y in [y + 1, 2y - 1].
#    - For y > floor(sqrt(L / 2)):
#        s ranges from y + 1 to floor(L / y), and floor(L / (y * s)) is always 1.
#        Since Q(1) = 1, this contribution is simply:
#          sum_{y = floor(sqrt(L/2)) + 1}^{y_max} (floor(L / y) - y)
#    - For y <= floor(sqrt(L / 2)):
#        s ranges from y + 1 to 2y - 1. We chunk the interval of s by constant quotients
#        q = floor(floor(L / y) / s), and add (count_s) * Q(q).
#    - Q(X) is precomputed up to Q_LIMIT = 5 * 10^6 via a linear square-free sieve and prefix sums.
#      For rare queries X > Q_LIMIT (which occur only when y < 448), Q(X) is computed via
#      Möbius inversion: Q(X) = sum_{d=1}^{floor(sqrt(X))} mu(d) * floor(X / d^2).


class Problem454:
    def __init__(self, limit: int = 10**12):
        self.limit = limit

    @timeit
    def solve(self, limit: int = None) -> int:
        if limit is None:
            limit = self.limit

        # 1. Precompute mu up to sqrt(limit / 6) for large Q(X) queries
        max_d = int(math.isqrt(limit // 6)) + 1
        mu = [0] * (max_d + 1)
        mu[1] = 1
        primes = []
        is_prime = [True] * (max_d + 1)
        for i in range(2, max_d + 1):
            if is_prime[i]:
                primes.append(i)
                mu[i] = -1
            for p in primes:
                if i * p > max_d:
                    break
                is_prime[i * p] = False
                if i % p == 0:
                    mu[i * p] = 0
                    break
                else:
                    mu[i * p] = -mu[i]

        # 2. Precompute Q_table (number of square-free integers up to X)
        q_limit = min(5 * 10**6, limit // 6 + 1)
        is_sqfree = [1] * (q_limit + 1)
        is_sqfree[0] = 0
        for p in primes:
            p2 = p * p
            if p2 > q_limit:
                break
            for j in range(p2, q_limit + 1, p2):
                is_sqfree[j] = 0

        q_table = [0] * (q_limit + 1)
        for i in range(1, q_limit + 1):
            q_table[i] = q_table[i - 1] + is_sqfree[i]

        def get_q(x: int) -> int:
            if x <= q_limit:
                return q_table[x]
            lim = int(math.isqrt(x))
            res = 0
            for d in range(1, lim + 1):
                if mu[d] != 0:
                    res += mu[d] * (x // (d * d))
            return res

        total_solutions = 0
        y_max = int((math.isqrt(1 + 4 * limit) - 1) // 2)
        y_split = int(math.isqrt(limit // 2))

        # Part 1: y from y_split + 1 to y_max (where q = 1 always)
        for y in range(y_split + 1, y_max + 1):
            total_solutions += (limit // y) - y

        # Part 2: y from 2 to y_split (chunking on q = floor(K / s))
        _q_table = q_table
        for y in range(2, y_split + 1):
            k = limit // y
            s_end = 2 * y - 1
            s = y + 1
            while s <= s_end:
                q = k // s
                s_next = min(s_end, k // q)
                val = _q_table[q] if q <= q_limit else get_q(q)
                total_solutions += (s_next - s + 1) * val
                s = s_next + 1

        return total_solutions


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
