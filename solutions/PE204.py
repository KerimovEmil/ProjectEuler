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
Solve time ~0.6 seconds
"""

import math

from primesieve import primes

import unittest
from util.utils import timeit


# Idea is as follows: (from user Assato in https://projecteuler.net/thread=204;page=2)
# Define hamming(N,b) returns how many numbers below N are primes(b)-smooth.
# note that the number of 2-smooth numbers N are: floor(log(N) / log(2)) + 1
# therefore hamming(N, 2) = floor(log(N) / log(2)) + 1

# Looking at hamming(N,7). There are two types of 7-smooth numbers:
# (i) those that are actually 5-smooth = hamming(N, 5)
# (ii) those that contains at least one factor 7 = ?

# The key to realize is that (ii) is  hamming(N/7 , 7).
# This is true because hamming(N/7,7) contains ALL 7-smooth values until N/7 (those that contains the factor 7 and
# those who don't). By multiplying each of them by 7, we'll get each and every 7-smooth number under a that contains
# at least one 7 factor.

# therefore hamming(N,7) = hamming(N,5) + hamming(N/7, 7)

# example:
# hamming(100, 5) = hamming(100, 3) + hamming(20, 5)

# hamming(100, 3) = hamming(100, 2) + hamming(33, 3) = hamming(100, 2) + hamming(33, 2) + hamming(11, 3)
#                 = hamming(100, 2) + hamming(33, 2) + hamming(11, 2) + hamming(3, 3)
#                 = ceil(log(100)/log(2)) + ceil(log(33)/log(2)) + ceil(log(11)/log(2)) + 3
#                 = 7 + 6 + 4 + 3
#                 = 20

# hamming(20, 5) = hamming(20, 3) + hamming(4, 5)
#                = hamming(20, 2) + hamming(6, 3) + 4
#                = hamming(20, 2) + hamming(6, 2) + hamming(2, 3) + 4
#                = ceil(log(20)/log(2)) + ceil(log(6)/log(2)) + 2 + 4
#                = 5 + 3 + 2 + 4
#                = 14

# therefore hamming(100, 5) = hamming(100, 3) + hamming(20, 5) = 20 + 14 = 34


class Problem204:
    def __init__(self, hamming, limit):
        self.hamming = hamming
        self.limit = limit

    @timeit
    def solve(self):
        """From user: Assato"""
        ls_prime = primes(self.hamming)[::-1]

        def recursive_count(n, ls_dec_primes):
            """
            n: total limit to consider
            ls_dec_primes: list of decreasing primes to consider.

            returns how many numbers below N are primes(b)-smooth.
            e.g. hamming(N,7) = hamming(N,5) + hamming(N/7, 7)
            """
            p = ls_dec_primes[0]
            if p == 2:
                return int(math.log2(n)) + 1
            if n <= p:
                return n
            return recursive_count(n, ls_dec_primes[1:]) + recursive_count(n // p, ls_dec_primes)

        return recursive_count(self.limit, ls_prime)

    @timeit
    def simple_recursive_solve(self):  # slower solution
        ls_prime = primes(self.hamming)

        def count(primeindex, product):
            if primeindex == len(ls_prime):
                return product <= self.limit
            else:
                result = 0
                while product <= self.limit:
                    result += count(primeindex + 1, product)
                    product *= ls_prime[primeindex]
                return result

        return count(0, 1)


class Solution204(unittest.TestCase):

    def test_solution_small(self):
        self.assertEqual(1105, Problem204(hamming=5, limit=int(1e8)).solve())

    def test_solution(self):
        self.assertEqual(2944730, Problem204(hamming=100, limit=int(1e9)).solve())

    def test_solution_small_simple(self):
        self.assertEqual(1105, Problem204(hamming=5, limit=int(1e8)).simple_recursive_solve())


if __name__ == '__main__':
    unittest.main()
