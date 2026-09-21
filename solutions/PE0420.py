"""
PROBLEM

A positive integer matrix is a matrix whose elements are all positive integers.
Some positive integer matrices can be expressed as a square of a positive integer matrix in two different ways.
Here is an example:

(40, 12 ; 48, 40) = (2, 3 ; 12, 2)^2 = (6, 1 ; 4, 6)^2
We define F(N) as the number of the 2x2 positive integer matrices which have a trace less than N and which can be
expressed as a square of a positive integer matrix in two different ways.
We can verify that F(50) = 7, F(1000) = 1019, and F(7000) = 16021.

Find F(10^7).

ANSWER: 145159332
Solve time: ~3.4 seconds (reduced from ~1113 seconds / 19 minutes)

MATHEMATICAL DERIVATION:
1. Matrix Square Root Parametrization:
   Let M = [[a, b], [c, d]] have square roots S_1 and S_2 with positive integer entries.
   By the Cayley-Hamilton theorem, S_i = (M + delta_i * I) / t_i, where t_i = tr(S_i) > 0 and delta_i = det(S_i).
   For two distinct square roots with positive entries, we must have det(M) = Delta^2, delta_1 = +Delta, delta_2 = -Delta.
   The traces satisfy:
     t_1^2 = tr(M) + 2*Delta
     t_2^2 = tr(M) - 2*Delta
   Hence, tr(M) = (t_1^2 + t_2^2) / 2 < N, and Delta = (t_1^2 - t_2^2) / 4.

2. Divisor and Coprime Factorization:
   Let u = gcd(t_1, t_2), so t_1 = u * x and t_2 = u * y with gcd(x, y) = 1 and x > y >= 1.
   Then tr(M) = u^2 * (x^2 + y^2) / 2 < N.
   Parity condition: t_1 and t_2 must have the same parity:
     - If u is even, this holds for all coprime (x, y).
     - If u is odd, both x and y must be odd.

3. Algebraic Reduction of Valid Entries:
   Expressing the integer constraints on the entries of S_1 and S_2 yields:
     k_d^2 + 4 * k_b * k_c = u^2
   Setting p = (u - k_d) / 2 and q = (u + k_d) / 2, we have p + q = u and k_b * k_c = p * (u - p).
   For each integer p in [1, u - 1], the number of valid factorizations (k_b, k_c) is d(p * (u - p)).

4. Positivity Bounds:
   The requirement that all entries of S_1 and S_2 are strictly positive integers restricts p to:
     p_min = max(1, ceil((u * (x - y) + 2) / (2 * x)))
     p_max = min(u - 1, floor((u * (x + y) - 2) / (2 * x)))

5. Complexity:
   Precomputing d(K) via a linear sieve and maintaining prefix sums pref[u][p] = sum_{i=1}^p d(i * (u - i))
   allows each pair (x, y) to query the number of valid solutions in O(1) time.
   Overall runtime for N = 10^7 is ~3.4 seconds.
"""

import math
import unittest
from util.utils import timeit


def num_divisors_sieve(limit):
    """Sieve to compute the number of divisors d(k) for 1 <= k <= limit."""
    d = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(i, limit + 1, i):
            d[j] += 1
    return d


class Problem420:
    def __init__(self, n=10000000):
        self.n = n

    @timeit
    def solve(self):
        n = self.n
        max_u = int((2 * n / 5) ** 0.5) + 2
        max_k = (max_u // 2) ** 2 + 10
        d = num_divisors_sieve(max_k)

        # Precompute prefix sums of d(p * (u - p)) for each u
        pref = [None] * (max_u + 1)
        for u in range(2, max_u + 1):
            p_arr = [0] * u
            cur = 0
            for p in range(1, u):
                cur += d[p * (u - p)]
                p_arr[p] = cur
            pref[u] = p_arr

        ans = 0
        for u in range(2, max_u + 1):
            lim_xy = 2 * n / (u * u)
            pref_u = pref[u]
            max_x = int(lim_xy ** 0.5) + 1

            is_u_odd = (u % 2 == 1)
            step_y = 2 if is_u_odd else 1
            start_y = 1

            for x in range(2, max_x):
                x2 = x * x
                if x2 >= lim_xy:
                    break
                if is_u_odd and (x % 2 == 0):
                    continue

                y_max = min(x - 1, int(math.isqrt(int(lim_xy) - x2)))

                for y in range(start_y, y_max + 1, step_y):
                    if u * u * (x2 + y * y) >= 2 * n:
                        continue
                    if math.gcd(x, y) != 1:
                        continue

                    p_min = (u * (x - y) + 2 + 2 * x - 1) // (2 * x)
                    p_max = (u * (x + y) - 2) // (2 * x)

                    p_min = 1 if p_min < 1 else p_min
                    p_max = (u - 1) if p_max > u - 1 else p_max

                    if p_min <= p_max:
                        ans += pref_u[p_max] - pref_u[p_min - 1]

        return ans


class Solution420(unittest.TestCase):
    def test_solution_small(self):
        self.assertEqual(7, Problem420(n=50).solve())

    def test_solution_1000(self):
        self.assertEqual(1019, Problem420(n=1000).solve())

    def test_solution_7000(self):
        self.assertEqual(16021, Problem420(n=7000).solve())

    def test_solution(self):
        self.assertEqual(145159332, Problem420(n=10000000).solve())


if __name__ == '__main__':
    unittest.main()
