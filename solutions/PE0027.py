"""
PROBLEM

Euler discovered the remarkable quadratic formula:

n^2 + n + 41

It turns out that the formula will produce 40 primes for the consecutive integer values 0 <= n <= 39. However, when
n = 40, 40^2 + 40 + 41 = 40(40 + 1) + 41 is divisible by 41, and certainly when n = 41, 41^2 + 41 + 41 is clearly
divisible by 41.

The incredible formula n^2 - 79n + 1601 was discovered, which produces 80 primes for the consecutive values 0 <= n
<= 79. The product of the coefficients, -79 and 1601, is -126479.

Considering quadratics of the form:

n^2 + an + b, where |a| < 1000 and |b| <= 1000

where |n| is the modulus/absolute value of n, e.g. |11| = 11 and |-4| = 4.

Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of
primes for consecutive values of n, starting with n = 0.

ANSWER: -59231
Solve time: ~0.004 seconds
"""

import unittest
from util.utils import timeit, primes_upto


class Problem27:
    def __init__(self, a_max, b_max):
        self.a_max = a_max
        self.b_max = b_max

    @timeit
    def solve(self):
        # Max possible value of n^2 + a*n + b for the searched range of consecutive n is well under
        # a_max^2 + a_max * n_max + b_max. Sieve once up to a safe bound.
        bound = self.a_max ** 2 + (self.a_max + self.b_max) * self.a_max + self.b_max + 1000
        prime_set = set(primes_upto(bound))

        best_product = 0
        best_run = 0
        for a in range(-self.a_max + 1, self.a_max):
            for b in range(-self.b_max, self.b_max + 1):
                n = 0
                while (n * n + a * n + b) in prime_set:
                    n += 1
                if n > best_run:
                    best_run = n
                    best_product = a * b
        return best_product


class Solution27(unittest.TestCase):
    def setUp(self):
        self.problem = Problem27(1000, 1000)

    def test_solution(self):
        self.assertEqual(-59231, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
