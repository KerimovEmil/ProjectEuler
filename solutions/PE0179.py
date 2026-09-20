"""
PROBLEM

Find the number of integers 1 < n < 10^7, for which n and n + 1 have the same number of positive divisors.
For example, 14 has the positive divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15.

ANSWER: 986262
Solve time: ~18 seconds
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

        # fixing the number of divisors for 0 and 1
        divisors[0] = 0
        divisors[1] = 1

        for i in range(2, int(self.n ** 0.5) + 1):
            # i2 = i * i
            # divisors[i2] -= 1  # remove one divisor for each square number
            # for x in range(i2, self.n, i):
            #     divisors[x] += 2  # add the two divisors of i and n/i

            divisors[i * i] += 1  # add one divisor for each square number
            for k in range(i + 1, self.n // i + 1):
                divisors[k*i] += 2  # add the two divisors of i and n/i
        return sum(divisors[i] == divisors[i - 1] for i in range(3, self.n))


class Solution179(unittest.TestCase):
    def setUp(self):
        self.problem = Problem179(n=int(1e7))

    def test_solution(self):
        self.assertEqual(986262, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
