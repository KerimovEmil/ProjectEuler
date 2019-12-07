"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER:
???
Solve time ~ ??? seconds
"""

from util.utils import timeit, primes_of_n
import unittest
from primesieve import primes


def m3(n, ls_prime):
    if n == 1:
        return 1
    if n in ls_prime:
        return 1


def m2(n, ls_prime):
    i = 0
    p = ls_prime[i]
    num_prime = 0
    while p * p <= n:
        if n % p == 0:
            num_prime += 1
            n //= p
            if n % p == 0:
                return 0
        i += 1
        p = ls_prime[i]
    if n > 1:
        num_prime += 1
    if num_prime % 2 == 0:
        return 1
    else:
        return -1


def m(n, ls_primes):
    """
    μ(n) = 1 if n is square-free with an even number of prime factors.
    μ(n) = −1 if n is square-free with an odd number of prime factors.
    μ(n) = 0 if n has a squared prime factor.
    """
    dc_p = primes_of_n(n, ls_primes)
    if any(exp >= 2 for exp in dc_p.values()):
        return 0
    if len(dc_p.keys()) % 2 == 0:
        return 1
    else:
        return -1


class Problem193:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        ls_primes = primes(self.n**0.5)
        # ls_primes = None
        limit = self.n - 1
        count = 0
        for i in range(1, int(limit ** 0.5) + 1):
            # mobius = m(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            mobius = m2(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            count += mobius * (limit // (i ** 2))
        return count


class Solution193(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem193(n=int(2**50))
        self.problem = Problem193(n=int(2**36))

    def test_solution(self):
        self.assertEqual(41776432306, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
