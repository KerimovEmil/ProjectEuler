"""
PROBLEM

Consider the number 3600. It is very special, because

3600 = 48^2 +   36^2
3600 = 20^2 + 2×40^2
3600 = 30^2 + 3×30^2
3600 = 45^2 + 7×15^2

Similarly, we find that 88201 = 99^2 + 280^2 = 287^2 + 2×54^2 = 283^2 + 3×52^2 = 197^2 + 7×84^2.

In 1747, Euler proved which numbers are representable as a sum of two squares.
We are interested in the numbers n which admit representations of all of the following four types:

n = a_1^2 +   b_1^2
n = a_2^2 + 2×b_2^2
n = a_3^2 + 3×b_3^2
n = a_7^2 + 7×b_7^2,
where the a_k and b_k are positive integers.

There are 75373 such numbers that do not exceed 10^7.
How many such numbers are there that do not exceed 2×10^9?

ANSWER: 11325263

Solve time ~5.6 seconds
"""
import numpy as np
from primesieve.numpy import primes  # much faster than primesieve.primes

import unittest
from util.utils import timeit, primes_of_n


# Extending the number field of the reals with a field extension of sqrt(D), n = a + b sqrt(D)
# such that Norm(a + b sqrt(D)) = a^2 - D×b^2
# Note that there are only the following negative D for which the resulting field is a principal ideal domain (PID)
# D = −1, −2, −3, −7, −11, −19, −43, −67, −163
# However only the field extensions of D = −1, −2, −3, −7, −11 are Euclidean domains.
# The remaining fields, D = −19, −43, −67, −163 are rare examples of PID's that are not Euclidean domains

# For reference: commutative rings ⊃ integral domains ⊃ integrally closed domains ⊃ GCD domains ⊃
# unique factorization domains (UFD) ⊃ principal ideal domains (PID) ⊃ Euclidean domains ⊃ fields ⊃ finite fields

# For reference: the only D's for which the field extension is a Euclidean domain are
# D = −11, -7, -3, -2, −1, 2, 3, 5, 6, 7, 11, 13, 17, 19, 21, 29, 33, 37, 41, 57, 73

# Using the Legendre symbol (-1/p) = {1 if p==1 mod 4, -1 if p==3 mod 4}
# In other words -1 has quadratic residues iff p == 1 mod 4,
# i.e. x^2 == -1 mod p has solutions for x iff p == 1 mod 4

# we can use legendre symbol arithmetic, (a/p)*(b/p) = (ab/p) to prove a lot more of these quadratic residues.
# We get:
# -1 has quadratic residues if p == 1 mod 4
# -2 has quadratic residues if p == 1,3 mod 8
# -3 has quadratic residues if p == 1 mod 3
# -7 has quadratic residues if p == 1,2,4 mod 7
# see here: https://en.wikipedia.org/wiki/Quadratic_residue

# Therefore if p == 1 mod 4 AND p == 1,3 mod 8 AND p == 1 mod 3 AND p == 1,2,4 mod 7
# then x^2 == -1, -2, -3, -7  mod p has a solution.

# RULES
# For D = -1:
# Ignore powers of 2. 3 mod 4 primes must be even power. 1 mod 4 primes must exist OR odd power of 2.

# For D = -2:
# Ignore powers of 2. 5,7 mod 8 primes must be even power. 1,3 mod 8 primes must exist.

# For D = -3:
# Ignore powers of 3. 2 mod 3 primes must be even power. 1 mod 3 primes must exist OR even power of 2.

# For D = -7:
# Ignore powers of 7. 3,5,6 mod 7 primes must be even power. 1,2,4 mod 7 primes must exist AND 2 cannot be raised to 1
# (if other primes exist). If only 2 exists then 2 cannot be raised to 1 or 2.

# The smallest value that satisfies all of these conditions is 193, which is a prime number.

# EXAMPLES
# 3600 = 2^4 3^2 5^2
# D = -1: 3 mod 4 is even power. 1 mod 4 prime exists.
# D = -2: 5 mod 8 is even power. 3 mod 8 prime exists.
# D = -3: 2 mod 3 is even power. 1 mod 3 prime does not exist, but even power of 2 does.
# D = -7: 3,5 mod 7 is even power. 2 mod 7 prime exists AND 2 is raised to the power greater than 1.

# 193 = 193
# D = -1: 193 mod 4 = 1.
# D = -2: 193 mod 8 = 1.
# D = -3: 193 mod 3 = 1.
# D = -7: 193 mod 7 = 4 and no single power of 2.

# Note that is a number satisfies these constraints then any square multiple of that number will also work.
# 193 * [all squares] are all in this form.
# 337 * [all squares] are all in this form.
# 457 * [all squares] are all in this form.
# this holds true for all primes of the 1,25,121 mod 168.
# since 8, 3, and 7 are all co-prime: 8*3*7 = 168

# the only cases that this doesn't cover are if the numbers are square.

# Looking at the full condition we get:
# [(1 mod 4)^(x>1) or 2^odd] AND (5,7 mod 8)^even AND (1,3 mod 8)^(x>1) AND (2 mod 3)^even
# AND [(1 mod 3)^(x>1) or 2^even] AND (3,5,6 mod 7)^even AND (1,2,4 mod 7)^(x>1) AND 2^(x!=1)

# Assuming our number is a square we get:
# [(1 mod 4)^(x>1)] AND (1,3 mod 8)^(x>1) AND [(1 mod 3)^(x>1) or 2^(x>1)] AND (1,2,4 mod 7)^(x>1)

# If x is a square, we can factor it and then test as in demonc post.
# If x is not a square, its squarefree part must consist of primes congruent to 1, 25 or 121 (mod 168),
# because p = 1, 3 (mod 8), p = 1 (mod 6) and p = 1, 9, 11 (mod 14).


class Problem229:
    def __init__(self, max_n):
        self.max_n = max_n
        self.count = 0

    @staticmethod
    def cond_d_1(dc_prime):  # Accurate!
        """Ignore powers of 2. 1 mod 4 primes must exist. 3 mod 4 primes must be even power."""
        # NOTE: THIS EXCLUDES 0, SO NO 2^2 + 0^2 = 4.
        # n is a sum of two squares iff it factors as n = ab^2, where a has no prime factor p ≡ 3 (mod 4)
        # 3 mod 4 primes must all be even powers
        if any([x % 2 != 0 for p, x in dc_prime.items() if p % 4 == 3]):
            return False
        # At least one 1mod4 prime must exist
        if sum([x % 4 == 1 for x in dc_prime.keys()]) == 0:
            # if at least one 1mod4 prime does not exist then the power of 2 must be odd
            # if 2 in dc_prime.keys():
            if dc_prime.get(2, 0) % 2 == 1:
                return True
            else:
                return False
        return True

    @staticmethod
    def cond_d_2(dc_prime):  # Accurate!
        # At least one (1/3) mod8 prime must exist
        if sum([x % 8 in [1, 3] for x in dc_prime.keys()]) == 0:
            return False
        # 0, 4, 6 can never be values of p%2 :
        if any([x % 2 != 0 for p, x in dc_prime.items() if p % 8 in [5, 7]]):
            return False
        return True

    @staticmethod
    def cond_d_3(dc_prime):  # Accurate!
        """Ignore powers of 3. 1 mod 3 primes must exist. 2 mod 3 primes must be even power."""
        # 2 mod 3 primes must all be even powers
        if any([x % 2 != 0 for p, x in dc_prime.items() if p % 3 == 2]):
            return False
        # At least one 1 mod3 prime must exist
        if sum([x % 3 == 1 for x in dc_prime.keys()]) == 0:
            # if at least one 1mod3 prime does not exist then the power of 2 must be even
            if 2 in dc_prime.keys():
                return True
            else:
                return False
        return True

    @staticmethod
    def cond_d_7(dc_prime):  # Accurate!
        # if divisible by 2 only once, then return False
        if dc_prime.get(2, 0) == 1:
            return False

        # 3/5/6 mod 7 primes must all be even powers
        if any([x % 2 != 0 for p, x in dc_prime.items() if p % 7 in [3, 5, 6]]):
            return False
        # At least one 1/2/4 mod7 prime must exist
        good_primes = [(p, x) for p, x in dc_prime.items() if p % 7 in [1, 2, 4]]
        if len(good_primes) == 0:
            return False
        if len(good_primes) == 1:
            if dc_prime.get(2, 0) in [1, 2]:
                return False

        return True

    @staticmethod
    def is_sq_rep_d_1(dc_prime):
        """
        Returns True or False is the square of the input can be represented at a^2 + 1*b^2 for a,b >0.
        Input is the prime factorization of the number.
        """
        # At least one 1mod4 prime must exist
        if sum([p % 4 == 1 for p in dc_prime.keys()]) == 0:
            return False
        return True

    @staticmethod
    def is_sq_rep_d_2(dc_prime):
        """
        Returns True or False is the square of the input can be represented at a^2 + 2*b^2 for a,b >0.
        Input is the prime factorization of the number.
        """
        # At least one (1/3) mod8 prime must exist
        if sum([p % 8 in [1, 3] for p in dc_prime.keys()]) == 0:
            return False
        return True

    @staticmethod
    def is_sq_rep_d_3(dc_prime):
        """
        Returns True or False is the square of the input can be represented at a^2 + 3*b^2 for a,b >0.
        Input is the prime factorization of the number.
        """
        # if divisible by 2
        if 2 in dc_prime.keys():
            return True
        # At least one 1 mod3 prime must exist
        if sum([x % 3 == 1 for x in dc_prime.keys()]) == 0:
            return False
        return True

    @staticmethod
    def is_sq_rep_d_7(dc_prime):
        """
        Returns True or False is the square of the input can be represented at a^2 + 7*b^2 for a,b >0.
        Input is the prime factorization of the number.
        """
        # At least one 1/2/4 mod7 prime must exist
        good_sum = sum([p % 7 in [1, 2, 4] for p in dc_prime.keys()])
        if good_sum == 0:
            return False
        if good_sum == 1:
            if dc_prime.get(2, 0) == 1:
                return False

        return True

    @staticmethod
    @timeit
    def get_ls_good_composite(max_n: int, ls_good_primes: list) -> list:
        """
        Compute a list of composite numbers consisting of two primes, less than max_n
        Args:
            max_n: max composite number
            ls_good_primes: list of primes to use

        Returns:

        """
        max_prime_of_2 = int(max_n / (ls_good_primes[0])) + 1
        prod_2 = [i for i in ls_good_primes if i <= max_prime_of_2]

        ls_good_composite = []
        sq_n = int(max_n ** 0.5)
        for i, p1 in enumerate(prod_2):
            if p1 > sq_n:
                break
            for p2 in prod_2[i + 1:]:
                c = p1 * p2
                if c > max_n:
                    break
                else:
                    ls_good_composite.append(c)
        return ls_good_composite

    @staticmethod
    @timeit
    def get_ls_good_composite_3_primes(max_n: int, ls_good_primes: list) -> list:
        """
        Compute a list of composite numbers consisting of three primes, less than max_n
        Args:
            max_n: max composite number
            ls_good_primes: list of primes to use

        Returns:

        """

        max_prime_of_3 = int(max_n / (ls_good_primes[0] * ls_good_primes[1])) + 1
        prod_3 = [i for i in ls_good_primes if i <= max_prime_of_3]

        ls_good_triple_comp = []
        for i, p1 in enumerate(prod_3):
            for j, p2 in enumerate(prod_3[i + 1:]):
                c2 = p1 * p2
                if c2 * prod_3[0] > max_n:
                    break
                for k, p3 in enumerate(prod_3[i + j + 2:]):
                    c3 = c2 * p3
                    if c3 > max_n:
                        break
                    else:
                        ls_good_triple_comp.append(c3)
        return ls_good_triple_comp

    @timeit
    def solve(self):
        print("generating primes")
        ls_primes = timeit(primes)(self.max_n)
        print("finished generating primes")  # 1.3 seconds
        # Note: 25^2 mod 168 = 121, 121^2 mod 168 = 25, 1^1 mod 168 = 1, 121*25 mod 168 = 1
        p_168 = ls_primes % 168  # using numpy arrays for speed
        ls_good_primes = (ls_primes[np.isin(p_168, [1, 25, 121])]).tolist()

        # generate all n = p_i * p_j, s.t. n <= max_n
        ls_good_comp = self.get_ls_good_composite(max_n=self.max_n, ls_good_primes=ls_good_primes)

        # generate all n = p_i * p_j * p_k, s.t. n <= max_n
        ls_good_triple_comp = self.get_ls_good_composite_3_primes(max_n=self.max_n, ls_good_primes=ls_good_primes)

        ls_good_nums = ls_good_primes + ls_good_comp + ls_good_triple_comp

        # adding the non-square numbers
        self.count += int(np.floor((self.max_n / np.array(ls_good_nums)) ** 0.5).sum())

        sq_n = int(self.max_n ** 0.5)
        for i in range(60, sq_n):  # first number that works is 60
            dc_prime = primes_of_n(i)
            cond = self.is_sq_rep_d_7(dc_prime)
            if cond:
                cond = cond and self.is_sq_rep_d_3(dc_prime)
            if cond:
                cond = cond and self.is_sq_rep_d_1(dc_prime)
            if cond:
                cond = cond and self.is_sq_rep_d_2(dc_prime)
            if cond:
                self.count += 1

        return self.count


class Solution229(unittest.TestCase):
    def setUp(self):
        # self.problem_small = Problem229(max_n=1000)
        # self.problem_small = Problem229(max_n=10000)
        # self.problem_small = Problem229(max_n=int(1e7))
        self.problem = Problem229(max_n=2 * int(1e9))

    def test_solution(self):
        # self.assertEqual(5, self.problem_small.solve())
        # self.assertEqual(96, self.problem_small.solve())
        # self.assertEqual(75373, self.problem_small.solve())  # 0.09 seconds
        self.assertEqual(11325263, self.problem.solve())  # 7 seconds


if __name__ == '__main__':
    unittest.main()

# balakrishnan_v comment
# I did not realise that this can be solved using brute force. So I found it a bit hard.
# First we look at the primes that are very special.
# The required primes are enumerated here .
# These are the set of primes that are 1,25,121 (mod) 168 . This is the set P .
# The set of all special numbers ≤ N can be split into the following 4 disjoint cases:
# 1)Numbers of the form k2 pi with pi ∈ P. The number of such numbers can be computed as
# ∑{p[sub]i ≤ N,pi  ∈  P}[/sub] floor(√ (N/pi))
# 2)Numbers of the form k2 pipj with pi < pj and pi,pj ∈ P. The number of such numbers can be computed as
# ∑{p[sub]i≤ √N,pi ∈ P}[/sub] ∑{p[sub]i<pj≤N/pi ,pj ∈ P}[/sub] floor( √(N/(pipj))
# 3)Numbers of the form k2 pipjpk with pi<pj<pk and pi,pj,pk ∈ P. The number of such numbers is
# ∑{p[sub]i≤N(1/3),pi ∈ P}[/sub] ∑{p[sub]i<pj≤√(N/pi) , pj ∈ P}[/sub] ∑{p[sub]j<pk≤(N/(pipj)),
# pk ∈ P}[/sub] floor( √(N/(pipjpk))
# P.S.: Note that numbers of the form pipjpkpl k2 does not exist in our case. This is because the smallest 4 primes
#  (193, 337, 457, 673) multiply to 20004075001 which is greater than 2*10^9 and hence need not be counted in this case.
# 4)Some of the square numbers(m2≤N). There are floor(√N) such square numbers. Each of them needs to be tested.
# This can be done either by brute force(since there are just √N~45000 of them) or more elegantly as follows:
#
# I:Test for x2+7y2
# M can be written in the form x2+7y2 with x>0 and y>0 iff in the prime-factorization M=2b7s{p1m1*p2m2...plml} *
# {q1n1*q2n2...qknk} (where pi are primes (3,5,6)(mod)7 and qi 's are odd primes which are 1,2,4(mod)7),
# the following are true:
# 1)All the mi 's are even
# 2)k>0 or b>=3 or both
# 3)b!=1
#
# Note that in our case, we don't need to check for (1) and (3) since M is already a square.
#
# II:Test for x2+3y2
# M can be written in the form x2+3y2 with x>0 and y>0  iff in the prime-factorization
# M=2b3s {p1m1*p2m2...plml} * {q1n1*q2n2...qknk} (where pi are odd primes (-1)(mod)3 and qi's are odd primes
# which are 1(mod)3), the following are true:
# 1)All the mi's are even
# 2)b+k>0
#
# Again we don't need to check for (1)
#
# III:Test for x2+2y2
# M can be written in the form x2+2y2 with x>0 and y>0  iff in the prime-factorization
# M=2b  {p1m1*p2m2...plml} * {q1n1*q2n2...qknk} (where pi are odd primes which are 5(mod)8 or 7(mod)8 and  qi's are
# odd primes which are 1(mod)8 or 3(mod)8), the following are true:
# 1)All the mi's are even
# 2)k>0
#
# Again, we don't need to check for (1).
#
# IV:Test for x2+y2
# This is well known. M can be written in the form x2+y2 with x>0 and y>0  iff in the prime-factorization M=2b
# {p1m1*p2m2...plml} * {q1n1*q2n2...qknk} (where pi are odd primes which are 3(mod)4 and qi's are odd primes
# which are 1(mod)4),  the following are true:
# 1)All the mi's are even
# 2)k>0 or b is odd or both
#
# Again, here too we don't need to check for condition (1) since M is a square. Also there is no need to check
# if b is odd(since b is already even), implying that k must be greater than 0.
#
# Thus for every integer M=i2≤ N, we first factorize the number and evaluate if the integer M comes under each of
#  the above 4 categories. If yes, then M is a required special number.
