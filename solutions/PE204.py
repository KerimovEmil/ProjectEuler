"""
PROBLEM

A Hamming number is a positive number which has no prime factor larger than 5.
So the first few Hamming numbers are 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15.
There are 1105 Hamming numbers not exceeding 10^8.

We will call a positive number a generalised Hamming number of type n, if it has no prime factor larger than n.
Hence the Hamming numbers are the generalised Hamming numbers of type 5.

How many generalised Hamming numbers of type 100 are there which don't exceed 10^9?

ANSWER:
2944730
Solve time ~11 seconds
"""

from util.utils import timeit
import unittest
from primesieve import count_primes, primes
import math


class Problem204:
    def __init__(self, hamming, limit):
        self.hamming = hamming
        self.limit = limit

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')

    @timeit
    def simple_recursive_solve(self):
        ls_prime = primes(self.hamming)
        LIMIT = self.limit

        def count(primeindex, product):
            if primeindex == len(ls_prime):
                return 1 if product <= LIMIT else 0
            else:
                result = 0
                while product <= LIMIT:
                    result += count(primeindex + 1, product)
                    product *= ls_prime[primeindex]
                return result

        return count(0, 1)


class Solution204(unittest.TestCase):
    # def setUp(self):
    #     self.problem = Problem204()

    # def test_solution_small(self):
    #     self.assertEqual(1105, Problem204(hamming=5, limit=int(1e8)).solve())

    def test_solution_small_simple(self):
        self.assertEqual(1105, Problem204(hamming=5, limit=int(1e8)).simple_recursive_solve())

    def test_solution_simple(self):
        self.assertEqual(2944730, Problem204(hamming=100, limit=int(1e9)).simple_recursive_solve())


if __name__ == '__main__':
    unittest.main()
