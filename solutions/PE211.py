# For a positive integer n, let σ2(n) be the sum of the squares of its divisors. For example,

# σ2(10) = 1 + 4 + 25 + 100 = 130.
# Find the sum of all n, 0 < n < 64,000,000 such that σ2(n) is a perfect square.

# Answer = 1922364685
# solve time ~ way too long.

# n = p1^x p2^y p3^z
# σ2(n) = (1 + p1^2 + p1^4 + ... + p1^2x) * (1 + p2^2 + p2^4 + ... + p2^2y) * (1 + p3^2 + p3^4 + ... + p3^2z)
# σ2(n) = (p1^(2x + 2) - 1)/(p1^2 - 1)) * (p2^(2y + 2) - 1)/(p2^2 - 1)) * (p3^(2z + 2) - 1)/(p3^2 - 1))
# σ2(n) = (p1^(2x + 2) - 1) * (p2^(2y + 2) - 1) * (p3^(2z + 2) - 1) / [ (p1^2 - 1) * (p2^2 - 1) * (p3^2 - 1) ]

# S = 1 + x^2 + x^4 + x^6
# x^2 S = x^2 + x^4 + x^6 + x^8
# S (1 - x^2) = 1 - x^8
# S = (x^8 - 1) / (x^2 - 1)

import unittest
from util.utils import timeit
from util.utils import primes_of_n
from util.utils import sieve
# import math
# from functools import lru_cache


class Problem211:
    def __init__(self, max_int):
        self.max_int = max_int
        self.sum_n = 0
        self.dc_sq_sum = {}
        self.dc_prime_factor_sq_sum = {}

    @timeit
    def solve(self):

        ls_primes = list(sieve(int(self.max_int)))
        # max_lg = math.log2(self.max_int)
        # dc_max_factors = {p: int(max_lg/math.log2(p)) for p in ls_primes}
        #
        # # Load all sigma2's
        # for p, max_m in dc_max_factors.items():
        #     for i in range(1, max_m + 1):
        #         self.dc_sq_sum[(p, i)] = int((p ** (2 * i + 2) - 1) / (p ** 2 - 1))
        #         self.dc_prime_factor_sq_sum[(p, i)] = primes_of_n(self.dc_sq_sum[(p, i)])

        for i in range(self.max_int):
            dc_factors = primes_of_n(i, ls_primes)
            sum_sqs = self.sum_sq_divisors(dc_factors)

            if self.test_square(sum_sqs):
                print(i, dc_factors, int(sum_sqs), int(sum_sqs**0.5))
                self.sum_n += i
        return self.sum_n

    @staticmethod
    def test_square(x):
        sqrtx = x ** 0.5
        return abs(sqrtx - int(sqrtx)) < 1e-14

    # @lru_cache(maxsize=None)
    def sum_sq_divisors_prime(self, prime, factor):
        if (prime, factor) in self.dc_sq_sum:
            return self.dc_sq_sum[(prime, factor)]
        else:
            self.dc_sq_sum[(prime, factor)] = (prime**(2*factor+2) - 1) / (prime**2 - 1)
            return self.dc_sq_sum[(prime, factor)]

    def sum_sq_divisors(self, dc_primes):
        sum_sq = 1
        for p, m in dc_primes.items():
            sum_sq *= self.sum_sq_divisors_prime(p, m)
        return sum_sq

    def get_solution(self):
        return self.sum_n


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem211(max_int=64000000)
        # self.problem = Problem211(max_int=100)

    def test_solution(self):
        self.assertEqual(1922364685, self.problem.solve())
        # self.assertEqual(43, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
