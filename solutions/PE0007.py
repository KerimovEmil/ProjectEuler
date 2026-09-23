"""
PROBLEM

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

ANSWER: 104743
Solve time: ~0.002 seconds
"""

import unittest
from util.utils import timeit, count_primes_upto


class Problem7:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        # The nth prime is less than n * (log n + log log n) for n >= 6, so sieve up to that bound.
        n = self.n
        bound = int(n * (10 ** 0.5)) if n < 10 else int(n * (n.bit_length() * 0.6931471805599453 + 4))
        while count_primes_upto(bound) < n:
            bound *= 2
        sieved = [True] * bound
        for i in range(bound):
            if i >= 2 and sieved[i]:
                for j in range(i * i, bound, i):
                    sieved[j] = False
        count = 0
        for i in range(2, bound):
            if sieved[i]:
                count += 1
                if count == n:
                    return i
        return None


class Solution7(unittest.TestCase):
    def setUp(self):
        self.problem = Problem7(10001)

    def test_solution(self):
        self.assertEqual(104743, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
