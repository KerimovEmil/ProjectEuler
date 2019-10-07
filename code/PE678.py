"""
PROBLEM

If a triple of positive integers (a,b,c) satisfies a2+b2=c2, it is called a Pythagorean triple.
No triple (a,b,c) satisfies ae+be=ce when e≥3 (Fermat's Last Theorem). However, if the exponents of the left-hand side
 and right-hand side differ, this is not true. For example, 3^3+6^3=3^5.

Let a,b,c,e,f be all positive integers, 0<a<b, e≥2, f≥3 and c^f≤N.
Let F(N) be the number of (a,b,c,e,f) such that a^e+b^e=c^f. You are given F(10^3)=7, F(10^5)=53 and F(10^7)=287.

Find F(10^18).

ANSWER:
1986065
Solve time ~135 seconds
"""

# Problem
# a^e + b^e = c^f, for 0 < a < b, e>= 2, f>=3, c^f <= 10^18
#
# https://www.science20.com/vastness_ways_science/parcelatories_powers_equations_fermats_last_theorem
# e and f need to be co-prime

# BEAL'S CONJECTURE:  If A^x + B^y = C^z, where A, B, C, x, y and z are positive integers
# and x, y and z are all greater than 2, then A, B and C must have a common prime factor.

# assuming the Beal conjecture, we can split the problem into 2 cases:

# CASE 1: e = 2
# a^2 + b^2 = c^f, for 0 < a < b, f>=3, c^f <= 10^18
# For this we can figure out if a number can be expressed as the sum of two squares by counting the number of prime
# factors in it. (see PE 229 and 233)
# Ignore powers of 2. 3 mod 4 primes must be even power. 1 mod 4 primes must exist OR odd power of 2.

# CASE 2: e > 2
# a^e + b^e = c^f, for 0 < a < b, e>= 3, f>=3, c^f <= 10^18
# Assuming Beal's conjecture, a,b,c must all have a common factor.

from util.utils import timeit, is_coprime, primes_of_n, sieve
import unittest
from functools import reduce
import operator
from math import ceil, log, floor, log10, gcd, log2


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def lcm(x, y):
    return x*y//gcd(x, y)


def sols_from_primitive(cf, N, ls_primes, e, f):
    # number of solutions generated from one primitive solution with c^f = cf
    # ans is the number of integers <= (N/cf)^(1/lcm(e,f)) which are coprime to c
    # P is a list of prime factors of c
    def loop(acc, x, i, mu):
        acc += x * mu
        for j in range(i, len(ls_primes)):
            p = ls_primes[j]
            if p > x:
                break
            acc = loop(acc, x // p, j + 1, -mu)
        return acc

    limit = int(round((N // cf)**(1/lcm(e, f)), 12))
    return loop(0, limit, 0, 1)


class Problem678:
    def __init__(self, n):
        self.n = n

    @staticmethod
    def number_of_sum_of_squares(dc_prime):
        """
        Given the prime factorization, outputs the number of ways this number can be represented as the sum of two
        squares. Excluding the a^2 + 0^2 case.
        This function does not consider any powers of 2, this simplifies the exceptions.
        Ignore powers of 2. 1 mod 4 primes must exist. 3 mod 4 primes must be even power.
        """
        # n is a sum of two squares iff it factors as n = ab^2, where a has no prime factor p ≡ 3 (mod 4)
        # 3 mod 4 primes must all be even powers
        if any(x % 2 != 0 for p, x in dc_prime.items() if p % 4 == 3):  # odd powers of bad primes
            return 0
        # NOTE: THIS EXCLUDES 0, SO NO 2^2 + 0^2 = 4.
        # n is a sum of two squares iff it factors as n = ab^2, where a has no prime factor p ≡ 3 (mod 4)
        # 3 mod 4 primes must all be even powers

        # At least one 1mod4 prime must exist. Ignoring the special condition of powers of 2.
        mod_4_remainder_1 = {k: v for k, v in dc_prime.items() if k % 4 == 1}
        if len(mod_4_remainder_1) == 0:
            return 0

        num_of_partitions = ceil(prod(v + 1 for k, v in mod_4_remainder_1.items()) / 2)
        # if perfect square then subtract 1 to eliminate the solution 0 + b^2 = square
        if all(exp % 2 == 0 for p, exp in mod_4_remainder_1.items()):
            num_of_partitions -= 1

        return num_of_partitions

    @timeit
    def solve_old(self):
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        max_c = int(round(self.n**(1/3)))
        answer = 0
        for c in range(3, max_c + 1):  # todo prove that c=2 does not work. This simplifies the below logic
            dc_prime = primes_of_n(c)
            f = 3
            new_dc_prime = {k: v * f for k, v in dc_prime.items()}

            while c**f <= self.n:
                # check if sum of squares
                answer += self.number_of_sum_of_squares(new_dc_prime)
                answer += self.check_if_sum_of_powers(round(c**f), c, f, lowest_e=3)
                f += 1
                new_dc_prime = {k: v * f for k, v in dc_prime.items()}
        return answer

    @staticmethod
    def check_if_sum_of_powers(limit, c, f, lowest_e=2):
        """
        Returns how many a^e + b^e = limit, for a < b. Where limit = c^f.
        Beal's conjecture: a,b,c must have a common prime factor.
        """
        count = 0
        # for a in range(1, round((limit/2)**(1/lowest_e))+1):  # way too many
        #     for b in range(a+1, round((limit - a**lowest_e)**(1/lowest_e) + 1)):  # way too many
        for a in range(c, round((limit / 2) ** (1 / lowest_e)) + 1, c):  # way too many
            if f == 3:
                range_b = [2*a]
            else:
                range_b = range(a + c, round((limit - a ** lowest_e) ** (1 / lowest_e) + 1), c)
            for b in range_b:  # way too many
                e = lowest_e  # e must be either 2 or coprime to f
                fermat_sum = round(a**e + b**e)
                while fermat_sum < limit:
                    e += 1
                    fermat_sum = round(a**e + b**e)
                if fermat_sum == limit:
                    count += 1
                    print("{}^{} + {}^{} = {}^{} = {}".format(a, e, b, e, c, f, limit))
        return count

    @timeit
    def solve_case2(self):
        answer = 0
        fmax = int(log2(self.n))
        m = 1000  # todo calibrate this top range
        # factor^e * (a^e + b^e = c). where c*factor^e <= N, e >= 3
        for a in range(1, m):
            for b in range(a + 1, m+1):
                if gcd(a, b) != 1:
                    continue
                e = 3
                c = a ** e + b ** e
                while c <= self.n ** 0.5:  # todo this is not related to N at all, just arbitary
                    # Find the prime factorisation of the sum of eth powers α^e+β^e = ∏_i p_i ^ r_i.
                    dc_prime_c = primes_of_n(c)
                    num_primes = len(dc_prime_c)
                    Q = list(dc_prime_c.items())
                    ls_primes_c = list(dc_prime_c.keys())
                    for f in range(3, fmax + 1):  # todo calibrate this fmax
                        if e == f:  # no solutions due to Fermat's Last Theorem
                            continue

                        # cf = c
                        # acc = 0
                        # for p, r in dc_prime_c.items():
                        #     while cf <= self.n:
                        #         if r % f == 0:
                        #             break
                        #         r += e
                        #         cf *= p ** e
                        # acc += sols_from_primitive(cf, self.n, ls_primes_c, e, f)
                        # answer += acc

                        # # generate possible factors by generating power combinations (si)
                        # dc_s = dict()
                        # for p, r in dc_prime_c.items():
                        #     while cf <= self.n:
                        #         if r % f == 0:
                        #             dc_s[p] = r
                        #         r += e
                        #         cf *= p ** e

                        # 2. Generate sets S={si} such that r_i+s_i*e ≡ 0 mod f for each i.
                        # 3. For each valid S, define k=∏_i p_i^s_i and then note that by setting a=kα and b=kβ
                        #    we have a^e+b^e=c^f for some c.
                        # 4. For each of these solutions (assuming c^f≤N), there may be additional - call them
                        #    "non-primitive" - solutions

                        def loop(acc, cf, i):
                            if i == num_primes:  # after using all of the primes already
                                acc += sols_from_primitive(cf, self.n, ls_primes_c, e, f)
                                return acc
                            p, t = Q[i]
                            while cf <= self.n:
                                if t % f == 0:
                                    acc = loop(acc, cf, i + 1)
                                t += e
                                cf *= p ** e
                            return acc

                        answer += loop(0, c, 0)
                    e += 1
                    c = a ** e + b ** e
        return answer

    @timeit
    def solve(self):
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        max_c = int(round(self.n ** (1 / 3)))
        ls_primes = list(sieve(max_c))
        answer = 0
        n_log = log10(self.n)

        # case 1
        for c in range(3, max_c + 1):
            dc_prime = primes_of_n(c, ls_primes)

            max_f = floor(round(n_log / log10(c), 12))
            answer += sum(self.number_of_sum_of_squares({k: v * f for k, v in dc_prime.items()})
                          for f in range(3, max_f + 1))

        print("Case1 values: {}".format(answer))
        # case 2
        answer += self.solve_case2()
        return answer


class Solution678(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem678(n=int(1e3))
        pass

    def test_smallest_solution_old(self):
        problem = Problem678(n=int(1e3))
        self.assertEqual(7, problem.solve_old())

    def test_smallest_solution(self):
        problem = Problem678(n=int(1e3))
        self.assertEqual(7, problem.solve())

    def test_small_solution_old(self):
        problem = Problem678(n=int(1e5))
        self.assertEqual(53, problem.solve_old())

    def test_small_solution(self):
        problem = Problem678(n=int(1e5))
        self.assertEqual(53, problem.solve())

    def test_big_sample_solution_old(self):
        problem = Problem678(n=int(1e7))
        self.assertEqual(287, problem.solve_old())

    def test_big_sample_solution(self):
        problem = Problem678(n=int(1e7))
        self.assertEqual(287, problem.solve())

    def test_bigger_sample_solution(self):
        problem = Problem678(n=int(1e12))
        self.assertEqual(16066, problem.solve())

    def test_solution(self):
        problem = Problem678(n=int(1e18))
        self.assertEqual(1986065, problem.solve())  # Case1 values: 1985353


if __name__ == '__main__':
    unittest.main()


# 1. Find the prime factorisation of the sum of eth powers
# α^e+β^e = ∏_i p_i ^ r_i.
# 2. Generate sets S={si} such that r_i+s_i*e ≡ 0 mod f for each i.
# 3. For each valid S, define k=∏_i p_i^s_i and then note that by setting a=kα and b=kβ we have a^e+b^e=c^f for some c.
# 4. For each of these solutions (assuming c^f≤N), there may be additional - call them "non-primitive" - solutions
#    whereby both sides are multiplied by some power wlcm(e,f), with w coprime to c (the coprime condition here is to
#    prevent double-counting of solutions).


# todo do this.
# I'd handled the e=3 case by factorising a^3+b^3 as:
#
# a^3+b^3=(a+b)(a^2−ab+b^2)=(a+b)((a+b)^2−3ab)=c^f
# Given d dividing c^f, let a+b=d, then 3ab=d^2−(c^f/d). Solving with the quadratic formula, we find a valid solution
# exists when d^2>(c^f/d), and 12(c^f/d)−3d^2 is a positive square.
