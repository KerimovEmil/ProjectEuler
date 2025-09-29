"""
PROBLEM

Let p_n be the nth prime: 2, 3, 5, 7, 11, ..., and let r be the remainder when (p_{n} − 1)^n + (p_{n} + 1)^n is divided
by p_{n}^2.

For example, when n = 3, p_3 = 5, and 4^3 + 6^3 = 280 ≡ 5 mod 25.

The least value of n for which the remainder first exceeds 10^9 is 7037.
Find the least value of n for which the remainder first exceeds 10^10.

ANSWER: 21035
Solve time ~850 ms
"""

from util.utils import timeit, primes_upto
import unittest

# r = (p_{n} − 1)^n + (p_{n} + 1)^n
# r = sum_{i=0}^{n} p_{n}^i (1 + (-1)^(n-i)) * (n choose i)
# r == sum_{i=0}^{1} p_{n}^i (1 + (-1)^(n-i)) * (n choose i)  mod p_{n}^2
# r ==  (1 + (-1)^(n)) + n * p_{n} *  (1 + (-1)^(n-1)) mod p_{n}^2
# if n is even then r == 2
# if n is odd then r == 2*n*p_{n}

# find odd n such that 2*n*p_{n} >= 10^10


class Problem123:
    def __init__(self, limit):
        self.limit = limit

    @timeit
    def solve(self):
        ls_primes = primes_upto(int(1e6))
        for n in range(1, 100000, 2):
            r = n * ls_primes[n-1] * 2
            if r >= self.limit:
                return n
        return 0


class Solution123(unittest.TestCase):
    def setUp(self):
        self.problem = Problem123(limit=pow(10, 10))

    def test_solution(self):
        self.assertEqual(21035, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
