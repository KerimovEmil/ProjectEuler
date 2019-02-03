# The divisors of 6 are 1,2,3 and 6.
# The sum of the squares of these numbers is 1+4+9+36=50.

# Let sigma2(n) represent the sum of the squares of the divisors of n. Thus sigma2(6)=50.

# Let SIGMA2 represent the summatory function of sigma2, that is SIGMA2(n)=∑sigma2(i) for i=1 to n.
# The first 6 values of SIGMA2 are: 1,6,16,37,63 and 113.
# Find SIGMA2(10^15) modulo 10^9.

# Answer = 281632621

# p(n) = sum_k=1^n k^2 = n*(n+1)*(2n+1)/6
# the divisor i appears exactly floor(n/i) times for all integers below or equal to n
# so in total we should get sum_i  floor(n/i)*i^2
# but this is too slow.

# we can use the sum of squares formula
# the sum of squares of all integers which appear exactly m-times is p(floor(n/m)) - p(floor(n/(m+1)))


import unittest
from util.utils import timeit


class Problem401:
    def __init__(self, max_int, mod):
        self.max_int = max_int
        self.mod = mod
        self.sum_n = 0

    @timeit
    def solve(self):
        mod = self.mod
        n = self.max_int
        sqr_n = int(n**0.5)
        # i < sqrt(n)
        self.sum_n = sum(((i**2 % mod) * (n // i)) for i in range(1, sqr_n + 1)) % mod

        # i >= sqrt(n)
        self.sum_n += sum(((i * self.diff_sum_squares(n // i, n // (i + 1))) % mod
                           for i in range(1, sqr_n + 1))) % mod

        self.sum_n %= mod
        return self.sum_n

    def get_solution(self):
        return self.sum_n

    @staticmethod
    def diff_sum_squares(n, n2):
        """Returns sum_squares(n) - sum_squares(n2)"""
        x = n - n2  # n2 = n - x
        return (x*n*(n2 + 1)) + (x*(2*x-1)*(x-1)) // 6

    # def sum_squares(self, n, m):
    #     if n not in self.dc_sum_sq.keys():
    #         self.dc_sum_sq[n] = ((n * (n + 1) * (2 * n + 1)) // 6) % m
    #     return self.dc_sum_sq[n]


class Solution401(unittest.TestCase):
    def setUp(self):
        self.problem = Problem401(max_int=int(1e15), mod=int(1e9))

    def test_solution(self):
        self.assertEqual(281632621, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
