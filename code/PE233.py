"""
PROBLEM

Let f(N) be the number of points with integer coordinates that are on a circle passing
through (0,0), (N,0),(0,N), and (N,N).

It can be shown that f(10000) = 36.

What is the sum of all positive integers N ≤ 10^11 such that f(N) = 420 ?

ANSWER:

Solve time ~  seconds
"""

from util.utils import timeit
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
# 1) N must be even
# 2) N must have exactly 3 primes of 1 mod 4, with exponents 2,4,6. (420/4 = 105 = 3*5*7)

# Since there is an infinite amount of ways to construct this, we must use the 3rd condition in the problem
# 3) N ≤ 10^11

class Problem233:
    def __init__(self, n, limit):
        self.n = n
        self.limit = limit

    @timeit
    def solve(self):
        if self.n % 4 == 0:
            pass
        else:
            return 0


class Solution1(unittest.TestCase):
    def setUp(self):
        self.problem = Problem233(n=420, limit=int(1e11))

    # def test_solution(self):
        # self.assertEqual(420, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
