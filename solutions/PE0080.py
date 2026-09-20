"""
PROBLEM
It is well known that if the square root of a natural number is not an integer, then it is irrational.
The decimal expansion of such square roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first one hundred decimal
digits for all the irrational square roots.

ANSWER: 40886
Solve time: ~0.05 seconds
"""

from util.utils import timeit
import unittest


def fast_sq_root(n, decimal_limit=1e10):
    """
    Algorithm by Frazer Jarvis
    References: https://studylib.net/doc/7921494/square-roots-by-subtraction---jarvis--frazer
    Args:
        n: value to take the square root of
        decimal_limit: number of decimals

    Returns:

    """
    a = 5*n
    b = 5
    while b <= decimal_limit:
        if a >= b:
            a = a-b
            b += 10
        else:
            a = int(str(a) + '00')
            b = int(str(b)[:-1] + '05')
    return b


def str_digit_sum(n: str):
    return sum(int(i) for i in list(n))


class Problem80:
    def __init__(self, decimals=100, limit=100):
        self.decimals = decimals
        self.limit = limit
        self.ans = 0

    @timeit
    def solve(self):
        for n in range(1, self.limit+1):
            if n not in [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]:
                sqrt_n = fast_sq_root(n, pow(10, self.decimals+1))
                decimal_str = str(sqrt_n)[:self.decimals]
                self.ans += str_digit_sum(decimal_str)

        return self.ans

    def solve_one_value(self, n):
        sqrt_n = fast_sq_root(n, pow(10, self.decimals + 1))
        decimal_str = str(sqrt_n)[:self.decimals]
        return str_digit_sum(decimal_str)


class Solution80(unittest.TestCase):
    def setUp(self):
        self.problem = Problem80()

    def test_2(self):
        self.assertEqual(475, self.problem.solve_one_value(2))

    def test_solution(self):
        self.assertEqual(40886, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
