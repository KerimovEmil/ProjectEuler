"""
PROBLEM

For a positive number N, find the sum of all x such that 1 < x < N and x^3 ≡ 1 mod N.

For example, for N = 91, the 8 solutions are 9, 16, 22, 29, 53, 74, 79, 81, and their sum is 363.
Find the sum of all such x for N = 13082761331670030.

ANSWER: 4617456485273129588
Solve time: ~0.002 seconds
"""

import itertools
import math
import unittest
from typing import List
from util.utils import timeit
from util.crt import ChineseRemainderTheoremSets


# MATHEMATICAL DERIVATION:
#
# 1. Problem Formulation:
#    We are seeking the sum of all integers x in (1, N) such that:
#      x^3 = 1 (mod N)
#    where N = 13082761331670030.
#
# 2. Prime Factorization of N:
#    N is square-free and equals the product of the first 14 primes (the 14th primorial p_14#):
#      N = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43
#
# 3. Chinese Remainder Theorem (CRT) Decomposition:
#    Because N is a product of pairwise coprime primes, solving x^3 = 1 (mod N) is equivalent
#    to simultaneously solving:
#      x^3 = 1 (mod p_i)   for each prime factor p_i of N.
#
# 4. Roots of Unity Modulo Primes:
#    For any prime p, the multiplicative group (Z / pZ)* is cyclic of order p - 1.
#    The number of solutions to x^3 = 1 (mod p) is gcd(3, p - 1):
#      - If p = 1 (mod 3): gcd(3, p - 1) = 3, yielding 3 distinct roots in [1, p - 1].
#        The prime factors of N with p = 1 (mod 3) are:
#          7  --> {1, 2, 4}
#          13 --> {1, 3, 9}
#          19 --> {1, 7, 11}
#          31 --> {1, 5, 25}
#          37 --> {1, 10, 26}
#          43 --> {1, 6, 36}
#        There are exactly 6 such primes.
#      - If p != 1 (mod 3): gcd(3, p - 1) = 1, so x = 1 is the unique solution.
#        The remaining 8 prime factors {2, 3, 5, 11, 17, 23, 29, 41} each contribute only {1}.
#
# 5. Total Solutions & Summation:
#    The total number of solutions in [1, N] is:
#      3^6 * 1^8 = 729 solutions.
#    Exactly one solution is x = 1. The problem requests the sum over 1 < x < N (the other 728 solutions).
#
#    For each residue combination (a_1, ..., a_14), the unique solution mod N is obtained by CRT:
#      x = sum_{i=1}^{14} a_i * M_i * (M_i^(-1) mod p_i)   (mod N)
#    where M_i = N // p_i.


class Problem271:
    def __init__(self, primes: List[int] = None):
        if primes is None:
            self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
        else:
            self.primes = primes

    @timeit
    def solve(self, primes: List[int] = None) -> int:
        if primes is None:
            primes = self.primes

        n_val = math.prod(primes)

        # Find modular cube roots of 1 for each prime factor
        roots_per_p = []
        for p in primes:
            roots = [x for x in range(1, p) if (x * x * x) % p == 1]
            roots_per_p.append(roots)

        # Precompute CRT basis weights: w_i = (N // p_i) * ((N // p_i)^(-1) mod p_i)
        weights = []
        for p in primes:
            m_i = n_val // p
            inv_i = pow(m_i, -1, p)
            weights.append(m_i * inv_i)

        # Sum all CRT combinations satisfying 1 < x < N
        total_sum = 0
        for combination in itertools.product(*roots_per_p):
            x = sum(a * w for a, w in zip(combination, weights)) % n_val
            if 1 < x < n_val:
                total_sum += x

        return total_sum


class Solution271(unittest.TestCase):
    def setUp(self):
        self.problem = Problem271()

    def test_example(self):
        # Example N = 91 = 7 * 13
        self.assertEqual(363, self.problem.solve(primes=[7, 13]))

    def test_solution(self):
        self.assertEqual(4617456485273129588, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
