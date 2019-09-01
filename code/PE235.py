"""
PROBLEM

Given is the arithmetic-geometric sequence u(k) = (900-3k)r^{k-1}.
Let s(n) = Σk=1...n u(k).

Find the value of r for which s(5000) = -600,000,000,000.

Give your answer rounded to 12 places behind the decimal point.

ANSWER: 1.002322108633, more precise: 1.00232210863287

Solve time ~ 0.003 seconds
"""

from util.utils import timeit
import unittest
import math


# Using:
# 1) sum_ k=1 to n of r^{k-1} = (r^n - 1) / (r-1)
# 2) sum_ k=1 to n of k*r^{k-1} = (n*r^{n+1} - (n+1)*r^n + 1) / (r-1)^2

# We can write s(n) = (-3*(n-300)*r^{n+1} + 3*(n-299)*r^n - 900*r + 897) / (r-1)^2
# plugging in n=5000 we get
# s(5000) = (-14100 * r^5001 + 14103 * r^5000 - 900 * r + 897)/(r - 1)^2

# Goal: solve for r such that
# (-14100 * r^5001 + 14103 * r^5000 - 900 * r + 897)/(r - 1)^2 = - 600,000,000,000
# (14100*r^5001 - 14103*r^5000 + 900*r - 897)/(r - 1)^2 = 600,000,000,000

# (4700*r^5001 - 4701*r^5000 + 300*r - 299)/(r - 1)^2 = 200,000,000,000  # divide by 3
# (r^5000 * (4700*r - 4700 -1) + 300*r - 300 + 1)/(r - 1)^2 = 200,000,000,000
# r^5000 * (4700*r - 4700 -1) /(r - 1)^2 + (300*r - 300 + 1)/(r - 1)^2 = 200,000,000,000
# 4700 * r^5000 /(r - 1) - r^5000 /(r - 1)^2 + 300/(r - 1) + 1/(r - 1)^2 = 200,000,000,000
# (4700 * r^5000 + 300) /(r - 1) + (1- r^5000)/(r - 1)^2 = 200,000,000,000


class Problem235:
    def __init__(self, limit, num_iter, low, high, precision):
        self.num_iter = num_iter
        self.limit = limit
        self.low = low
        self.high = high
        self.precision = precision

    @staticmethod
    def s(r):  # using limit/(-3)
        # (4700 * r ^ 5000 + 300) / (r - 1) + (1 - r ^ 5000) / (r - 1) ^ 2 = 200,000,000,000
        r_5000 = math.pow(r, 5000)
        r_1 = r-1
        return (4700 * r_5000 + 300) / r_1 + (1-r_5000) / math.pow(r_1, 2)

    @timeit
    def solve(self):
        lo, hi = self.low, self.high
        r = None
        for i in range(self.num_iter):
            r = (lo + hi) / 2.0
            val = self.s(r)
            lo, hi = (lo, r) if val > -self.limit/3 else (r, hi)
            # print(i, r, val)

        return round(r, self.precision)


class Solution235(unittest.TestCase):
    def setUp(self):
        self.problem = Problem235(limit=int(- 6*1e11), num_iter=40, low=1.0, high=1.1, precision=12)

    def test_solution(self):
        self.assertEqual(1.002322108633, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
