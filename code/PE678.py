"""
PROBLEM

If a triple of positive integers (a,b,c) satisfies a2+b2=c2, it is called a Pythagorean triple.
No triple (a,b,c) satisfies ae+be=ce when e≥3 (Fermat's Last Theorem). However, if the exponents of the left-hand side
 and right-hand side differ, this is not true. For example, 3^3+6^3=3^5.

Let a,b,c,e,f be all positive integers, 0<a<b, e≥2, f≥3 and c^f≤N.
Let F(N) be the number of (a,b,c,e,f) such that a^e+b^e=c^f. You are given F(10^3)=7, F(10^5)=53 and F(10^7)=287.

Find F(10^18).

ANSWER:
????
Solve time ~???? seconds
"""

# Problem
# a^e + b^e = c^f, for 0 < a < b, e>= 2, f>=3, c^f <= 10^18
#
# https://www.science20.com/vastness_ways_science/parcelatories_powers_equations_fermats_last_theorem
# e and f need to be co-prime

# BEAL'S CONJECTURE:  If A^x + B^y = C^z, where A, B, C, x, y and z are positive integers
# and x, y and z are all greater than 2, then A, B and C must have a common prime factor.

# assuming the Beal conjecture, we can split the problem into 3 cases:

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
from math import ceil


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


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
    def solve2(self):
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        max_c = int(round(self.n**(1/3)))
        ls_primes = list(sieve(max_c))
        answer = 0
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        # for c in range(2, round(self.n**(1/3))+1):
        for c in range(3, max_c + 1):  # todo prove that c=2 does not work. This simplifies the below logic
            dc_prime = primes_of_n(c, ls_primes)
            f = 3
            new_dc_prime = {k: v*f for k, v in dc_prime.items()}
            while c**f <= self.n:
                # check if sum of squares
                answer += self.number_of_sum_of_squares(new_dc_prime)
                answer += self.check_if_sum_of_powers(round(c**f), c, f, lowest_e=3)  # this part needs to be faster
                f += 1
                new_dc_prime = {k: v * f for k, v in dc_prime.items()}
        return answer

    # @timeit
    # def solve(self):
    #     answer = 0
    #     # lowest value of f is 3
    #     # Therefore the highest value of c is N**(1/3)
    #     for c in range(2, round(self.n**(1/3))+1):
    #         f = 3
    #         while c**f <= self.n:
    #             answer += self.check_if_sum_of_powers(round(c**f), c, f)
    #             f += 1
    #     return answer

    @staticmethod
    def check_if_sum_of_powers(limit, c, f, lowest_e=2):
        """Returns how many a^e + b^e = limit, for a < b. Where limit = c^f"""
        count = 0
        for a in range(1, round((limit/2)**(1/lowest_e))+1):  # way too many
            for b in range(a+1, round((limit - a**lowest_e)**(1/lowest_e) + 1)):  # way too many
                e = lowest_e  # e must be either 2 or coprime to f
                fermat_sum = round(a**e + b**e)
                while fermat_sum < limit:
                    e += 1
                    fermat_sum = round(a**e + b**e)
                if fermat_sum == limit:
                    count += 1
                    print("a:{}, b:{}, e:{}, c:{}, f:{} , a^e + b^e:{}".format(a, b, e, c, f, a**e + b**e))
                    # print(primes_of_n(limit))
        return count


class Solution678(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem678(n=int(1e3))
        pass

    # def test_solution(self):
    #     # Fill this in once you've got a working solution!
    #     self.assertEqual(1, self.problem.solve())

    # def test_smallest_solution(self):
    #     problem = Problem678(n=int(1e3))
    #     self.assertEqual(7, problem.solve())
    #
    # def test_small_solution(self):
    #     problem = Problem678(n=int(1e5))
    #     self.assertEqual(53, problem.solve())

    def test_smallest_solution2(self):
        problem = Problem678(n=int(1e3))
        self.assertEqual(7, problem.solve2())

    def test_small_solution2(self):
        problem = Problem678(n=int(1e5))
        self.assertEqual(53, problem.solve2())

    def test_big_sample_solution2(self):
        problem = Problem678(n=int(1e7))  # takes 5 seconds.
        self.assertEqual(287, problem.solve2())

    # 1e7 takes 5 seconds
    # 1e8 takes 54 seconds

    # 1e18 for just case 1 takes: 24 seconds

    # def test_big(self):
    #     problem = Problem678(n=int(1e18))
    #     problem.solve2()


if __name__ == '__main__':
    unittest.main()
