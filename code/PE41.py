"""
PROBLEM

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once.
For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?

ANSWER:
7652413
Solve time ~0.5 seconds
"""

# Note that:
# 4-digit = 1+2+3+4 = 10
# 5-digit = 1+2+3+4+5 = 15, which is divisible by 3 so it cannot be a prime number.
# 6-digit = 1+2+3+4+5+6 = 21, which is divisible by 3 so it cannot be a prime number.
# 7-digit = 1+2+3+4+5+6+7 = 28
# 8-digit = 1+2+3+4+5+6+7+8 = 36, which is divisible by 3 so it cannot be a prime number.
# 9-digit = 1+2+3+4+5+6+7+8+9 = 45, which is divisible by 3 so it cannot be a prime number.
# 10-digit can't exist.

# therefore since we know it's not a 4 digit number due to the problem, it must be a 7-digit number.

from util.utils import timeit
import unittest
from primesieve import primes


class Problem41:
    def __init__(self, n):
        self.n = n
        self.ans = 0
        self.ls_prime = primes(int(10**(n-1)), int(10**n))

    @timeit
    def solve(self):
        digit_set = {str(i) for i in range(1, self.n + 1)}

        for prime in self.ls_prime[::-1]:
            unique = len(set(str(prime))) == len(list(str(prime)))
            correct_values = set(str(prime)) == digit_set
            if unique and correct_values:
                return prime


class Solution41(unittest.TestCase):
    def setUp(self):
        self.problem = Problem41(n=7)

    def test_solution(self):
        self.assertEqual(7652413, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
