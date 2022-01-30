"""
PROBLEM

The first known prime found to exceed one million digits was discovered in 1999,
and is a Mersenne prime of the form 2^6972593 − 1; it contains exactly 2,098,960 digits.
Subsequently other Mersenne primes, of the form 2^p − 1, have been found which contain more digits.

However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 28433×2^7830457 + 1.

Find the last ten digits of this prime number.

ANSWER: 8739992577
Solve time: ~0.004 seconds
"""
import unittest
from util.utils import timeit


class Problem97:
    """Find last n digits of k*2^(exp)+ 1  (Proth Prime)"""

    def __init__(self, last_num_digits, k, exp):
        self.modN = int(pow(10, last_num_digits))
        self.k = k
        self.exp = exp

    @timeit
    def solve(self):
        return (self.k * pow(2, self.exp, self.modN) + 1) % self.modN


class Solution97(unittest.TestCase):
    def setUp(self):
        # Find last 10 digits of 28433*2^(7830457)+ 1
        self.problem = Problem97(last_num_digits=10, k=28433, exp=7830457)

    def test_solution(self):
        self.assertEqual(8739992577, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
