"""
Consider quadratic Diophantine equations of the form:

x^2 – Dy^2 = 1

For example, when D=13, the minimal solution in x is 649^2 – 13×180^2 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

3^2 – 2×2^2 = 1
2^2 – 3×1^2 = 1
9^2 – 5×4^2 = 1
5^2 – 6×2^2 = 1
8^2 – 7×3^2 = 1

Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.

Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.

ANSWER: 661
Solve time: ~0.093 seconds
"""

import math
import unittest
from util.utils import timeit, pell_fundamental_solution


class Problem66:
    def __init__(self, max_d):
        self.max_d = max_d
        self.max_min_x = 0
        self.d_max_min_x = None

    @timeit
    def solve(self):
        for d in range(2, self.max_d + 1):
            r = math.isqrt(d)
            if r * r == d:
                continue

            sol = pell_fundamental_solution(d)
            if sol is not None:
                x = sol[0]
                if x > self.max_min_x:
                    self.max_min_x = x
                    self.d_max_min_x = d

        return self.d_max_min_x



class Solution66(unittest.TestCase):
    def setUp(self):
        self.problem = Problem66(1000)

    def test_solution(self):
        self.assertEqual(661, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
