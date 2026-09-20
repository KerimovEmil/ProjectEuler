"""
PROBLEM

Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a != b, then a and b are an amicable pair and each of a and b are called amicable
numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110 therefore d(220) = 284.
The proper divisors of 284 are 1, 2, 4, 71 and 142 so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.

ANSWER: 31626
Solve time: ~0.018 seconds
"""

import unittest
from util.utils import timeit, primes_of_n, num_of_divisors


class Problem21:
    def __init__(self, limit):
        self.limit = limit

    @timeit
    def solve(self):
        sum_proper = [0] * self.limit
        for i in range(1, self.limit):
            for j in range(2 * i, self.limit, i):
                sum_proper[j] += i

        amicable = 0
        for a in range(1, self.limit):
            b = sum_proper[a]
            if b < self.limit and b != a and sum_proper[b] == a:
                amicable += a
        return amicable


class Solution21(unittest.TestCase):
    def setUp(self):
        self.problem = Problem21(10000)

    def test_solution(self):
        self.assertEqual(31626, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
