"""
PROBLEM

Given is the arithmetic-geometric sequence u(k) = (900-3k)r^{k-1}.
Let s(n) = Σk=1...n u(k).

Find the value of r for which s(5000) = -600,000,000,000.

Give your answer rounded to 12 places behind the decimal point.

ANSWER:

Solve time ~  seconds
"""

from util.utils import timeit
import unittest


# Using:
# 1) sum_ k=1 to n of r^{k-1} = (r^n - 1) / (r-1)
# 2) sum_ k=1 to n of k*r^{k-1} = (n*r^{n+1} - (n+1)*r^n + 1) / (r-1)^2

# We can write s(n) = (-3*(n-300)*r^{n+1} + 3*(n-299)*r^n - 900*r + 897) / (r-1)^2
# plugging in n=5000 we get
# s(5000) = (-14100 * r^5001 + 14103 * r^5000 - 900 * r + 897)/(r - 1)^2

# Goal: solve for r such that
# (-14100 * r^5001 + 14103 * r^5000 - 900 * r + 897)/(r - 1)^2 = - 600,000,000,000
# (14100*r^5001 - 14103*r^5000 + 900*r - 897)/(r - 1)^2 = 600,000,000,000


class Problem235:
    def __init__(self, n, limit):
        self.n = n
        self.limit = limit

    @timeit
    def solve(self):
        pass
#
# class Solution1(unittest.TestCase):
#     def setUp(self):
#         self.problem = Problem235(n=420, limit=int(1e11))

    # def test_solution(self):
        # self.assertEqual(420, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
