"""
PROBLEM

Each new term in the Fibonacci sequence is generated by adding the previous two terms.
By starting with 1 and 2, the first 10 terms will be:

1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

By considering the terms in the Fibonacci sequence whose values do not exceed four million,
find the sum of the even-valued terms.

ANSWER: 4613732
Solve time: ~0.001 seconds
"""

import unittest
from util.utils import timeit


class Problem2:
    def __init__(self, limit):
        self.limit = limit

    @staticmethod
    def fib(limit):
        n1 = 1
        n2 = 2
        yield n1
        while n2 < limit:
            n1, n2 = n2, n1 + n2
            yield n1

    @timeit
    def solve(self):
        gen = self.fib(self.limit)
        gen_even = (x for x in gen if not x % 2)
        return sum(gen_even)


class Solution2(unittest.TestCase):
    def setUp(self):
        self.problem = Problem2(limit=4000000)

    def test_solution(self):
        self.assertEqual(4613732, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
