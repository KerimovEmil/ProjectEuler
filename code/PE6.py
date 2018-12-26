"""
PROBLEM

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

ANSWER:
25164150
Solve time ~ 0.000 seconds

square sum = (1 + 2 + 3 + 4 + ... + n)^2 = (n * (n+1) / 2)^2
sum squares = 1^2 + 2^2 + 3^2 + ... + n^2 = n * (n+1) * (2n+1) / 6
"""

from util.utils import timeit
import unittest


class Problem6:
    def __init__(self, n):
        self.n = n

    @staticmethod
    def square_sum(n):
        """
        Returns the square of the sum of digits from 1 to n.
        (1 + 2 + 3 + 4 + ... + n)^2
        """
        return (n * (n + 1) / 2) ** 2

    @staticmethod
    def sum_squares(n):
        """
        Returns the sum of the squares from 1 to n.
        1^2 + 2^2 + 3^2 + ... + n^2
        """
        return n * (n + 1) * (2*n + 1) / 6

    @timeit
    def solve(self):
        return self.square_sum(self.n) - self.sum_squares(self.n)


class Solution6(unittest.TestCase):
    def setUp(self):
        self.problem = Problem6(100)

    def test_solution(self):
        self.assertEqual(25164150, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
