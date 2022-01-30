"""
PROBLEM

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?

ANSWER:
6857
Solve time ~ 0.001 seconds
"""

import unittest
from util.utils import timeit, primes_of_n


class Problem3:
    def __init__(self, num):
        self.num = num

    @timeit
    def solve(self):
        pf = primes_of_n(self.num).keys()
        return max(pf)


class Solution3(unittest.TestCase):
    def setUp(self):
        self.problem = Problem3(600851475143)

    def test_solution(self):
        self.assertEqual(6857, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
