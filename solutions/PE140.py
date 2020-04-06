"""
PROBLEM

Consider the infinite polynomial series AG(x)=xG1+x2G2+x3G3+⋯, where Gk is the kth term of the second order recurrence
relation G_k =G_{k−1} + G_{k−2}, G_1=1 and G_2=4; that is, 1,4,5,9,14,23,… .

For this problem we shall be concerned with values of x for which A(x) is a positive integer.

The corresponding values of x for the first five natural numbers are shown below.
    x	      A(x)
(√5 - 1)/4	    1
   2/5	        2
(√22 − 2)/6	    3
(√137 - 5)/14	4
    1/2	        5
We shall call A(x) a golden nugget if x is rational, because they become increasingly rarer; for example,
 the 20th golden nugget is 211345365.

Find the sum of the first thirty golden nuggets.

ANSWER: 5673835352990
Solve time ~0.001 seconds
"""
from util.utils import timeit
import unittest

# A(x) = sum_{n=1, inf} G_n x^n
# A(x) = G_1 x + G_2 x^2 + sum_{n=3, inf} G_n x^n
# A(x) = G_1 x + G_2 x^2 + sum_{n=3, inf} G_{n-1} x^n + sum_{n=3, inf} G_{n-2} x^n
# A(x) = G_1 x + G_2 x^2 + x sum_{n=2, inf} G_{n} x^n + x^2 sum_{n=1, inf} G_{n} x^n
# A(x) = G_1 x + G_2 x^2 + x (A(x) - G_1 x) + x^2 A(x)
# A(x) = x + 4x^2 + x (A(x) - x) + x^2 A(x)
# A(x) (1 - x - x^2) = x + 4x^2 - x^2 = x + 5x^2
# A(x) = (x + 3x^2) / (1 - x - x^2)

# set A(x) = k, for k some integer
# A(x) = k = (x + 3x^2) / (1 - x - x^2)
# k(1 - x - x^2) = (x + 3x^2)
# (3+k)x^2 + (1+k)x - k = 0
# Solving using quadratic formula
# x = (-(1+k) +/- sqrt((1+k)^2 + 4*(3+k)*k)) / (2*(3+k))
# x is rational if sqrt() is an integer therefore
# (1+k)^2 + 4*(3+k)*k is a square
# 1 + 2k + k^2 + 12k + 4k^2 is a square
# 5k^2 + 14k + 1 is a square
# 5k^2 + 14k + 1 = q^2 (diophantine equation)
# rearrange
# 5(k + 7/5)^2 - 44/5 = q^2
# 1/5 (5k + 7)^2 - 44/5 = q^2
# substitute w = 5k + 7, => k = (w-7)/5, note if k is int so is w
# 1/5 w^2 - 44/5 = q^2, w = 5k + 7
# w^2 - 44 = 5 q^2
# w^2 - 5q^2 = 44

# k > 0 => (w-7)/5 >0 =>  w>7

# x^2 - 5y^2 = 44
# pell equation: x^2 - 5y^2 = 1
# fundamental solution (smallest value of y) (x,y) = (9,4), or (+/- 9, +/- 4)
# therefore u = 9 + 4*sqrt(5)

# to get all possible unique solutions of x^2 - 5*y^2 = 44, need to check
# |y| <= sqrt(44*u/5) < 12.5

# def is_int(n):
#     return abs(n - int(n)) < 1e-13
# for y in range(1, 13):
#     x2 = 1 + 5 * y * y
#     if is_int(x2 ** 0.5):
#         print(int(x2 ** 0.5), y)

# (x,y) = (+/- 7, +/- 1)
# (x,y) = (+/- 8, +/- 2)
# (x,y) = (+/- 13, +/- 5)
# (x,y) = (+/- 17, +/- 7)

# only looking at positive solutions of (x + y*sqrt(5)), this only leaves:
# (x,y) = (7, +/- 1)
# (x,y) = (8, +/- 2)
# (x,y) = (13, +/- 5)
# (x,y) = (17, +/- 7)

# Looking at (x + y*sqrt(5)) * (9 + 4*sqrt(5)) to find duplicates we find that
# (17 - 7*sqrt(5)) * (9 + 4*sqrt(5)) = (13 + 5*sqrt(5))
# (13 - 5*sqrt(5)) * (9 + 4*sqrt(5)) = (17 + 5*sqrt(5))
# hence we only have 6 unique solution generators:
# (x,y) = (7, +/- 1) = 7 +/- sqrt(5)
# (x,y) = (8, +/- 2) = 8 +/- 2*sqrt(5)
# (x,y) = (13, -5) = 15 - 5*sqrt(5)
# (x,y) = (17, -7) = 17 - 7*sqrt(5)

# u = (9 + 4*sqrt(5))
# (x + y*sqrt(5)) = (7 + 1*sqrt(5)) * u^z  for z in Z^{+} (positive integers)
# (x + y*sqrt(5)) = (7 - 1*sqrt(5)) * u^z  for z in Z^{+} (positive integers)
# (x + y*sqrt(5)) = (8 + 2*sqrt(5)) * u^z  for z in Z^{+} (positive integers)
# (x + y*sqrt(5)) = (8 - 2*sqrt(5)) * u^z  for z in Z^{+} (positive integers)
# (x + y*sqrt(5)) = (15 - 7*sqrt(5)) * u^z  for z in Z^{+} (positive integers)
# (x + y*sqrt(5)) = (17 - 7*sqrt(5)) * u^z  for z in Z^{+} (positive integers)

# for each solution x, compute k = (x-7)/5
# if k is an integer, then k is a golden nugget


def mult_by_u(a, b):
    """return (x,y) such that (x + y*sqrt(5)) =  (a+b*sqrt(5)) * (9 + 4*sqrt(5))"""
    f = 9*a + 20*b  # 20 = 4*5
    s = 4*a + 9*b
    return f, s


def divide_by_u(a, b):
    """return (x,y) such that (x + y*sqrt(5)) = (a+b*sqrt(5)) / (9 + 4*sqrt(5))"""
    f = 9*a - 20*b  # 20 = 4*5
    s = -4*a + 9*b  # note (9 + 4*sqrt(5))*(9 - 4*sqrt(5)) = 1
    return f, s


def is_int(n):
    return abs(n - int(n)) < 1e-13


class Problem140:

    @staticmethod
    def generate_sorted_golden_nuggets(ls_unique):
        num_iter = 10  # some large enough number
        ls_answers = []
        for tup in ls_unique:
            new_answer = tup
            for i in range(num_iter):
                new_answer = mult_by_u(*new_answer)
                x = new_answer[0]
                k = (x - 7) / 5
                if is_int(k):
                    ls_answers.append(int(k))

        return sorted(ls_answers)

    @timeit
    def solve(self, n):
        ls_unique = [(7, 1), (7, -1), (8, 2), (8, -2), (13, -5), (17, -7)]
        ls_answers = self.generate_sorted_golden_nuggets(ls_unique)
        return sum(ls_answers[:n])


class Solution140(unittest.TestCase):
    def setUp(self):
        self.problem = Problem140()

    def test_solution(self):
        self.assertEqual(5673835352990, self.problem.solve(n=30))

    def test_20th_nugget(self):
        ls_unique = [(7, 1), (7, -1), (8, 2), (8, -2), (13, -5), (17, -7)]
        self.assertEqual(211345365, self.problem.generate_sorted_golden_nuggets(ls_unique)[19])

    def test_multiply_and_divide_functions(self):
        self.assertEqual((3, 4), divide_by_u(*mult_by_u(3, 4)))


if __name__ == '__main__':
    unittest.main()

