"""
PROBLEM

For every positive integer n the Fibonacci sequence modulo n is periodic. The period depends on the value of n.
This period is called the Pisano period for n, often shortened to p(n).

There are three values of n for which p(n) equals 18: 19, 38, and 76.
The sum of those smaller than 50 is 19+38=57.

Find the sum of the values of n smaller than 1,000,000,000 for which p(n) equals 120.

ANSWER: 44,511,058,204
Solve time: 0.17 seconds
"""
from util.utils import timeit, primes_of_n, pisano_period
import unittest
from primesieve import primes
from functools import reduce
from itertools import combinations

# facts of p(n) = f(n)
# if n = p^t for p prime, then f(p^t) = p^{t-1} x f(p)
# if m, n coprime then f(m x n) = lcm(f(m), f(n))
# therefore f(p1^k1 x p2^k2 x p3^k3) = lcm(p1^{k1-1} x f(p1), p2^{k2-1} x f(p2), p3^{k3-1} x f(p3))

# example solution for f(n) = 18 = 2 x 3^2

# CASE 1: n = 2^k2 x 3^k3
# f(n) = 2 x 3^2 = lcm(2^{k1-1} x f(2), 3^{k2-1} x f(3))
# f(n) = 2 x 3^2 = lcm(2^{k1-1} x 3, 3^{k2-1} x 2^3)
# therefore no possible solutions for k2 can exist

# CASE 2: n = 2^k2 x p1 x p2 x ... such that f(p_i) = {2 x 3^2, 2 x 3, 2, 3^2}
# only case is f(19) = 2 x 3^2
# therefore f(n) = 2 x 3^2 = lcm(2^{k1-1} x 3, f(19))
# therefore f(n) = 2 x 3^2 = lcm(2^{k1-1} x 3, 2 x 3^2)
# k1 in {1, 2, 3} -> n = 2^k1 x 19 = {19, 38, 76}

# Working on f(n) = 120 = 2^3 x 3 x 5

# CASE 1: n = 2^k2 x 3^k3 x 5^k5
# f(n) = 2^3 x 3 x 5 = lcm(2^{k2-1} x f(2), 3^{k3-1} x f(3), 5^{k5-1} x f(5))
# f(n) = 2^3 x 3 x 5 = lcm(2^{k2-1} x 3, 3^{k3-1} x 2^3, 5^{k5-1} x 2^2 x 5)
# therefore k5 = 1, and k3 in {1,2} and k2 in {0,1,2,3,4}
# therefore n in {30, 90, 60, 180, 120, 360, 240, 720}
# we let the exponents be 0 as well for case 3

# CASE 2: find p_i's such that f(p_i) = {2^k2 x 3^k3 x 5^k5} for 0<=k2<=3, 0<=k3<=1, 0<=k5<=1
# 2 {3: 1}
# 3 {2: 3}
# 5 {2: 2, 5: 1}
# 11 {2: 1, 5: 1}
# 31 {2: 1, 3: 1, 5: 1}
# 41 {2: 3, 5: 1}
# 61 {2: 2, 3: 1, 5: 1}
# 2521 {2: 3, 3: 1, 5: 1}

# therefore [30, 90, 60, 180, 120, 360, 240, 720, + others] x all combinations of [11, 31, 41, 61, 2521]
# [30, 90, 60, 180, 120, 360, 240, 720] x
#    [11, 31, 41, 61, 2521, 341, 451, 671, 27731, 1271, 1891, 78151, 2501, 103361, 153781, 13981, 20801, 859661, 27511,
#     1136971, 1691591, 77531, 3204191, 4767211, 6305021, 852841, 35246101, 52439321, 69355231, 195455651, 2150012161]


class Problem853:
    def __init__(self, limit=1_000_000_000, debug=False):
        self.limit = limit
        self.debug = debug

    @timeit
    def solve(self):

        ls_n = []

        for k2 in range(5):
            for k3 in range(3):
                for k5 in range(2):
                    n = pow(2, k2) * pow(3, k3) * pow(5, k5)
                    ls_n.append(n)
        if self.debug:
            print(f'{ls_n=}')

        ls_p = []
        for p in primes(2600):
            dc = primes_of_n(pisano_period(p))
            if set(dc.keys()) <= {2, 3, 5}:
                # 0 <= k2 <= 3, 0 <= k3 <= 1, 0 <= k5 <= 1
                if dc.get(2, 0) <= 3 and dc.get(3, 0) <= 1 and dc.get(5, 0) <= 1:
                    if self.debug:
                        print(f'{p=}, primes={dc}')
                    if p not in {2, 3, 5}:
                        ls_p.append(p)
        if self.debug:
            print(f'{ls_p=}')

        ls_mult = [1]
        for k in range(len(ls_p)):
            ls_mult += [self.product_t(x) for x in combinations(ls_p, k+1)]
        if self.debug:
            print(f'{ls_mult=}')

        ans = 0
        for n in ls_n:
            for m in ls_mult:
                p = m*n
                if p <= self.limit:
                    if pisano_period(p) == 120:
                        ans += m*n

        return ans

    @staticmethod
    def product_t(x: tuple):
        """Return the product all elements within x"""
        return reduce(lambda a, b: a * b, x)


class Solution853(unittest.TestCase):
    def setUp(self):
        self.problem = Problem853()

    def test_solution(self):
        self.assertEqual(44511058204, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
