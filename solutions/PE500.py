"""
PROBLEM

The number of divisors of 120 is 16.
In fact 120 is the smallest number having 16 divisors.

Find the smallest number with 2^500500 divisors.
Give your answer modulo 500500507.

ANSWER:
Solve time ~ seconds
"""

from util.utils import timeit
import unittest

# 500500 = 2^2 × 5^3 × 7 × 11 × 13
# divisors(p1^{k1} x p2^{k2} x p3^{k3} x ... x pn^{kn}) = (k1+1) x (k2+1) x (k3+1) x ... x (kn+1)
# divisors(p1*p2*p3*...*pn) = (1+1)^n = 2^n


# d(2*3*5*7) = d(210) = (1+1)*(1+1)*(1+1)*(1+1) = 2^4 = 16
# d(2^3*3*5) = d(120) = (1+3)*(1+1)*(1+1) = 2^4

# 2^2 = 4 < 5
# 2^6 = 64 < 67


# 2^31 * 3^15 * 5^15 * 7^15 * 11^7 * 13^7 * 17^7 * 19^7 * 23^7 * 31^7 * 37^7 * 41^7 * 43^7 * 47^7 * 53^3 * ....
# * 7370029

class Problem500:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution500(unittest.TestCase):
    def setUp(self):
        self.problem = Problem500()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

