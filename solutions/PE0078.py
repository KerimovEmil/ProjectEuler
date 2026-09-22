"""
PROBLEM

Let p(n) represent the number of different ways in which n coins can be separated into piles.
For example, five coins can be separated into piles in exactly seven different ways, so p(5)=7.

OOOOO
OOOO O
OOO OO
OOO O O
OO OO O
OO O O O
O O O O O
Find the least value of n for which p(n) is divisible by one million.

ANSWER: 55374
Solve time: ~3.8 seconds
"""
from util.utils import timeit
import unittest


class Problem78:
    def __init__(self):
        pass

    @timeit
    def solve(self, div=1_000_000):
        """
        Euler's Pentagonal Number Theorem:
            p(n) = sum_{k=1}^inf (-1)^{k+1} [ p(n - k(3k-1)/2) + p(n - k(3k+1)/2) ]
        Compute p(n) modulo `div` iteratively using a dynamic programming list.
        """
        p = [1]
        n = 0
        while True:
            n += 1
            total = 0
            k = 1
            while True:
                p1 = k * (3 * k - 1) // 2
                p2 = k * (3 * k + 1) // 2
                sign = 1 if k % 2 == 1 else -1
                if p1 <= n:
                    total += sign * p[n - p1]
                else:
                    break
                if p2 <= n:
                    total += sign * p[n - p2]
                k += 1
            total %= div
            p.append(total)
            if total == 0:
                return n


class Solution78(unittest.TestCase):
    def setUp(self):
        self.problem = Problem78()

    def test_solution(self):
        self.assertEqual(55374, self.problem.solve(div=1_000_000))


if __name__ == '__main__':
    unittest.main()
