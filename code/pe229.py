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

ANSWER:

Solve time ~  seconds
"""

from util.utils import timeit, primes_of_n, sieve
import unittest


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

# Note through all of this we assumed p was an odd prime.

# RULES
# For D = -1:
# Ignore powers of 2. 3 mod 4 primes must be even power. 1 mod 4 primes must exist OR odd power of 2.

# For D = -2:
# Ignore powers of 2. 5,7 mod 8 primes must be even power. 1,3 mod 8 primes must exist.

# For D = -3:
# Ignore powers of 3. 2 mod 3 primes must be even power. 1 mod 3 primes must exist OR even power of 2.

# For D = -7:
# Ignore powers of 7. 3,5,6 mod 7 primes must be even power. 1,2,4 mod 7 primes must exist AND 2 cannot be raised to 1.

# The smallest value that satisfies all of these conditions is 193, which is a prime number.

# EXAMPLES # TODO: redo all examples.
# Example 3600: Divide out all of the powers of 2 and we get: 3600/16 = 225.
# 225 mod 4 = 1, 225 mod 8 = 1, 225 mod 7 = 1
# 225 mod 3 = 0 is a special case since 3 divides 225, and the legendre symbol arithmetic assumes they are coprime

# Example 88201:
# 88201 % 4 = 1, 88201 % 3 = 1, 88201 % 8 = 1, 88201 % 7 = 1

# 3600 = 2^4 3^2 5^2 works
# 1800 = 2^3 3^2 5^2 fails for d = 3
# 900 = 2^2 3^2 5^2 fails for d = 7
# 450 = 2 3^2 5^2 fails for d = 3 and 7
# 225 = 3^2 5^2 fails for d = 3 and 7
# 75 = 3 5^2 fails for d = 1, 3 and 7
# 25 = 5^2 fails for d = 2, 3 and 7

# 1200 = 2^4 3 5^2 fails for d = 1 and 7
# 400 = 2^4 5^2 fails for d = 2
# 200 = 2^3 5^2 fails for d = 2 and 3
# 100 = 2^2 5^2 fails for d = 2 and 7
# 50 = 2^1 5^2 fails for d = 2, 3 and 7


class Problem229:
    def __init__(self, max_n):
        self.max_n = max_n
        self.count = 0

    @staticmethod
    def legendre_neg1(n):
        if n % 4 == 1:
            return 1
        elif n % 4 == 3:
            return -1
        else:
            return 0

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
        if sum([x % 8 in [1, 3] for x in dc_prime.keys()]) < 1:
            return False
        # 0, 4, 6 can never be values of p%2 :
        # if any([x % 2 != 0 for p, x in dc_prime.items() if p % 8 in [0, 4, 5, 6, 7]]):
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
        # 3/5/6 mod 7 primes must all be even powers
        if any([x % 2 != 0 for p, x in dc_prime.items() if p % 7 in [3, 5, 6]]):
            return False
        # At least one 1/2/4 mod7 prime must exist
        good_primes = [(p, x) for p, x in dc_prime.items() if p % 7 in [1, 2, 4]]
        if len(good_primes) == 0:
            return False
        if len(good_primes) == 1:
            if good_primes[0][0] == 2:
                if good_primes[0][1] < 3:
                    return False
        ls_2 = [(p, x) for p, x in good_primes if p == 2]
        if len(ls_2) == 1:
            if ls_2[0][1] == 1:
                return False
        return True

    @timeit
    def solve(self):
        ls_primes = list(sieve(self.max_n))
        for i in range(2, self.max_n + 1):
            dc_prime = primes_of_n(i, ls_primes)
            # highest_multiple_of_2 = i & -i  # bitwise operation

            # # k = i // highest_multiple_of_2
            # k = i
            #
            # cond1 = k % 4 == 1  # not needed
            #
            # cond2 = k % 8 == 1
            # # cond3 = (i % 3 == 1) or i % 3 == 0
            # cond3 = (k % 3 == 1)
            # # cond4 = (i % 7 == 1) or i % 7 == 0
            # cond4 = (k % 7 == 1)
            cond = True
            if cond:
                cond = cond and self.cond_d_7(dc_prime)
            if cond:
                cond = cond and self.cond_d_3(dc_prime)
            if cond:
                cond = cond and self.cond_d_1(dc_prime)
            if cond:
                cond = cond and self.cond_d_2(dc_prime)

            if cond:
                self.count += 1
                print("Running count is: {}. With new number: {}".format(self.count, i))
        return self.count

    @staticmethod
    def g1(n, ls_sq):
        s = set()
        for a2 in ls_sq:
            for b2 in ls_sq:
                t = a2 + b2
                if t > n:
                    break
                else:
                    s.add(t)
        return s

    @staticmethod
    def g2(n, ls_sq):
        s = set()
        for a2 in ls_sq:
            for b2 in ls_sq:
                t = a2 + 2 * b2
                if t > n:
                    break
                else:
                    s.add(t)
        return s

    @staticmethod
    def g3(n, ls_sq):
        s = set()
        for a2 in ls_sq:
            for b2 in ls_sq:
                t = a2 + 3 * b2
                if t > n:
                    break
                else:
                    s.add(t)
        return s

    @staticmethod
    def g7(n, ls_sq):
        s = set()
        for a2 in ls_sq:
            for b2 in ls_sq:
                t = a2 + 7 * b2
                if t > n:
                    break
                else:
                    s.add(t)
        return s

    @timeit
    def solve_dumb(self):
        ls_sq = [x**2 for x in range(1, self.max_n)]
        s1 = self.g1(self.max_n, ls_sq)
        s2 = self.g2(self.max_n, ls_sq)
        s3 = self.g3(self.max_n, ls_sq)
        s4 = self.g7(self.max_n, ls_sq)
        full_s = s1.intersection(s2).intersection(s3).intersection(s4)
        return len(full_s)


class Solution229(unittest.TestCase):
    def setUp(self):
        # self.problem_small = Problem229(max_n=1000)
        self.problem_small = Problem229(max_n=int(1e7))
        # self.problem = Problem229(max_n=2*int(1e9))

    def test_solution(self):
        # self.assertEqual(5, self.problem_small.solve())
        self.assertEqual(75373, self.problem_small.solve())  # takes 11 mins to run
        # self.assertEqual(None, self.problem.solve())  # not done yet

    def test_solution_dumb(self):
        # self.assertEqual(5, self.problem_small.solve_dumb())
        self.assertEqual(75373, self.problem_small.solve_dumb())  # takes 27 seconds to run


if __name__ == '__main__':
    unittest.main()
