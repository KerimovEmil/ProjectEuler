"""
PROBLEM

Let r be the remainder when (a−1)^n + (a+1)^n is divided by a^2.

For example, if a = 7 and n = 3, then r = 42: 63 + 83 = 728 ≡ 42 mod 49. And as n varies, so too will r, but for a = 7
it turns out that rmax = 42.

For 3 ≤ a ≤ 1000, find ∑ rmax.

ANSWER: 333082500
Solve time: ~0.001 seconds
"""

import unittest
from util.utils import timeit


# Expanding using pascals triangle of (a−1)^n + (a+1)^n we see that only the last two terms are not powers of a^2
# moreover, if n is an even power only the constant term remains and if n is an odd term only the second last term
# remains. This logic can be summarized in the following function:
# def f(a, n):
#     if n % 2 == 0:
#         return 2
#     else:
#         return (2 * n * a) % (a ** 2)

# therefore to get the max r for a given a, we only need to loop over values of n to observe the values of:
# (2 * n * a) % (a ** 2)

# note that to maximize the value of (2 * n * a) % (a ** 2) over various n we can get the analytic form:
# If a is odd: (2 * ((a-1)/2) * a) is maximal = ((a-1) * a) = a^2-a
# If a is even: (2 * ((a-2))/ 2) * a) is maximal = (a-2) * a = a^2 - 2a


class Problem120:
    def __init__(self, min_a, max_a):
        self.min_a = min_a
        self.max_a = max_a
        self.sum_max_r = 0

    @timeit
    def solve(self):
        return sum(a ** 2 - (2 - (a % 2)) * a for a in range(self.min_a, self.max_a + 1))


class Solution120(unittest.TestCase):
    def setUp(self):
        self.problem = Problem120(min_a=3, max_a=1000)

    def test_solution(self):
        self.assertEqual(333082500, self.problem.solve())

    def test_simple_solution(self):
        self.assertEqual(42, Problem120(min_a=7, max_a=7).solve())


if __name__ == '__main__':
    unittest.main()
