from util.utils import timeit
import unittest
from itertools import product


class Problem4:
    def __init__(self, num_digits):
        self.lower = 10 ** (num_digits - 1) - 1
        self.upper = 10 ** num_digits - 1

    @staticmethod
    def get_digits(num):
        digits = []
        n = num

        while n > 0:
            d = n % 10
            digits.append(int(d))
            n -= d
            n /= 10

        return digits[::-1]

    @staticmethod
    def is_palindrome(num):
        digits = Problem4.get_digits(num)

        for i, j in zip(digits, reversed(digits)):
            if i != j:
                return False

        return True

    @timeit
    def solve(self):
        pds = []
        for i, j in product(range(self.lower, self.upper), repeat=2):
            if self.is_palindrome(i * j):
                pds.append(i * j)
        return max(pds)


class Solution4(unittest.TestCase):
    def setUp(self):
        self.problem = Problem4(3)

    def test_solution(self):
        self.assertEqual(906609, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
