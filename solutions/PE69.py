"""
PROBLEM

Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine the number of numbers less
than n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively
prime to nine, φ(9)=6.

ANSWER:
510510
Solve time ~0.002 seconds
"""
from util.utils import timeit, sieve
import unittest

# Note that you can show that phi(n) = n*(1-1/p1)*(1-1/p2)*... for all of the prime factors of n
# Therefore the maximum of n / phi(n) = max 1/((1-1/p1)*(1-1/p2)*...) = min((1-1/p1)*(1-1/p2)*...)
# = n with the most prime factors that is less than the limit of 1,000,000


class Problem69:
    def __init__(self, limit, max_prime=100):
        self.limit = limit
        self.primes = sieve(max_prime)

    @timeit
    def solve(self):
        output = 1
        for p in self.primes:
            output *= p
            if output > self.limit:
                return output/p
        raise ValueError("Max Prime is not large enough")


class Solution69(unittest.TestCase):
    def setUp(self):
        limit = 1000000
        self.problem = Problem69(limit)

    def test_solution(self):
        self.assertEqual(510510, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
