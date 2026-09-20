"""
PROBLEM

Let f(N) be the number of points with integer coordinates that are on a circle passing
through (0,0), (N,0),(0,N), and (N,N).

It can be shown that f(10000) = 36.

What is the sum of all positive integers N ≤ 10^11 such that f(N) = 420 ?

ANSWER: 271204031455541309
Solve time: ~2.5 seconds
"""

import unittest
from util.utils import timeit, primes_upto


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
# 1) 2* N^2 must have exactly 3 primes of 1 mod 4, with exponents 2,4,6. (420/4 = 105 = 3*5*7)
# This implies that N must exactly 3 primes of 1 mod 4, with exponents 1,2,3.
# Note if only 2 prime factors made up the 105 multiples then N would be bigger than 10^11, since
# 5**10 * 13**10 = 1346274334462890625

# Since there is an infinite amount of ways to construct this, we must use the 2nd condition in the problem
# 2) N ≤ 10^11

# Note the first few primes with 1 mod 4 are 5, 13, 17, 29, 37, 41, 53, ...
# therefore the smallest possible N would be 5^3 * 13^2 * 17^1 = 359125

# For each combination we need to also count multiples of every other prime number that keep N below 10^11.

# The largest prime that can be cubed is 521, since 5^2 * 13^1 * 677^3 = 100843838225
# The largest prime that can be squared is 5521, since 5^3 * 13^1 * 7853^2 = 100213114625
# The largest prime that can be raised to the 1st power is 2366809, since 5^3 * 13^2 * 4733753^1 = 100000532125.


class Problem233:

    def __init__(self, n):
        self.n = n
        self.ans_sum = 0
        self.available_multiples = None
        self.ls_1mod4_primes = None

    def calculate_options(self, chosen_n):
        limit = self.n // chosen_n

        mult_sum = 0
        for mult in self.available_multiples:
            if mult > limit:
                break
            else:
                mult_sum += mult

        self.ans_sum += chosen_n * mult_sum

    def calc(self, opt, test_num=1, ls_prime=None):

        if ls_prime is None:
            ls_prime = []

        if len(opt) > 0 and opt[0] != 0:
            for prime in self.ls_1mod4_primes:
                if prime not in ls_prime:
                    ls_new_prime = ls_prime + [prime]
                    new_test_num = test_num * prime ** opt[0]
                    if new_test_num > self.n:
                        break
                    self.calc(opt[1:], new_test_num, ls_new_prime)
        else:
            self.calculate_options(test_num)

    @staticmethod
    def compute(vals, pows):
        base = 1
        for (b, e) in zip(vals, pows):
            base *= b ** e
        return base

    def find_max_good(self, true_opts, mins):
        gg = []
        for opt in true_opts:
            val = Problem233.compute(mins, opt[:-1])
            gg.append(val)
        return int(self.n / min(gg)) + 1

    def generate_ls_all_possible_multiples(self, largest_3mod4_prime, debug=False):
        """
        Args:
            largest_3mod4_prime: largest 3mod4 prime to consider
            debug: <bool> to print logging or not
        Returns: a set of all possible multiples
        """

        all_multiples = set(range(largest_3mod4_prime))
        if debug:
            print("{} is the number of available multiples".format(len(all_multiples)))

        # Get list of ALL numbers which are not multiples of 1mod4 primes
        for prime in self.ls_1mod4_primes:
            num = prime
            while num < largest_3mod4_prime:
                all_multiples.discard(num)
                num += prime

        if debug:
            print("{} is the number of available multiples left".format(len(all_multiples)))

        return all_multiples

    @timeit
    def solve(self, debug=False):
        opts = [(3, 2, 1), (7, 3), (10, 2), (52,), (17, 1)]
        mins = (5, 13, 17)

        # filter the options by the minimum possible factor being less than N
        true_opts = [x for x in opts if Problem233.compute(mins, x) <= self.n]
        if debug:
            print("{} are the only possible (1 mod 4) prime powers.".format(true_opts))

        # Compute the largest 3 mod 4 prime to consider
        min_factor_option = min([Problem233.compute(mins, x) for x in true_opts])
        largest_3mod4_prime = int(self.n / min_factor_option) + 1
        if debug:
            print("Largest 3mod4 prime to consider is: {}".format(largest_3mod4_prime))

        # Compute the largest 1 mod 4 prime to consider
        largest_1mod4_prime = self.find_max_good(true_opts, mins)
        if debug:
            print("Largest 1mod4 prime to consider is: {}".format(largest_1mod4_prime))

        # Generate list of primes
        available_primes = primes_upto(max(largest_1mod4_prime, largest_3mod4_prime))

        # Filter to get the list of relevant 1mod4 primes
        self.ls_1mod4_primes = [x for x in available_primes if Problem233.is_1mod4(x) and x <= largest_1mod4_prime]

        self.available_multiples = self.generate_ls_all_possible_multiples(largest_3mod4_prime, debug)
        self.available_multiples = sorted(self.available_multiples)  # to ensure the order

        if debug:
            print('Starting looping over every combination')
        for opt in true_opts:
            self.calc(opt)
        return self.ans_sum

    @staticmethod
    def is_1mod4(prime):
        return prime % 4 == 1


class Solution233(unittest.TestCase):
    def setUp(self):
        self.small_problem = Problem233(n=38000000)
        self.problem = Problem233(n=int(1e11))

    def test_small_solution(self):
        self.assertEqual(30875234922, self.small_problem.solve())

    def test_solution(self):
        self.assertEqual(271204031455541309, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
