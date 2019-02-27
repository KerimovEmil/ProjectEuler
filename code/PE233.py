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
# f(N) = length of the set such that {a^2 + b^2 = N^2/2 for a,b integers}

# We can use this to quickly count f(N).
# After we factor N, we first ignore all of the primes which are 3 mod 4 (and 2). The remainder are primes which are a
# multiplication of 2 Gaussian primes. After we square the number we double the exponents on these prime factors.
# Remember we are looking for two conjugate Gaussian integers which multiply to give us N^2. It is equivalent to
# finding the number of factors of N^2.

# Example: N = 10,000 = 2^4 * 5^4.
# N^2/2 = 2^7 * 5^8
# only looking at the primes 1 mod 4, we have 5^8.
# there are (1+8) choices of factors, and we multiply by 4 for the 4 possible rotations (1,-1,i,-i)
# hence f(10,000) = 9*4 = 36

# therefore N such that f(N) = 420 implies that
# 1) N must be even. Otherwise N^2/2 is not an integer.  # todo, on second thought, I don't think this is true.
# 2) N^2 must have exactly 3 primes of 1 mod 4, with exponents 2,4,6. (420/4 = 105 = 3*5*7)
# This implies that N must exactly 3 primes of 1 mod 4, with exponents 1,2,3.
# Note if only 2 prime factors made up the 105 multiples then N would be bigger than 10^11, since
# 5**10 * 13**10 = 1346274334462890625

# Since there is an infinite amount of ways to construct this, we must use the 3rd condition in the problem
# 3) N ≤ 10^11

# Note the first few primes with 1 mod 4 are 5, 13, 17, 29, 37, 41, 53, ...
# therefore the smallest possible N would be 2 * 5^3 * 13^2 * 17^1 = 718250
# The largest possible prime 1 mod 4 to consider would be 2366809 since 2 * 5^3 * 13^2 * 2366809^1 = 99997680250

# There are only 86929 primes less then or equal to 2366809 which are 1 mod 4.
# For each combination we need to also count multiples of every other prime number that keep N below 10^11.

# The largest prime that can be cubed is 521, since 2 * 5^2 * 13^1 * 521^3 = 91923494650
# The largest prime that can be squared is 5521, since 2 * 5^3 * 13^1 * 5521^2 = 99064683250
# The largest prime that can be raised to the 1st power is 2366809, since 2 * 5^3 * 13^2 * 2366809^1 = 99997680250.

MAX = 38000000


class Problem233:
    def __init__(self):
        pass

    @staticmethod
    def calculate_options(chosen_n, sub_options, sofar):
        if not len(sub_options):
            return
        # N^2 is getting factored into squares, not N -> we only need `head`, not `head^2`
        head = sub_options[0]
        new_chosen_n = head * chosen_n
        if (new_chosen_n <= MAX):
            sofar.add(new_chosen_n)
            # grow the chosen n using head more times if desired
            Problem233.calculate_options(new_chosen_n, sub_options, sofar)
        # grow the chosen n without using head at all, and only using other factors
        Problem233.calculate_options(chosen_n, sub_options[1:], sofar)

    @staticmethod
    def calc(pow, good_primes, prev=1):
        for a in good_primes:
            if (a ** pow) * prev > MAX:
                break
            yield a

    @staticmethod
    def calc3(opt, good_primes, bad_primes, sofar):
        for a in good_primes:
            if (a ** opt[0]) > MAX:
                break
            for b in good_primes:
                if (a ** opt[0] * b ** opt[1]) > MAX:
                    break
                if (a != b):
                    for c in good_primes:
                        if (b != c and a != c):
                            if (a ** opt[0] * b ** opt[1] * c * opt[2]) > MAX:
                                break

                            chosen_n = Problem233.compute((a, b, c), opt)
                            if chosen_n <= MAX:
                                sofar.add(chosen_n)
                                Problem233.calculate_options(
                                    chosen_n, bad_primes, sofar)

    @staticmethod
    def calc2(opt, good_primes, bad_primes, sofar):
        for a in good_primes:
            if (a ** opt[0]) > MAX:
                break
            for b in good_primes:
                if (a ** opt[0] * b ** opt[1]) > MAX:
                    break
                if (a != b):
                    chosen_n = Problem233.compute((a, b), opt)
                    if chosen_n <= MAX:
                        sofar.add(chosen_n)
                        Problem233.calculate_options(
                            chosen_n, bad_primes, sofar)

    @staticmethod
    def compute(vals, pows):
        base = 1
        for (b, e) in zip(vals, pows):
            base *= b ** e
        return base

    @timeit
    def solve(self):
        opts = [(3, 2, 1), (7, 3), (10, 2), (52,), (17, 1)]
        mins = (5, 13, 17)
        true_opts = [x for x in opts if Problem233.compute(mins, x) <= MAX]
        print(true_opts)

        min_option = min([Problem233.compute(mins, x) for x in true_opts])
        max_option = int(MAX / min_option) + 1
        # super_max = int(MAX ** 0.5) + 1
        # trying to figure out the largest max that we could have
        super_max = int(MAX/5/5/5/13/13)

        available_primes = list(sieve(super_max))
        good_primes = [x for x in available_primes if Problem233.is_1mod4(x)]
        bad_primes = [
            x for x in available_primes if x <= max_option and not Problem233.is_1mod4(x)]

        sofar = set()
        for opt in true_opts:
            if len(opt) == 2:
                Problem233.calc2(opt, good_primes, bad_primes, sofar)
            if len(opt) == 3:
                Problem233.calc3(opt, good_primes, bad_primes, sofar)
        return sum(sofar)

    @staticmethod
    def is_1mod4(prime):
        return prime % 4 == 1


class Solution1(unittest.TestCase):
    def setUp(self):
        self.problem = Problem233()

    def test_solution(self):
        self.assertEqual(30875234922, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
