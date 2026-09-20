"""
PROBLEM

A positive fraction whose numerator is less than its denominator is called a proper fraction.
For any denominator, d, there will be d−1 proper fractions; for example, with d = 12:
1/12 , 2/12 , 3/12 , 4/12 , 5/12 , 6/12 , 7/12 , 8/12 , 9/12 , 10/12 , 11/12 .

We shall call a fraction that cannot be cancelled down a resilient fraction.
Furthermore we shall define the resilience of a denominator, R(d), to be the ratio of its proper fractions
that are resilient; for example, R(12) = 4/11 .
In fact, d = 12 is the smallest denominator having a resilience R(d) < 4/10 .

Find the smallest denominator d, having a resilience R(d) < 15499/94744 .

ANSWER: 892371480
Solve time: ~0.003 seconds
"""

# note that this problem and problem 69 both require the Euler totient function
# https://en.wikipedia.org/wiki/Euler%27s_totient_function


import unittest
from util.utils import timeit, primes_upto


# The number of fractions with a denominator d that cannot get simplified is equal to the euler totient function of d,
# since that is the same as the number of numbers below d that d is co-prime with.

# You can show that phi(d) = d*(1-1/p1)*(1-1/p2)*... for all of the prime factors of d
# therefore R(d) = d/(d-1) *(1-1/p1)*(1-1/p2)*... for all of the prime factors of d
# Note that d/(d-1) is always > 1. Therefore for R(d) < 15499/94744, it implies that (1-1/p1)*(1-1/p2)*... < 15499/94744
# Note that we get more impact from smaller primes for the second term

# EXAMPLE (limit=4/10)
# example with d=12 and limit = 4/10 = 0.4
# (1-1/2)*(1-1/3) = 1/3 < 0.4
# 0.4 / (1/3) = 1.2 > d/(d-1)
#  d*0.2 > 1.2
#  d > 6
# therefore d has primes 2 and 3, and is greater than 6, the smallest number that satisfies this is d=12

# SOLUTION (limit=15499/94744)
# (1-1/2)*(1-1/3)*(1-1/5)*...*(1-1/23) = 0.16358819535559344 < 15499/94744
# therefore d > 2*3*5*7*11*13*17*19*23 = 223092870
# However multiplying by d/(d-1) brings R(d) slightly below the 15499/94744 limit

# 15499/94744 / 0.16358819535559344 = 1.000000001240703 > d /(d-1)
# d * 0.000000001240703 > 1.000000001240703
# d > 805994666.9
# d >= 805994667

# 223092870*4 = 892371480 > 805994667
# and d = 892371480 has R(d) = 0.16358819553891188 < 15499/94744 = 0.1635881955585578


# See code below to codify this logic


class Problem243:
    def __init__(self, limit, max_prime=100):
        self.limit = limit
        self.primes = primes_upto(max_prime)

    @timeit
    def solve(self):
        output = 1
        n = 1
        for p in self.primes:
            output *= (1 - 1 / p)
            n *= p
            if output < self.limit:
                break

        # find bound on d using d/(d-1) * output < limit, rearranging
        # d < limit/output *(d)  - limit/output
        # limit/output < (limit/output - 1) * d
        # d > limit/output / (limit/output - 1) = lower_bound
        ratio = self.limit / output
        lower_bound = ratio / (ratio - 1)
        # take the ceiling of the ratio from all of the primes to the lower bound to get the scalar required
        scalar = int(lower_bound / n) + 1
        return n * scalar


class Solution243(unittest.TestCase):
    def setUp(self):
        self.problem = Problem243(limit=15499 / 94744)

    def test_solution(self):
        self.assertEqual(892371480, self.problem.solve())

    def test_sample_solution(self):
        small_problem = Problem243(limit=4 / 10)
        self.assertEqual(12, small_problem.solve())


if __name__ == '__main__':
    unittest.main()
