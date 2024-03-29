"""
PROBLEM

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

ANSWER: 232792560
Solve time: ~0.003 seconds
"""

from collections import defaultdict

import unittest
from util.utils import timeit, primes_of_n


class Problem5:
    def __init__(self, nums):
        self.nums = nums

    @staticmethod
    def lcm_factors(nums):
        min_factors = defaultdict(int)
        for n in nums:
            pfs = primes_of_n(n)
            for k, v in pfs.items():
                min_factors[k] = max(min_factors[k], v)

        return min_factors

    @staticmethod
    def lcm(nums):
        fs = Problem5.lcm_factors(nums)
        n = 1

        for k, v in fs.items():
            n *= k ** v

        return n

    @timeit
    def solve(self):
        return self.lcm(self.nums)


class Solution5(unittest.TestCase):
    def setUp(self):
        self.problem = Problem5(list(range(2, 21)))

    def test_solution(self):
        self.assertEqual(232792560, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
