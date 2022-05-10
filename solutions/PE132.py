"""
PROBLEM

A number consisting entirely of ones is called a repunit. We shall define R(k) to be a repunit of length k.

For example, R(10) = 1111111111 = 11×41×271×9091, and the sum of these prime factors is 9414.

Find the sum of the first forty prime factors of R(10^9).

ANSWER: 843296
Solve time ~0.05 seconds
"""
from util.utils import timeit
import unittest
from primesieve import primes


# R(n) = (10^n - 1) / 9
# R(n) == 0 mod p
# 10^n - 1 == 0 mod 9p
# 10^n == 1 mod 9p


class Problem132:
    def __init__(self):
        pass

    @timeit
    def solve(self, n=pow(10, 9), max_count=40, max_prime=200000):
        ans = 0
        count = 0
        ls_primes = primes(max_prime)
        for p in ls_primes:
            if pow(10, n, 9 * p) == 1:
                count += 1
                ans += p
            if count == max_count:
                break
        return ans


class Solution132(unittest.TestCase):
    def setUp(self):
        self.problem = Problem132()

    def test_solution(self):
        self.assertEqual(843296, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

