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

Solve time ~231 seconds
"""

from util.utils import timeit, primes_of_n, sieve
import unittest
import primesieve


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

# Therefore
# 193 * [all squares] are all in this form.
# 337 * [all squares] are all in this form.
# 457 * [all squares] are all in this form.
# this holds true for all primes of the 1,25,121 mod 168


# Solving with some of the mandatory conditions.
# 3 mod 4 primes must be even power and 5,7 mod 8 primes must be even power
# and 2 mod 3 primes must be even power and 3,5,6 mod 7 primes must be even power

# Notice that 3 mod 4 primes must be even power is a weaker condition than 7 mod 8 primes must be even power.
# therefore we can eliminate that condition:

# 5,7 mod 8 primes must be even power
# and 2 mod 3 primes must be even power and 3,5,6 mod 7 primes must be even power

# since 8, 3, and 7 are all co-prime: 8*3*7 = 168
# (5 or 7) * 2 * (3 or 5 or 6) mod 168 must be an even power.
# i.e. 30, 42, 50, 60, 70, 84 mod 168 must be an even power

# [(1 mod 4)^(x>1) or 2^odd] AND (5,7 mod 8)^even AND (1,3 mod 8)^(x>1) AND (2 mod 3)^even
# AND [(1 mod 3)^(x>1) or 2^even] AND (3,5,6 mod 7)^even AND (1,2,4 mod 7)^(x>1) AND 2^(x!=1)

# Expanding the or's:
# (1 mod 4)^(x>1) AND (5,7 mod 8)^even AND (1,3 mod 8)^(x>1) AND (2 mod 3)^even
# AND (1 mod 3)^(x>1) AND (3,5,6 mod 7)^even AND (1,2,4 mod 7)^(x>1) AND 2^(x!=1)
# OR
# (1 mod 4)^(x>1) AND (5,7 mod 8)^even AND (1,3 mod 8)^(x>1) AND (2 mod 3)^even
# AND (2^even) AND (3,5,6 mod 7)^even AND (1,2,4 mod 7)^(x>1) AND 2^(x!=1)
# OR
# (2^odd) AND (5,7 mod 8)^even AND (1,3 mod 8)^(x>1) AND (2 mod 3)^even
# AND (1 mod 3)^(x>1) AND (3,5,6 mod 7)^even AND (1,2,4 mod 7)^(x>1) AND 2^(x!=1)

# if number to consider is already a square then the criteria simplifies to:
# (1 mod 4)^(x>1) AND (1,3 mod 8)^(x>1) AND (1 mod 3)^(x>1) AND (1,2,4 mod 7)^(x>1)
# OR
# (1 mod 4)^(x>1) AND (1,3 mod 8)^(x>1) AND (2^even) AND (1,2,4 mod 7)^(x>1)

# expanding
# if number to consider is already a square then the criteria simplifies to:
# (1 mod 8)^(x>1) AND (1 mod 3)^(x>1) AND (1,2,4 mod 7)^(x>1)
# OR
# (1 mod 4)^(x>1) AND (3 mod 8)^(x>1) AND (1 mod 3)^(x>1) AND (1,2,4 mod 7)^(x>1)
# OR
# (1 mod 8)^(x>1) AND (2^even) AND (1,2,4 mod 7)^(x>1)
# OR
# (1 mod 4)^(x>1) AND (3 mod 8)^(x>1) AND (2^even) AND (1,2,4 mod 7)^(x>1)


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

    @timeit
    def solve(self):
        # ls_primes = list(sieve(self.max_n))
        # ls_primes = sieve(self.max_n)
        print("generating primes")
        ls_primes = primesieve.primes(self.max_n)
        print("finsihed generating primes")
        ls_good_primes = [p for p in ls_primes if p % 168 in [1, 25, 121]]  # 1 = 1^2, 25=5^2, 121=11^2
        # Note: 25^2 mod 168 = 121, 121^2 mod 168 = 25, 1^1 mod 168 = 1, 121*25 mod 168 = 1

        # [i for i in range(1, 168) if i**2 % 168 in [1,25,121]]
        # [1, 5, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41, 43, 47, 53, 55, 59, 61, 65, 67, 71, 73, 79, 83, 85, 89,
        # 95, 97, 101, 103, 107, 109, 113, 115, 121, 125, 127, 131, 137, 139, 143, 145, 149, 151, 155, 157, 163, 167]

        # # todo: add base of 4624 = 2**4 * 17**2 and 3600 = 2^4 3^2 5^2
        # # todo fix this, this slightly over-counts the result.
        # ls_good_primes.append(3600)  # 2^4 3^2 5^2
        # ls_good_primes.append(4624)  # 2^4 17^2 (* 2^2
        # ls_good_primes.append(12100)  # 2^2 5^2 11^2  (* 2^2
        # ls_good_primes.append(12321)  # 3^2 37^2  (* 2^2
        # ls_good_primes.append(75076)  # 2^2 137^2

        ls_good_primes.sort()
        # todo: include all possible multiplications of good_primes within each other
        print("finished adding good primes")

        ls_good_comp = []
        sq_n = int(self.max_n**0.5)
        for i, p1 in enumerate(ls_good_primes):
            if p1 > sq_n:
                break
            # for p2 in ls_good_primes[i:]:
            for p2 in ls_good_primes[i+1:]:
                # for p3 in [1] +  # todo add another loop p1*p2 or p1*p2*p3
                c = p1*p2
                if c > self.max_n:
                    break
                else:
                    ls_good_comp.append(c)

        # ls_good_nums = ls_good_comp + ls_good_primes

        print("finished adding composites p1*p2")

        max_prime_of_3 = int(self.max_n / (193 * 337)) + 1
        prod_3 = [i for i in ls_good_primes if i <= max_prime_of_3]

        ls_good_triple_comp = []  # 187 choose 3
        for i, p1 in enumerate(prod_3):
            for j, p2 in enumerate(prod_3[i+1:]):
                c2 = p1 * p2
                if c2*190 > self.max_n:  # 190 < 193 first prime
                    break
                for k, p3 in enumerate(prod_3[i+j+2:]):
                    c3 = c2*p3
                    if c3 > self.max_n:
                        break
                    else:
                        ls_good_triple_comp.append(c3)

        ls_good_nums = ls_good_primes + ls_good_comp + ls_good_triple_comp
        print("finished adding composites p1*p2*p3")

        # todo include
        # 20449= 11^2 13^2  # 11^2 13^2 mod 168 = 121*1 mod 168 = 121  # 13^2 * 11^2
        # 24336= 2^4 3^2 13^2  # 13^2 mod 168 = 1  13^2 * 12^2
        # 26896= 41^2 2^4  # 41^2 mod 168 = 1
        # 30276= 2^2 3^2 29^2  # 29^2 mod 168 = 1
        # 46225= 43^2 5^2  # 43^2 mod 168 = 1
        # 51076= 113^2 2^2  # 113^2 mod 168 = 1
        # 81796= 2^2 11^2 13^2  # 121 * 1 mod 168 = 121
        # 85264= 73^2 2^4  # 73^2 mod 168 = 121
        # 97344= 2^6 3^2 13^2  # 13^2 mod 168 = 1

        # adding the non-square numbers
        for p in ls_good_nums:
            max_possible_sq = self.max_n / p
            max_count = int(max_possible_sq**0.5)

            self.count += max_count
        print("Finished adding the non square numbers. {} numbers.".format(self.count))
        for sq in [i**2 for i in range(2, sq_n)]:
            cond = True
            if cond:
                # dc_prime = primes_of_n(sq, ls_primes)
                dc_prime = primes_of_n(sq)
                cond = cond and self.cond_d_7(dc_prime)
            if cond:
                cond = cond and self.cond_d_3(dc_prime)
            if cond:
                cond = cond and self.cond_d_1(dc_prime)
            if cond:
                cond = cond and self.cond_d_2(dc_prime)

            if cond:
                self.count += 1
                print("Running count is: {}. With new number: {}".format(self.count, sq))

        return self.count

    @timeit
    def solve_basic(self):
        ls_primes = list(sieve(self.max_n))
        for i in range(2, self.max_n + 1):
            # dc_prime = primes_of_n(i, ls_primes)
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
            cond = (i & -i) != 2
            # cond = True
            if cond:
                dc_prime = primes_of_n(i, ls_primes)
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
    def gx(n, ls_sq, x):
        s = set()
        for a2 in ls_sq:
            for b2 in ls_sq:
                t = a2 + x*b2
                if t > n:
                    break
                else:
                    s.add(t)
        return s

    @timeit
    def solve_dumb(self):
        ls_sq = [x**2 for x in range(1, self.max_n)]
        s1 = self.gx(self.max_n, ls_sq, 1)
        s2 = self.gx(self.max_n, ls_sq, 2)
        s3 = self.gx(self.max_n, ls_sq, 3)
        s4 = self.gx(self.max_n, ls_sq, 7)
        full_s = s1.intersection(s2).intersection(s3).intersection(s4)
        return len(full_s)


class Solution229(unittest.TestCase):
    def setUp(self):
        # self.problem_small = Problem229(max_n=1000)
        # self.problem_small = Problem229(max_n=10000)
        # self.problem_small = Problem229(max_n=int(1e7))
        self.problem = Problem229(max_n=2*int(1e9))
        # s = list(range(np1)): MemoryError

    def test_solution(self):
        # self.assertEqual(5, self.problem_small.solve())
        # self.assertEqual(96, self.problem_small.solve())
        # self.assertEqual(75373, self.problem_small.solve())  # takes 1 second to run. 74960 != 75373.
        self.assertEqual(11325263, self.problem.solve())  # 3 mins 50 seconds

    # def test_solution_dumb(self):
        # self.assertEqual(5, self.problem_small.solve_dumb())
        # self.assertEqual(96, self.problem_small.solve_dumb())
        # self.assertEqual(75373, self.problem_small.solve_dumb())  # takes 27 seconds to run
        # self.assertEqual(1, self.problem.solve_dumb())  #


if __name__ == '__main__':
    unittest.main()

# todo include
# 3600 = 2^4 3^2 5^2  # 5^2 mod 168 = 25
# 4624 = 2^4 17^2  # 17^2 mod 168 = 121 (extra 2^4)
# 12100 = 2^2 11^2 5^2  # 11^2 * 5^2 mod 168 = 121 * 25 mod 168 = 1  (extra 2^2)
# 12321 = 3^2 37^2  # 37^2 mod 168 = 25 (extra 3^2)
# 14400= 2^6 3^2 5^2  # 5^2 mod 168 = 25 (3600 * 2^2)
# 18496= 2^6 17^2  # 17^2 mod 168 = 121 (extra 2^6)
# 20449= 11^2 13^2  # 11^2 13^2 mod 168 = 121*1 mod 168 = 121
# 24336= 2^4 3^2 13^2  # 13^2 mod 168 = 1
# 26896= 41^2 2^4  # 41^2 mod 168 = 1
# 30276= 2^2 3^2 29^2  # 29^2 mod 168 = 1
# 32400= 2^4 3^4 5^2  # 5^2 mod 168 = 25  (3600 * 3^2)
# 37249= 193^2  # 193^2 mod 168 = 121
# 41616= 2^4 3^2 17^2  # 17^2 mod 168 = 121
# 46225= 43^2 5^2  # 43^2 mod 168 = 1
# 48400= 2^4 11^2 5^2  # 11^2 mod 168 = 121
# 49284= 2^2 3^2 37^2  # 37^2 mod 168 = 25
# 51076= 113^2 2^2  # 113^2 mod 168 = 1
# 57600= 2^8 3^2 5^2  # 5^2 mod 168 = 25 (3600 * 4^2)
# 65041= 193^1 337^1  25 * 1 mod 168 = 25
# 73984= 2^8 17^2  # 17^2 mod 168 = 121
# 75076= 137^2 2^2  # 137^2 mod 168 = 121
# 81796= 2^2 11^2 13^2  # 121 * 1 mod 168 = 121
# 85264= 73^2 2^4  # 73^2 mod 168 = 121
# 88201= 193^1 457^1  # 25*121 mod 168 = 1
# 90000= 2^4 3^2 5^4  # 5^4 mod 168 = 121
# 97344= 2^6 3^2 13^2  # 13^2 mod 168 = 1


#
# N = int(1e7)
# ls_sq = [x ** 2 for x in range(1, N)]
# s1 = gx(N, ls_sq, 1)
# s2 = gx(N, ls_sq, 2)
# s3 = gx(N, ls_sq, 3)
# s4 = gx(N, ls_sq, 7)
# full_s = s1.intersection(s2).intersection(s3).intersection(s4)
#
# def sieve(n):
#     """Return all primes <= n."""
#     np1 = n + 1
#     s = list(range(np1))
#     s[1] = 0
#     sqrtn = int(round(n ** 0.5))
#     for i in range(2, sqrtn + 1):
#         if s[i]:
#             s[i * i: np1: i] = [0] * len(range(i * i, np1, i))
#     return filter(None, s)
# ls_primes = list(sieve(N))
# ls_good_primes = [p for p in ls_primes if p % 168 in [1, 25, 121]]
# ls_good_primes.append(3600)
# ls_good_primes.append(4624)
# ls_good_primes.sort()
# ls_good_comp = []
# sq_n = int(N ** 0.5)
# for i, p1 in enumerate(ls_good_primes):
#     if p1 > sq_n:
#         break
#     for p2 in ls_good_primes[i:]:
#         c = p1 * p2
#         if c > N:
#             break
#         else:
#             ls_good_comp.append(c)
# ls_good_nums = ls_good_comp + ls_good_primes
#
# GOOD = set()
# for p in ls_good_nums:
#     max_possible_sq = N / p
#     max_count = int(max_possible_sq ** 0.5)
#     for i in range(1, max_count + 1):
#         GOOD.add(p * (i ** 2))
# print(GOOD - full_s)
# X = list(full_s - GOOD)
# X.sort()


# 11323675 + [(187 choose 3) = 1072445] +
# 11323675 + 187*186*185 / (3*2) +
# 11323675 + 187* (187 choose 2)
