"""
PROBLEM

Consider the following Diophantine equation:
16x^2 + y^4 = z^2
where x, y and z are positive integers.

Let S(N) = sum(x + y + z) where the sum is over all solutions (x, y, z) such that
1 <= x, y, z <= N and gcd(x, y, z) = 1.

For N = 100, there are only two such solutions: (3, 4, 20) and (10, 3, 41). So S(10^2) = 81.

You are also given that S(10^4) = 112851 (with 26 solutions), and
S(10^7) = 248876211 mod 10^9.

Find S(10^16). Give your answer modulo 10^9.

ANSWER: 255228881
Solve time: ~0.25 seconds

---
MATHEMATICAL DERIVATION:

1. Rewriting as a Pythagorean Equation:
   The equation can be rewritten as:
     (4x)^2 + (y^2)^2 = z^2.
   Since gcd(x, y, z) = 1, any prime dividing gcd(4x, y^2, z) must divide 2.
   Therefore, we divide the analysis based on whether y is odd or even:

2. Family 1 (y is odd):
   Here (4x, y^2, z) is a primitive Pythagorean triple with even leg 4x and odd leg y^2:
     4x = 2uv  ==>  2x = uv
     y^2 = u^2 - v^2
     z = u^2 + v^2
   for coprime u > v > 0 of opposite parity.
   Since y^2 + v^2 = u^2 with gcd(u, v) = 1, (v, y, u) is also a primitive Pythagorean triple.
   Since y is odd, v must be even. Thus there exist coprime a > b > 0 of opposite parity such that:
     v = 2ab,  y = a^2 - b^2,  u = a^2 + b^2.
   Substituting back:
     x = ab(a^2 + b^2)
     y = a^2 - b^2
     z = a^4 + 6a^2b^2 + b^4
   Here x + y + z = (a^4 + a^2) + a^3 b + (6a^2 - 1) b^2 + a b^3 + b^4.
   Bound: z <= N ==> b^2 <= sqrt(8a^4 + N) - 3a^2, and b < a.

3. Family 2 (y is even):
   If y is even, 16 | y^4 and 16 | 16x^2, so 16 | z^2 ==> 4 | z.
   Let y = 2k, z = 4w. Then x^2 + k^4 = w^2.
   Since gcd(x, y, z) = 1, x must be odd, so k must be even: y = 4m.
   Then x^2 + (4m^2)^2 = w^2 with x odd. This is a primitive Pythagorean triple:
     4m^2 = 2uv  ==>  uv = 2m^2,  x = u^2 - v^2,  w = u^2 + v^2,  z = 4w.
   Since gcd(u, v) = 1 and uv = 2m^2, one of u, v has the factor 2:
   - Case 2A (u is even): u = 2a^2, v = b^2 with b odd and 2a^2 > b^2:
       x = 4a^4 - b^4,  y = 4ab,  z = 16a^4 + 4b^4
       x + y + z = 20a^4 + 4ab + 3b^4.
   - Case 2B (v is even): u = a^2, v = 2b^2 with a odd and a^2 > 2b^2:
       x = a^4 - 4b^4,  y = 4ab,  z = 4a^4 + 16b^4
       x + y + z = 5a^4 + 4ab + 12b^4.

4. Fast Summation via Faulhaber's Formula & Möbius Inversion:
   Notice that in all families, for a fixed a, the summand (x + y + z) is a degree-4 polynomial P(b)
   in b. For N = 10^16, a <= N^(1/4) = 10^4.
   Instead of iterating over all 50 million pairs (a, b) and calling gcd:
     sum_{b <= M, gcd(b, a) = 1} P(b) = sum_{d | a} mu(d) sum_{j <= M/d} P(j*d)
   The inner sum sum_{j <= J} (j*d)^k is evaluated in O(1) time using Faulhaber's formulas for k = 0..4.
   Parity restrictions on b are handled by splitting into even and odd indices.
   This evaluates S(10^16) mod 10^9 across all 10,000 values of a in ~0.2 seconds!
"""

import math
import unittest
from util.utils import timeit

MOD = 10**9


def pow_sum(j: int):
    """Returns (sum j^0, sum j^1, sum j^2, sum j^3, sum j^4) for j = 1..J mod 10^9."""
    if j <= 0:
        return (0, 0, 0, 0, 0)
    s0 = j
    s1 = j * (j + 1) // 2
    s2 = j * (j + 1) * (2 * j + 1) // 6
    s3 = s1 * s1
    s4 = j * (j + 1) * (2 * j + 1) * (3 * j * j + 3 * j - 1) // 30
    return (s0 % MOD, s1 % MOD, s2 % MOD, s3 % MOD, s4 % MOD)


class Problem764:
    def __init__(self, limit: int = 10**16):
        self.limit = limit
        self.max_a = int(limit**0.25) + 1
        self._precompute_divisors(self.max_a)

    def _precompute_divisors(self, max_val: int):
        mu = [0] * max_val
        primes = []
        is_prime = [True] * max_val
        mu[1] = 1
        for i in range(2, max_val):
            if is_prime[i]:
                primes.append(i)
                mu[i] = -1
            for p in primes:
                if i * p >= max_val:
                    break
                is_prime[i * p] = False
                if i % p == 0:
                    mu[i * p] = 0
                    break
                mu[i * p] = -mu[i]

        self.divs = [[] for _ in range(max_val)]
        for d in range(1, max_val):
            if mu[d] != 0:
                for m in range(d, max_val, d):
                    self.divs[m].append((d, mu[d]))

    def _sum_poly_coprime(self, m: int, c0: int, c1: int, c2: int, c3: int, c4: int, a: int) -> int:
        total = 0
        for d, m_val in self.divs[a]:
            j = m // d
            if j <= 0:
                continue
            s0, s1, s2, s3, s4 = pow_sum(j)
            d2 = (d * d) % MOD
            d3 = (d2 * d) % MOD
            d4 = (d3 * d) % MOD
            term = (c0 * s0 + c1 * d * s1 + c2 * d2 * s2 + c3 * d3 * s3 + c4 * d4 * s4) % MOD
            total += m_val * term
        return total % MOD

    def compute_S(self, n: int) -> int:
        total = 0

        # Family 1: y odd
        max_a = int(n**0.25)
        for a in range(2, max_a + 1):
            a2 = a * a
            a4 = a2 * a2
            rad = math.isqrt(8 * a4 + n) - 3 * a2
            if rad <= 0:
                continue
            max_b = min(a - 1, math.isqrt(rad))
            if max_b <= 0:
                continue

            c0 = (a4 + a2) % MOD
            c1 = (a * a2) % MOD
            c2 = (6 * a2 - 1) % MOD
            c3 = a % MOD
            c4 = 1

            if a % 2 == 0:
                term = self._sum_poly_coprime(max_b, c0, c1, c2, c3, c4, a)
                total = (total + term) % MOD
            else:
                m = max_b // 2
                if m > 0:
                    k0 = c0
                    k1 = (2 * c1) % MOD
                    k2 = (4 * c2) % MOD
                    k3 = (8 * c3) % MOD
                    k4 = (16 * c4) % MOD
                    term = self._sum_poly_coprime(m, k0, k1, k2, k3, k4, a)
                    total = (total + term) % MOD

        # Family 2A: y even, u even
        max_a = int((n / 16)**0.25)
        for a in range(1, max_a + 1):
            a2 = a * a
            a4 = a2 * a2
            rem = (n - 16 * a4) // 4
            if rem <= 0:
                continue
            max_b = min(math.isqrt(2 * a2 - 1), math.isqrt(math.isqrt(rem)))
            if max_b <= 0:
                continue

            c0 = (20 * a4) % MOD
            c1 = (4 * a) % MOD
            c2 = 0
            c3 = 0
            c4 = 3

            if a % 2 == 0:
                term = self._sum_poly_coprime(max_b, c0, c1, c2, c3, c4, a)
                total = (total + term) % MOD
            else:
                term_all = self._sum_poly_coprime(max_b, c0, c1, c2, c3, c4, a)
                m = max_b // 2
                if m > 0:
                    k0 = c0
                    k1 = (2 * c1) % MOD
                    k2 = 0
                    k3 = 0
                    k4 = (16 * c4) % MOD
                    term_even = self._sum_poly_coprime(m, k0, k1, k2, k3, k4, a)
                else:
                    term_even = 0
                total = (total + term_all - term_even) % MOD

        # Family 2B: y even, v even
        max_a = int((n / 4)**0.25)
        for a in range(1, max_a + 1, 2):
            a2 = a * a
            a4 = a2 * a2
            rem = (n - 4 * a4) // 16
            if rem <= 0:
                continue
            max_b = min(math.isqrt((a2 - 1) // 2), math.isqrt(math.isqrt(rem)))
            if max_b <= 0:
                continue

            c0 = (5 * a4) % MOD
            c1 = (4 * a) % MOD
            c2 = 0
            c3 = 0
            c4 = 12
            term = self._sum_poly_coprime(max_b, c0, c1, c2, c3, c4, a)
            total = (total + term) % MOD

        return total % MOD

    @timeit
    def solve(self) -> int:
        return self.compute_S(self.limit)


class Solution764(unittest.TestCase):
    def setUp(self):
        self.problem = Problem764()

    def test_sample(self):
        self.assertEqual(81, self.problem.compute_S(100))
        self.assertEqual(112851, self.problem.compute_S(10000))
        self.assertEqual(248876211, self.problem.compute_S(10**7))

    def test_solution(self):
        self.assertEqual(255228881, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
