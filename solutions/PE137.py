"""
PROBLEM

Consider the infinite polynomial series A(x)=xF_1+x^2 F_2 + x^3 F_3+…, where Fk is the kth term in the Fibonacci
sequence: 1,1,2,3,5,8,…; that is, F_{k}=F_{k−1}+F_{k−2}, F_1=1 and F_2=1.

For this problem we shall be interested in values of x for which AF(x) is a positive integer.

Surprisingly A(1/2)=2

We shall call A(x) a golden nugget if x is rational, because they become increasingly rarer; for example,
the 10th golden nugget is 74049690.

Find the 15th golden nugget.

ANSWER: 1120149658760
Solve time ~0.001 seconds
"""
import unittest
from solutions.PE140 import Problem140
from util.utils import timeit


# A(x) = x / (1 - x - x^2)

# set A(x) = k, for k some integer
# A(x) = k = x / (1 - x - x^2)
# k(1 - x - x^2) = x
# kx^2 + (1+k)x - k = 0
# Solving using quadratic formula
# x = (-(1+k) +/- sqrt((1+k)^2 + 4*k*k)) / (2*(3+k))
# x is rational if sqrt() is an integer therefore
# (1+k)^2 + 4*k*k is a square
# 1 + 2k + k^2 + 4k^2 is a square
# 5k^2 + 2k + 1 is a square
# 5k^2 + 2k + 1 = q^2 (diophantine equation)
# rearrange
# 5(k + 1/5)^2 + 4/5 = q^2
# 1/5 (5k + 1)^2 + 4/5 = q^2
# substitute w = 5k + 1, => k = (w-1)/5, note if k is int so is w
# 1/5 w^2 + 4/5 = q^2, w = 5k + 1
# w^2 + 4 = 5q^2
# w^2 - 5q^2 = -4


# x^2 - 5y^2 = -4
# pell equation: x^2 - 5y^2 = 1
# fundamental solution (smallest value of y) (x,y) = (9,4), or (+/- 9, +/- 4)
# therefore u = 9 + 4*sqrt(5)

# to get all possible unique solutions of x^2 - 5*y^2 = 44
# see the rest of the analysis in PE140.py


class Problem137(Problem140):

    @timeit
    def solve(self, n):
        ls_answers = self.generate_all_solutions(d=5, equal_n=-4, get_k=lambda x: (x - 1) / 5)
        return ls_answers[n - 1]


class Solution137(unittest.TestCase):
    def setUp(self):
        self.problem = Problem137()

    def test_solution(self):
        self.assertEqual(1120149658760, self.problem.solve(n=15))


if __name__ == '__main__':
    unittest.main()
