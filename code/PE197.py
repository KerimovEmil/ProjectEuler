"""
PROBLEM

Given is the function f(x) = ⌊2^(30.403243784-x^2)⌋ × 1e-9 ( ⌊ ⌋ is the floor-function),
the sequence u(n) is defined by u(0) = -1 and u(n+1) = f(u(n)).

Find u(n) + u(n+1) for n = 10^12.
Give your answer with 9 digits after the decimal point.

ANSWER:
1.710637717
Solve time ~ 0.001 seconds
"""

from util.utils import timeit
import unittest


def f(x):
    return int(2**(30.403243784-x**2)) * 1e-9


def u(n):
    if n == 0:
        return -1
    else:
        return f(u(n-1))


# notice that the values of u_n seem to osculate
# u(0) = -1
# u(1) = 0.7100000000000001
# u(2) = 1.001242148
# u(3) = 0.708777686
# u(4) = 1.002446415
# u(5) = 0.707593212
# u(6) = 1.0036128
# u(7) = 0.706446531
# u(8) = 1.0047414000000001
# u(9) = 0.7053374990000001

# looking at the consecutive sums we get:
# u(0) + u(1) = -0.2899999999999999
# u(2) + u(3) = 1.7100198340000001
# u(4) + u(5) = 1.710039627
# u(6) + u(7) = 1.710059331
# u(8) + u(9) = 1.7100788990000002

# this number seems to converge, computing a few more terms:
# u(514) + u(515) = 1.710637717
# u(516) + u(517) = 1.710637717
# u(518) + u(519) = 1.710637717
# u(520) + u(521) = 1.710637717


class Problem197:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        return round(u(518) + u(518+1), 9)


class Solution197(unittest.TestCase):
    def setUp(self):
        self.problem = Problem197()

    def test_solution(self):
        self.assertEqual(1.710637717, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
