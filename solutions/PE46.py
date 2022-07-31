"""
PROBLEM
What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?

ANSWER: 5777
Solve time < 1 ms
"""

from util.utils import timeit
import unittest
from primesieve import primes


class Problem46:
    def __init__(self, max_potential=10000):

        self.ls_primes = primes(10000)
        self.ls_square = [x**2 for x in range(int(max_potential**0.5))]

    @timeit
    def solve(self):
        num_set = set(range(3, 10000, 2))
        for p in self.ls_primes:
            for sq in self.ls_square:
                value = p + 2*sq
                try:
                    num_set.remove(value)
                except KeyError:
                    pass

        return min(num_set)


class Solution46(unittest.TestCase):
    def setUp(self):
        self.problem = Problem46()

    def test_solution(self):
        self.assertEqual(5777, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
