"""
PROBLEM

Let f(N) be the number of points with integer coordinates that are on a circle passing
through (0,0), (N,0),(0,N), and (N,N).

It can be shown that f(10000) = 36.

What is the sum of all positive integers N ≤ 10^11 such that f(N) = 420 ?

ANSWER:

Solve time ~  seconds
"""

from util.utils import timeit, sieve
import unittest


# Examining f(N)
# Define G(N) = number of lattice points on circle with radius sqrt(N)
# We will show that G(N) is equal to f(N).

# G(N) is equal to the length of the set such that {a^2 + b^2 = N^2 for a,b integers}
# allowing ourselves to go into Gaussian integers we can write this as
# G(N) = length of {(a+i*b)*(a-i*b) = N^2 for a,b integers}
# idea: we need to count how many ways we can factor N^2 using Gaussian integers
# point: just like in normal integers prime factorization is unique up to a multiple of -1, in Gaussian integers
# prime factorization is unique up to a multiple of i, -i, 1, -1. Hence we will multiply our result by 4.

# important point, all primes which are 1 mod 4 factor exactly into 2 Gaussian primes, all primes which are 3 mod 4
# do not factor into Gaussian primes. Note that 2 does factor into (1+i) and (1-i) but those are not unique up to a
# multiple of i, so they won't really matter for the counting of G(N). This is why G(N) = f(N) (for even N) since
# f(N) = length of the set such that {a^2 + b^2 = 2*N^2 for a,b integers}. The reason it is 2*N^2 is due to the
# inscribed angle in a half circle is always 90 degrees.

# We can use this to quickly count f(N).
# After we factor N, we first ignore all of the primes which are 3 mod 4 (and 2). The remainder are primes which are a
# multiplication of 2 Gaussian primes. After we square the number we double the exponents on these prime factors.
# Remember we are looking for two conjugate Gaussian integers which multiply to give us 2*N^2. It is equivalent to
# finding the number of factors of N^2.

# Example: N = 10,000 = 2^4 * 5^4.
# 2*N^2 = 2^9 * 5^8
# only looking at the primes 1 mod 4, we have 5^8.
# there are (1+8) choices of factors, and we multiply by 4 for the 4 possible rotations (1,-1,i,-i)
# hence f(10,000) = 9*4 = 36

# therefore N such that f(N) = 420 implies that
# 1) N^2 must have exactly 3 primes of 1 mod 4, with exponents 2,4,6. (420/4 = 105 = 3*5*7)
# This implies that N must exactly 3 primes of 1 mod 4, with exponents 1,2,3.
# Note if only 2 prime factors made up the 105 multiples then N would be bigger than 10^11, since
# 5**10 * 13**10 = 1346274334462890625

# Since there is an infinite amount of ways to construct this, we must use the 2nd condition in the problem
# 2) N ≤ 10^11

# Note the first few primes with 1 mod 4 are 5, 13, 17, 29, 37, 41, 53, ...
# therefore the smallest possible N would be 5^3 * 13^2 * 17^1 = 718250

# For each combination we need to also count multiples of every other prime number that keep N below 10^11.

# The largest prime that can be cubed is 521, since 5^2 * 13^1 * 677^3 = 100843838225
# The largest prime that can be squared is 5521, since 5^3 * 13^1 * 7853^2 = 100213114625
# The largest prime that can be raised to the 1st power is 2366809, since 5^3 * 13^2 * 4733753^1 = 100000532125.


class Problem233:
    def __init__(self):
        pass

    @staticmethod
    def calculate_options(chosen_n, sub_options, sofar):
        if not len(sub_options):
            return sofar
        # head = sub_options[0] ** 2
        head = sub_options[0]
        new_chosen_n = head * chosen_n
        if (new_chosen_n <= 1e11):
            sofar.add(new_chosen_n)
            # grow the chosen n using head more times if desired
            Problem233.calculate_options(new_chosen_n, sub_options, sofar)
        # grow the chosen n without using head at all, and only using other factors
        Problem233.calculate_options(chosen_n, sub_options[1:], sofar)

    @staticmethod
    def get_variants(p1, p2, p3, others, options):
        n_max = 1e11
        # chosen_n = 2 * (p1 ** 1) * (p2 ** 2) * (p3 ** 3)
        chosen_n = (p1 ** 1) * (p2 ** 2) * (p3 ** 3)
        # max multiplicative limit
        limit = n_max / chosen_n
        sub_others = [x for x in others if x <= limit]

        # fac_2 = 0
        fac_2 = 1
        while True:
            cn = (2 ** fac_2) * chosen_n
            if cn > n_max:
                break
            else:
                options.add(cn)
                Problem233.calculate_options(cn, sub_others, options)
                fac_2 += 1

    @staticmethod
    def compute_numbers(p1s, p2s, p3s, others):
        options = set()
        for p3 in p3s:
            for p2 in p2s:
                if (2 * p3 ** 3 * p2 ** 2) > 1e11:
                    break
                if (p2 == p3):
                    continue

                for p1 in p1s:
                    # if (2 * p3 ** 3 * p2 ** 2 * p1 ** 1) > 1e11:
                    if (p3 ** 3 * p2 ** 2 * p1 ** 1) > 1e11:
                        break
                    if (p1 == p2):
                        continue
                    if (p1 == p3):
                        continue

                    Problem233.get_variants(p1, p2, p3, others, options)
        return sum(options)

    @timeit
    def solve(self):
        max_p1 = 4733753
        max_p2 = 7853
        max_p3 = 677

        available_primes = sieve(max_p1)
        modded_primes = [x for x in available_primes if Problem233.is_1mod4(x)]

        p1s = [x for x in modded_primes if x < max_p1]
        p2s = [x for x in modded_primes if x < max_p2]
        p3s = [x for x in modded_primes if x < max_p3]
        # for multiplying by even powers of primes
        others = [x for x in sieve(400) if Problem233.is_3mod4(x)]

        return self.compute_numbers(p1s, p2s, p3s, others)

    @staticmethod
    def is_1mod4(prime):
        return prime % 4 == 1

    @staticmethod
    def is_3mod4(prime):
        return prime % 4 == 3


class Solution1(unittest.TestCase):
    def setUp(self):
        self.problem = Problem233()

    def test_solution(self):
        self.assertEqual(0, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
