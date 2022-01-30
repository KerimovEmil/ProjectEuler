"""
PROBLEM

There are exactly ten ways of selecting three from five, 12345:
123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

In combinatorics, we use the notation, (5 choose 3) = 10
In general, (n choose r) = n!/(r! * (n-r)!), where r <= n

It is not until n=23, that a value exceeds one-million: (23 choose 10) = 1144066
How many, not necessarily distinct, values of (n choose r) for 1<=n<=100 are greater than one-million?

ANSWER: 4075
Solve time ~0.001 seconds
"""
import unittest
from util.utils import combin
from util.utils import timeit


class Problem53:
    def __init__(self, max_int, max_n):
        self.max_int = max_int
        self.max_n = max_n

    @timeit
    def solve(self):
        count = 0
        for n in range(0, self.max_n + 1):
            for r in range(0, int(n / 2 + 1)):
                if combin(n, r) > self.max_int:
                    count += n - 2 * r + 1
                    break

        return count


class Solution53(unittest.TestCase):
    def setUp(self):
        self.problem = Problem53(max_int=1000000, max_n=100)

    def test_solution(self):
        self.assertEqual(4075, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
