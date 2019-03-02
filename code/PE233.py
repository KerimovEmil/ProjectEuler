"""
PROBLEM

Let f(N) be the number of points with integer coordinates that are on a circle passing
through (0,0), (N,0),(0,N), and (N,N).

It can be shown that f(10000) = 36.

What is the sum of all positive integers N ≤ 10^11 such that f(N) = 420 ?

ANSWER: 271204031455541309

Solve time ~9 seconds
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

    def calculate_options(self, chosen_n, sub_options, sofar):
        for opt in sub_options:
            new_chosen_n = opt * chosen_n
            if new_chosen_n > self.n:
                break
            else:
                sofar.add(new_chosen_n)

    def calc3(self, opt, good_primes, bad_primes, sofar):
        for a in good_primes:
            if (a ** opt[0]) > self.n:
                break
            for b in good_primes:
                if (a ** opt[0] * b ** opt[1]) > self.n:
                    break
                if (a != b):
                    for c in good_primes:
                        if (b != c and a != c):
                            if (a ** opt[0] * b ** opt[1] * c ** opt[2]) > self.n:
                                break

                            chosen_n = Problem233.compute((a, b, c), opt)
                            if chosen_n <= self.n:
                                sofar.add(chosen_n)
                                self.calculate_options(chosen_n, bad_primes, sofar)

    def calc2(self, opt, good_primes, bad_primes, sofar):
        for a in good_primes:
            if (a ** opt[0]) > self.n:
                break
            for b in good_primes:
                if (a ** opt[0] * b ** opt[1]) > self.n:
                    break
                if (a != b):
                    chosen_n = Problem233.compute((a, b), opt)
                    if chosen_n <= self.n:
                        sofar.add(chosen_n)
                        self.calculate_options(chosen_n, bad_primes, sofar)

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

    @timeit
    def solve(self):
        opts = [(3, 2, 1), (7, 3), (10, 2), (52,), (17, 1)]
        mins = (5, 13, 17)
        true_opts = [x for x in opts if Problem233.compute(mins, x) <= self.n]
        print("{} are the only possible (1 mod 4) prime powers.".format(true_opts))

        min_good_option = min([Problem233.compute(mins, x) for x in true_opts])
        max_bad_prime = int(self.n / min_good_option) + 1
        max_good_prime = self.find_max_good(true_opts, mins)
        print(max_bad_prime, max_good_prime)

        available_primes = list(sieve(max(max_good_prime, max_bad_prime)))

        mod4_1_primes = [x for x in available_primes if Problem233.is_1mod4(x)]
        good_primes = [x for x in mod4_1_primes if x <= max_good_prime]

        mod4_1_primes = set(mod4_1_primes)

        really_bad_nums = set(range(max_bad_prime))
        print("{} is the number of (2/3 mod 4) prime candidates".format(len(really_bad_nums)))

        # TODO: explain what this is doing and how it works
        for factor in mod4_1_primes:
            num = factor
            while True:
                really_bad_nums.discard(num)
                num += factor
                if num > max_bad_prime:
                    break

        print("{} is the number of (2/3 mod 4) prime candidates left".format(len(really_bad_nums)))

        print('starting calc')
        sofar = set()
        for opt in true_opts:
            if len(opt) == 2:
                # todo: why not just make opt[2] = 0, that way you don't need two functions?
                self.calc2(opt, good_primes, really_bad_nums, sofar)
                print('done calc2 for ', opt)
            if len(opt) == 3:
                self.calc3(opt, good_primes, really_bad_nums, sofar)
                print('done calc3 for ', opt)
        return sum(sofar)

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
