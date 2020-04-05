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

ANSWER:

Solve time ~ seconds
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
# 5(k + 7/5)^2 - 44/5 = q^2
# 1/5 (5k + 7)^2 - 44/5 = q^2
# 1/5 w^2 - 44/5 = q^2, w = 5k + 7
# w^2 - 44 = 5 q^2
# w^2 - 5q^2 = 44

# k > 0 => (w-7)/5 >0 =>  w>7

# Solving the equation x^2 - 5y^2 = 44
# Stolt fundamental solution [0]: (7, 1)
# x = (7u + 5v)/2
# y = (u + 7v)/2
# Stolt fundamental solution [1]: (-7, 1)
# x = (-7u + 5v)/2
# y = (u - 7v)/2
# where u and v are integers satisfying u^2 - 5v^2 = 4
# There are 2 Stolt fundamental solutions of x^2 - 5 y^2 = 44
# (3,1) is the fundamental solution to u^2 - 5v^2 = 4
# 3^2 - 5 1^2 = 9 - 5 = 4
# ε_4 = (3+√5)/2
# (1/2) * (u + v √5) = (ε_4)^z = ((3+√5)/2)^z
# e.g. z=1 -> u=3, v=1 -> x = (7u + 5v)/2 = (21 + 5)/2 = 13 ->  k=(13-7)/5 = 6/5, can't work not int
# ((3+√5)/2)^2 = 1/4 * (9 + 6√5 + 5) = 1/2 (7 + 3√5)
# e.g. z=2 -> u=7, v=3 -> x = (7u + 5v)/2 = (49 + 15)/2 = 32 ->  k=(32-7)/5 = 5

# ((3+√5)/2)^z
# ((3+√5)/2)^1 = 1/2*(3 + 1√5)
# ((3+√5)/2)^2 = 1/2*1/2*(3 + 1√5)*(3 + 1√5) = 1/2*1/2*(3^2 + 2*3*1*√5 + 1^2*5) = 1/2*(7 + 3*√5)
# ((3+√5)/2)^{k+1} = 1/2*(a_{k+1} + b_{k+1}*√5) = 1/2*(a_{k} + b_{k}*√5) * 1/2*(3 + 1√5) = ...
# = 1/2*1/2*(3*a_{k} + a_{k}*√5 + 3*b_{k}*√5 + 5*b_{k})
# = 1/2*1/2*((3*a_{k} + 5*b_{k}) + (a_{k} + 3*b_{k})*√5)
# = 1/2*((3*a_{k} + 5*b_{k})/2 + (a_{k} + 3*b_{k})/2*√5)

# a_{k+1} = (3*a_{k} + 5*b_{k})/2
# b_{k+1} = (a_{k} + 3*b_{k})/2
# a_1 = 3, b_1 = 1
# a_2 = (3*3 + 5*1)/2 = 14/2 = 7
# b_2 = (3 + 3*1)/2 = 3

# 2*a_{k+1} = 3*a_{k} + 5*b_{k}  ... (1)
# 2*b_{k+1} = a_{k} + 3*b_{k}    ... (2)


# (√5k)^2 + 14k + 1 = q^2

# mod 4 of a square is either 1 or 0
# 5k^2 + 14k + 1 mod 4 = k^2 + 2k + 1 mod 4 = {0, 1}
# if k = 2*m:
#   4m^2 + 4m + 1 mod 4 = 1
# if k = 2*m + 1:
#   4m^2 + 1 + 4m + 2 + 1 mod 4 = 0


def get_k(f, s):
    def g(n):
        a = f * (9 - 4 * (5 ** 0.5)) ** (2 * n)
        b = -s * (5 ** 0.5) * (9 - 4 * (5 ** 0.5)) ** (2 * n)
        c = f * (9 + 4 * (5 ** 0.5)) ** (2 * n)
        d = s * (5 ** 0.5) * (9 + 4 * (5 ** 0.5)) ** (2 * n)
        return round(0.1 * (a + b + c + d - 14))

    return g


g1 = get_k(217, 97)
g2 = get_k(17, 7)
# g3 = get_k(56, 25, 7)
g3 = get_k(112, 50)
# g4 = get_k(16, 7, 7)
g4 = get_k(32, 14)
g5 = get_k(7, 1)
ls_g = [g1,g2,g3,g4,g5]


def is_int(n):
    return abs(n - int(n)) < 1e-13


class Problem140:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        answers = list(set([g(n) for g in ls_g for n in range(0, 9)]))
        # for n in range(0, 10):
        #     print(n, [g(n) for g in ls_g])
        answers = sorted(answers)
        print(answers)
        return sum(answers[:self.n])

    def solve_1(self):
        num_sol = 0
        sum_num = 0
        for k in range(1, 1000):
            x = 5 * k ** 2 + 14 * k + 1
            # print(k, x, x**0.5)
            if is_int(x ** 0.5):
                num_sol += 1
                sum_num += k
                print(k, x)
            if num_sol > self.n:
                print(sum_num)
                return sum_num
        return None


class Solution140(unittest.TestCase):
    def setUp(self):
        self.problem = Problem140(n=30)
        self.problem.solve_1()

    def test_solution(self):
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

