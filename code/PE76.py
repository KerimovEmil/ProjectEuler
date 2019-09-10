"""
PROBLEM

It is possible to write five as a sum in exactly six different ways:

4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?

ANSWER:

Solve time ~0.03 seconds
"""

# using recursive equation found here: http://www.cs.utsa.edu/~wagner/python/fp/part.html
# p(n) = sum_{k=1}^{n} (-1)^{k+1} (p(x) + p(y))
# x = n - k*(3k-1)/2
# y = n - k*(3k+1)/2

from util.utils import timeit, partition_number
import unittest


class Problem76:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        return partition_number(self.n) - 1  # minus one remove the n + 0 case


class Solution76(unittest.TestCase):
    def setUp(self):
        self.problem = Problem76(n=100)

    def test_solution(self):
        self.assertEqual(190569291, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
