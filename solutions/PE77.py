"""
PROBLEM

It is possible to write ten as the sum of primes in exactly five different ways:

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over five thousand different ways?

ANSWER: 71
Solve time: ~26 ms
Related problems: 31, 76
"""
from util.utils import timeit
import unittest
from primesieve import primes


class Problem77:
    def __init__(self, target=5000):
        self.target = target

    @timeit
    def solve(self):
        dc_ways = dict()
        dc_ways[0] = 1

        for i in primes(self.target):
            for j in range(i, self.target + 1):
                new_ways = dc_ways.get(j, 0) + dc_ways.get(j - i, 0)
                dc_ways[j] = new_ways
                if new_ways > self.target:
                    break

        for k, v in dc_ways.items():
            if v > self.target:
                return k

        return None


class Solution77(unittest.TestCase):
    def setUp(self):
        self.problem = Problem77(target=5000)

    def test_solution(self):
        self.assertEqual(71, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
