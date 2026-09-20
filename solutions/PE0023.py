"""
PROBLEM

A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the
sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum
exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of
two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be
written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even
though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than
this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.

ANSWER: 4179871
Solve time: ~0.26 seconds
"""

import unittest
from util.utils import timeit


class Problem23:
    def __init__(self, limit):
        self.limit = limit

    @timeit
    def solve(self):
        sum_proper = [0] * (self.limit + 1)
        for i in range(1, self.limit + 1):
            for j in range(2 * i, self.limit + 1, i):
                sum_proper[j] += i

        abundant = [i for i in range(12, self.limit + 1) if sum_proper[i] > i]

        can_sum = [False] * (self.limit + 1)
        for i, a in enumerate(abundant):
            for b in abundant[i:]:
                s = a + b
                if s > self.limit:
                    break
                can_sum[s] = True

        return sum(i for i in range(1, self.limit + 1) if not can_sum[i])


class Solution23(unittest.TestCase):
    def setUp(self):
        self.problem = Problem23(28123)

    def test_solution(self):
        self.assertEqual(4179871, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
