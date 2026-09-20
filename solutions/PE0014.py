"""
PROBLEM

The following iterative sequence is defined for the set of positive integers:

n -> n/2 (n is even)
n -> 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet
(Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.

ANSWER: 837799
Solve time: ~0.45 seconds
"""

import unittest
from util.utils import timeit


class Problem14:
    def __init__(self, limit):
        self.limit = limit

    @timeit
    def solve(self):
        def chain_len(start):
            n = start
            count = 1
            while n != 1:
                if n < len(cache) and cache[n]:
                    count += cache[n] - 1
                    break
                n = n // 2 if n % 2 == 0 else 3 * n + 1
                count += 1
            if start < len(cache):
                cache[start] = count
            return count

        cache = [0] * (self.limit + 1)
        max_len = 0
        max_start = 1
        for i in range(1, self.limit):
            length = chain_len(i)
            if length > max_len:
                max_len = length
                max_start = i
        return max_start


class Solution14(unittest.TestCase):
    def setUp(self):
        self.problem = Problem14(1_000_000)

    def test_solution(self):
        self.assertEqual(837799, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
