"""
PROBLEM

We shall call a positive integer "A" an "Alexandrian integer", if there exist integers a,b,c such that:

A = a*b*c
and
1/A = 1/a + 1/b + 1/c

For example, 630 is an Alexandrian integer (a=5, b=-7, c=-18). In fact, 630 is the
6th Alexandrian integer, the first 6 Alexandrian integers being: 6,42,120,156,420, and 630.

Find the 150000th Alexandrian integer

ANSWER:
Solve time:
"""
from util.utils import timeit, is_int
import unittest

# a*b + b*c + a*c = 1
# (a+b+c)^2 = a^2 + b^2 + c^2 + 2
# (a+b+c)^3 = a^3 + b^3 + c^3 + 3 (a^2 b + a^2 c + a b^2 + a c^2 + b^2 c + b c^2) + 6 a b c
# (a+b+c)^3 = a^3 + b^3 + c^3 + 3 (a*(ab + ac) + b*(ab + bc) + c*(ac + bc)) + 6 a b c
# (a+b+c)^3 = a^3 + b^3 + c^3 + 3 (a*(ab + ac + bc) - abc + b*(ab + bc + ac) - abc + c*(ac + bc + ab) - abc) + 6 a b c
# (a+b+c)^3 = a^3 + b^3 + c^3 + 3 (a + b + c - 3*abc) + 6abc
# (a+b+c)^3 = a^3 + b^3 + c^3 + 3*(a + b + c) - 3abc
# 3abc = a^3 + b^3 + c^3 + 3*(a+b+c) - (a+b+c)^3

# wlog let |a| >= |b| >= |c|
# fix k, k*b + b*c + k*c = 1
# k*(b+c) = 1 - b*c
# k = (1 - b*c) / (b+c)


class Problem221:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        ls_sol = []

        def check(x, y, z):
            if y == -z:
                return False
            return x == (1 - y*z) / (y+z)

        def add(x, y, z):
            p = x*y*z
            print(f'{p=}, {x=}, {y=}, {z=}, {len(ls_sol)=}')
            ls_sol.append(p)

        a = 1
        while len(ls_sol) < 2*self.n:
            a += 1
            for b in range(1, a + 1):
                for c in range(1, b + 1):
                    a_neg, b_neg, c_neg = -a, -b, -c
                    if check(a_neg, b, c_neg):
                        add(a_neg, b, c_neg)
                    elif check(a_neg, b_neg, c):
                        add(a_neg, b_neg, c)
                    elif check(a, b_neg, c_neg):
                        add(a, b_neg, c_neg)
        ls_sol.sort()
        print(ls_sol)
        return ls_sol[self.n - 1]


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem221(n=150_000)

    def test_small_solution(self):
        self.assertEqual(630, Problem221(n=6).solve())

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

