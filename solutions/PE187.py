"""
PROBLEM

A composite is a number containing at least two prime factors. For example, 15 = 3 × 5; 9 = 3 × 3; 12 = 2 × 2 × 3.

There are ten composites below thirty containing precisely two, not necessarily distinct, prime factors:
4, 6, 9, 10, 14, 15, 21, 22, 25, 26.

How many composite integers, n < 10^8, have precisely two, not necessarily distinct, prime factors?
ANSWER: 17427258
Solve time: ~ 0.04 seconds
"""

import unittest
from util.utils import timeit, primes_upto, count_primes_upto


class Problem187:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        """pi(n/q) - pi(q) + 1 for all prime q not greater than sqrt(n)"""
        ls_p = primes_upto(self.n ** 0.5)

        count = 0
        for p in ls_p:
            count += count_primes_upto(self.n / p) - count_primes_upto(p) + 1

        return count


class Solution187(unittest.TestCase):
    def setUp(self):
        self.problem = Problem187(n=int(1e8))

    def test_solution(self):
        self.assertEqual(17427258, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
