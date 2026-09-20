"""
PROBLEM

If a triple of positive integers (a, b, c) satisfies a^2 + b^2 = c^2, it is called a
Pythagorean triple. No triple (a, b, c) satisfies a^e + b^e = c^e when e >= 3
(Fermat's Last Theorem).

However, if the exponents of the left-hand side and right-hand side differ, this is
not true. For example, 3^3 + 6^3 = 3^5.

Let a, b, c, e, f be all positive integers, 0 < a < b, e >= 2, f >= 3 and c^f <= N.
Let F(N) be the number of (a, b, c, e, f) such that a^e + b^e = c^f. You are given
F(10^3) = 7, F(10^5) = 53 and F(10^7) = 287.

Find F(10^18).

ANSWER: 1986065
Solve time: ~16.6 seconds
"""

import unittest
from functools import reduce
from math import floor, gcd, lcm, log2, log10
import operator

from util.utils import timeit, primes_of_n, primes_upto


def prod(iterable):
    """Return the product of the items in the iterable."""
    return reduce(operator.mul, iterable, 1)


class Problem678:
    def __init__(self, n):
        self.n = n

    @staticmethod
    def sols_from_primitive(cf, n, primes_of_c, e, f):
        """
        Number of solutions generated from one primitive solution with c^f = cf.
        Equals the count of integers w <= (n / cf)^(1 / lcm(e, f)) that are coprime
        to c, computed with Mobius-style inclusion-exclusion over the primes of c.
        """
        def loop(acc, x, i, mu):
            acc += x * mu
            for j in range(i, len(primes_of_c)):
                p = primes_of_c[j]
                if p > x:
                    break
                acc = loop(acc, x // p, j + 1, -mu)
            return acc

        limit = int(round((n // cf) ** (1 / lcm(e, f)), 12))
        return loop(0, limit, 0, 1)

    @staticmethod
    def smallest_prime_factor_sieve(limit):
        """Return a list where spf[x] is the smallest prime factor of x for x >= 2."""
        spf = list(range(limit + 1))
        for i in range(2, int(limit ** 0.5) + 1):
            if spf[i] == i:
                for j in range(i * i, limit + 1, i):
                    if spf[j] == j:
                        spf[j] = i
        return spf

    @staticmethod
    def factorize(spf, value):
        """Return the prime factorization of value as a dict of prime -> exponent."""
        factors = {}
        while value > 1:
            p = spf[value]
            factors[p] = factors.get(p, 0) + 1
            value //= p
        return factors

    @staticmethod
    def combined_factors(dict_a, dict_b):
        """Return the factor dict formed by merging the two factor dicts."""
        combined = dict(dict_a)
        for p, exp in dict_b.items():
            combined[p] = combined.get(p, 0) + exp
        return combined

    @timeit
    def solve_case2(self):
        """
        Count solutions with e >= 3. Assuming Beal's conjecture, a, b and c must all
        share a common prime factor, so every solution arises from scaling a primitive
        (coprime) pair (alpha, beta) with alpha^e + beta^e = c0.
        """
        n = self.n
        answers = 0
        fmax = int(log2(n))
        m = 1000
        # b^e <= c <= n^0.5 with e >= 3 caps b at n^(1/6) == 1000 for n = 10^18
        primes = [int(p) for p in primes_upto(40000)]
        # e == 3 splits as a^3 + b^3 = (a + b)(a^2 - ab + b^2) with a + b <= 2000 and
        # a^2 - ab + b^2 <= 10^6, so a smallest-prime-factor sieve up to min(n^0.5, 10^6)
        # factorizes both cofactors (both are at most c <= n^0.5).
        spf = self.smallest_prime_factor_sieve(min(int(n ** 0.5), 1_000_000))
        n_sqrt = n ** 0.5
        for a in range(1, m):
            for b in range(a + 1, m + 1):
                if gcd(a, b) != 1:
                    continue
                e = 3
                c = a ** e + b ** e
                while c <= n_sqrt:
                    if e == 3:
                        dc_prime_c = self.combined_factors(
                            self.factorize(spf, a + b),
                            self.factorize(spf, a * a - a * b + b * b),
                        )
                    else:
                        dc_prime_c = primes_of_n(c, primes)
                    factors = [(p, exp, p ** e) for p, exp in dc_prime_c.items()]
                    primes_of_c = list(dc_prime_c.keys())
                    # necessary condition: r_i + s_i*e == 0 (mod f) solvable for every
                    # prime exponent of c iff gcd(e, f) divides each r_i iff it divides
                    # their gcd.
                    exponent_gcd = 0
                    for _, exp, _ in factors:
                        exponent_gcd = gcd(exponent_gcd, exp)

                    def loop(acc, cf, i):
                        if i == len(factors):
                            return acc + Problem678.sols_from_primitive(
                                cf, n, primes_of_c, e, f
                            )
                        p, exp, pe = factors[i]
                        while cf <= n:
                            if exp % f == 0:
                                acc = loop(acc, cf, i + 1)
                            exp += e
                            cf *= pe
                        return acc

                    # c^f <= n with c >= 2 caps f at log2(n)
                    for f in range(3, fmax + 1):
                        if e == f:  # no solutions due to Fermat's Last Theorem
                            continue
                        if exponent_gcd % gcd(e, f):
                            continue
                        answers += loop(0, c, 0)
                    e += 1
                    c = a ** e + b ** e
        return answers

    @timeit
    def solve(self):
        n = self.n
        n_log = log10(n)
        max_c = int(round(n ** (1 / 3)))
        spf = self.smallest_prime_factor_sieve(max_c)

        answer = 0
        # case 1: e == 2, i.e. c^f expressible as a sum of two squares
        # The number of two-square representations of c^f depends only on the
        # exponents of primes == 1 (mod 4); primes == 3 (mod 4) may appear but only
        # with even exponent after scaling by f, so the factorization is split once.
        for c in range(3, max_c + 1):
            dc_prime = self.factorize(spf, c)
            mod4_1_exps = []
            has_odd_3mod4 = False
            for p, v in dc_prime.items():
                if p % 4 == 1:
                    mod4_1_exps.append(v)
                elif p % 4 == 3 and v % 2:
                    has_odd_3mod4 = True
            if not mod4_1_exps:
                continue
            all_even = all(v % 2 == 0 for v in mod4_1_exps)
            max_f = floor(round(n_log / log10(c), 12))
            for f in range(3, max_f + 1):
                if has_odd_3mod4 and f % 2:
                    # a prime == 3 (mod 4) keeps an odd exponent
                    continue
                partitions = (prod(v * f + 1 for v in mod4_1_exps) + 1) // 2
                if all_even or f % 2 == 0:
                    # a perfect square also has the form 0^2 + x^2
                    partitions -= 1
                answer += partitions

        # case 2: e >= 3 with e and f coprime to one another
        answer += self.solve_case2()
        return answer


class Solution678(unittest.TestCase):
    def setUp(self):
        self.problem = Problem678(n=10 ** 18)

    def test_sample_solution_1000(self):
        self.assertEqual(7, Problem678(n=10 ** 3).solve())

    def test_sample_solution_100000(self):
        self.assertEqual(53, Problem678(n=10 ** 5).solve())

    def test_sample_solution_10000000(self):
        self.assertEqual(287, Problem678(n=10 ** 7).solve())

    def test_sample_solution_1000000000000(self):
        self.assertEqual(16066, Problem678(n=10 ** 12).solve())

    def test_solution(self):
        self.assertEqual(1986065, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
