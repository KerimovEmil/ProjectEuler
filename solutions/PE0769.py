"""
PROBLEM

Consider the following binary quadratic form:
f(x, y) = x^2 + 5xy + 3y^2

A positive integer q has a primitive representation if there exist positive integers x and y
such that q = f(x, y) and gcd(x, y) = 1.
We are interested in primitive representations of perfect squares. For example:
  17^2 = f(1, 9)
  87^2 = f(13, 40) = f(46, 19)

Define C(N) as the total number of primitive representations of z^2 for 0 < z <= N.
Multiple representations are counted separately, so for example z = 87 is counted twice.
You are given C(10^3) = 142 and C(10^6) = 142463.

Find C(10^14).

ANSWER: 14246712611506
Solve time: ~115 seconds

---
MATHEMATICAL DERIVATION:

1. Algebraic Transformation of the Binary Quadratic Form:
   We seek integer solutions to:
     x^2 + 5xy + 3y^2 = z^2,   x, y > 0,  gcd(x, y) = 1,  z <= N.
   Multiplying by 4 and completing the square:
     (2x + 5y)^2 - 13y^2 = 4z^2 = (2z)^2
     (2x + 5y - 2z)(2x + 5y + 2z) = 13y^2.

2. Parametrization via Conic Sections / Rational Points:
   By standard parametrization of rational points on conics, the solutions correspond to pairs of
   coprime integers (p, q) with gcd(p, q) = 1 such that:
     Branch 1: p > 0, q > sqrt(3)*p,
       z = q^2 + 5pq + 3p^2 <= N.
     Branch 2: p = -a < 0, sqrt(3)*a < q < 2.5a,
       z = -(q^2 - 5aq + 3a^2) <= N.

3. Primitivity Characterization:
   gcd(x, y) = 1 if and only if gcd(p, q) = 1 and, when 13 does not divide p, q !equiv 4p (mod 13).
   If q = 4p (mod 13), 13 divides both x and y, yielding non-primitive representations.

4. Efficient Counting via Inclusion-Exclusion & Smallest Prime Factor (SPF):
   For each p (up to ~6.13 * 10^6 for N = 10^14), the valid range of q is an interval [q_min, q_max].
   We precompute an SPF array using a linear sieve to extract distinct prime factors of p in O(omega(p)) time.
   Inclusion-exclusion over square-free divisors d | p counts integers in [q_min, q_max] coprime to p,
   and an additional linear congruence filter subtracts cases with q = 4p (mod 13).
"""

from array import array
import math
import unittest
from util.utils import timeit

SQRT3 = math.sqrt(3.0)

INV_MOD13 = [0] * 13
for a in range(1, 13):
    INV_MOD13[a] = pow(a, -1, 13)


def build_spf_linear(n: int) -> array:
    """Build smallest prime factor table up to n using a linear sieve."""
    spf = array("I", [0]) * (n + 1)
    primes: list[int] = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        si = spf[i]
        for p in primes:
            v = i * p
            if v > n:
                break
            spf[v] = p
            if p == si:
                break
    return spf


def distinct_prime_factors(n: int, spf: array) -> list[int]:
    """Return the distinct prime factors of n."""
    res: list[int] = []
    while n > 1:
        p = spf[n]
        res.append(p)
        while n % p == 0:
            n //= p
    return res


def count_coprime_interval_with_divs(
    n: int, L: int, R: int, spf: array
) -> tuple[int, list[int], list[int]]:
    """Count integers q in [L, R] with gcd(n, q) = 1 via inclusion-exclusion."""
    primes = distinct_prime_factors(n, spf)
    ds = [1]
    mus = [1]
    for pr in primes:
        m = len(ds)
        for i in range(m):
            ds.append(ds[i] * pr)
            mus.append(-mus[i])

    lm = L - 1
    total = 0
    for d, mu in zip(ds, mus):
        total += mu * (R // d - lm // d)
    return total, ds, mus


def _count_congruence_in_interval(L: int, R: int, mod: int, rem: int) -> int:
    """Count integers x in [L, R] with x = rem (mod mod)."""
    if rem < L:
        rem += ((L - rem + mod - 1) // mod) * mod
    if rem > R:
        return 0
    return 1 + (R - rem) // mod


def count_coprime_with_mod13_congruence(
    ds: list[int],
    mus: list[int],
    L: int,
    R: int,
    rem13: int,
) -> int:
    """Count integers q in [L, R] with gcd(q, n) = 1 and q = rem13 (mod 13)."""
    total = 0
    for d, mu in zip(ds, mus):
        inv = INV_MOD13[d % 13]
        m0 = (rem13 * inv) % 13
        rem = d * m0
        mod = 13 * d
        total += mu * _count_congruence_in_interval(L, R, mod, rem)
    return total


def max_abs_p_for_negative_branch(N: int) -> int:
    """Binary searches the maximum a = -p such that z <= N has valid solutions."""
    hi = int(math.isqrt(N)) + 2
    lo = 0
    while lo + 1 < hi:
        a = (lo + hi) // 2
        if a == 0:
            lo = a
            continue

        qmin = int(SQRT3 * a) + 1
        thr = 3 * a * a
        while qmin * qmin <= thr:
            qmin += 1

        qmax = (5 * a - 1) // 2
        if qmin > qmax:
            ok = False
        else:
            z = -(qmin * qmin - 5 * a * qmin + 3 * a * a)
            ok = z <= N

        if ok:
            lo = a
        else:
            hi = a
    return lo


class Problem769:
    def __init__(self, limit: int = 10**14):
        self.limit = limit

    def compute_C(self, n: int, spf: array = None) -> int:
        n = int(n)
        four_n = 4 * n
        total = 0
        isqrt = math.isqrt

        if spf is None:
            maxp = max(int(isqrt(n // 3)), max_abs_p_for_negative_branch(n))
            spf = build_spf_linear(maxp)

        # Branch 1: p > 0, q > sqrt(3)*p, z = q^2 + 5pq + 3p^2 <= N
        pmax = int(isqrt(n // 3))
        for p in range(1, pmax + 1):
            qmin = int(SQRT3 * p) + 1
            thr = 3 * p * p
            while qmin * qmin <= thr:
                qmin += 1

            disc = 13 * p * p + four_n
            qmax = (isqrt(disc) - 5 * p) // 2
            if qmax < qmin:
                continue

            pp3 = 3 * p * p
            while qmax >= qmin and (qmax * qmax + 5 * p * qmax + pp3) > n:
                qmax -= 1
            if qmax < qmin:
                continue

            cnt, ds, mus = count_coprime_interval_with_divs(p, qmin, qmax, spf)
            if p % 13 != 0:
                bad = count_coprime_with_mod13_congruence(ds, mus, qmin, qmax, (4 * p) % 13)
                cnt -= bad

            total += cnt

        # Branch 2: p = -a < 0, sqrt(3)*a < q < 2.5a, z = -(q^2 - 5aq + 3a^2) <= N
        amax = max_abs_p_for_negative_branch(n)
        threshold = int(isqrt(four_n // 13))

        for a in range(1, amax + 1):
            qmin = int(SQRT3 * a) + 1
            thr = 3 * a * a
            while qmin * qmin <= thr:
                qmin += 1

            qmax = (5 * a - 1) // 2
            if qmax < qmin:
                continue

            if a > threshold:
                disc = 13 * a * a - four_n
                s = isqrt(disc)
                lim = (5 * a - s) // 2
                if lim < qmax:
                    qmax = lim

            while qmax >= qmin and (-(qmax * qmax - 5 * a * qmax + 3 * a * a)) > n:
                qmax -= 1
            if qmax < qmin:
                continue

            cnt, ds, mus = count_coprime_interval_with_divs(a, qmin, qmax, spf)
            if a % 13 != 0:
                bad = count_coprime_with_mod13_congruence(ds, mus, qmin, qmax, (-4 * a) % 13)
                cnt -= bad

            total += cnt

        return total

    @timeit
    def solve(self) -> int:
        maxp = max(int(math.isqrt(self.limit // 3)), max_abs_p_for_negative_branch(self.limit))
        spf = build_spf_linear(maxp)
        return self.compute_C(self.limit, spf)


class Solution769(unittest.TestCase):
    def setUp(self):
        self.problem = Problem769()

    def test_sample(self):
        spf = build_spf_linear(1000)
        self.assertEqual(142, self.problem.compute_C(10**3, spf))
        spf = build_spf_linear(1000000)
        self.assertEqual(142463, self.problem.compute_C(10**6, spf))

    def test_solution(self):
        self.assertEqual(14246712611506, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
