"""
PROBLEM

Find the number of integers 1 < n < 107, for which n and n + 1 have the same number of positive divisors.
For example, 14 has the positive divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15.

ANSWER: 986262

Solve time ~19 seconds
"""

import unittest
from util.utils import timeit


class Problem179:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        """Create a sieve of divisors"""
        divisors = [2] * (self.n + 1)  # every number is divisible by itself and 1.
        # The number of divisors for 1 is incorrect but we don't use it anyway
        for i in range(2, int(self.n ** 0.5) + 1):
            i2 = i * i
            divisors[i2] -= 1  # remove one divisor for each square number
            for x in range(i2, self.n, i):
                divisors[x] += 2  # add the two divisors of i and n/i
        return sum(divisors[i] == divisors[i - 1] for i in range(3, self.n))


class Solution179(unittest.TestCase):
    def setUp(self):
        self.problem = Problem179(n=int(1e7))

    def test_solution(self):
        self.assertEqual(102093, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
