"""
For a non-negative integer k, define
E_{k}(q) = sum_{n=1}^{inf} sigma_{k}(n) q^n
where sigma_{k}(n) is the sum of the k-th powers of the positive divisors of n.

It can be shown that, for every k, the series E_{k}(q) converges for any 0<q<1.

For example,
E_{1}(1 - 2^-4) = 3.872155809243e2
E_{3}(1 - 2^-8) = 2.767385314772e10
E_{7}(1 - 2^-15) = 6.725803486744e39

All the above values are given in scientific notation rounded to twelve digits after the decimal point.

Find the value of E_{15}(1 - 2^-25).

Give the answer in scientific notation rounded to twelve digits after the decimal point.

ANSWER: 3.376792776502e132
Solve time: ~0.001 seconds
"""
from util.utils import timeit
import unittest
from math import factorial, log
from util.special_number_series import zeta

# we see that E_{k}(q) = sum_{n=1}^{inf} \sigma_{k}(n) q^n = sum_{n=1}^{inf} n^k q^n / (1 - q^n)
# using paper here: https://arxiv.org/pdf/1602.01085.pdf we see that the expansion around q=1 is:
# E_{k}(q) ~= k! * zeta(k+1) / log(q)^{k+1}


class Problem722:
    def __init__(self):
        pass

    @staticmethod
    @timeit
    def solve(k, q):
        value = zeta(k+1) * factorial(k) / (log(q)) ** (k+1)
        return f'{value:.12e}'


class Solution722(unittest.TestCase):
    def setUp(self):
        self.problem = Problem722()

    def test_solution(self):
        self.assertEqual('3.376792776502e+132', self.problem.solve(k=15, q=1-pow(2, -25)))


if __name__ == '__main__':
    unittest.main()
