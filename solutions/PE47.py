"""
PROBLEM

The first two consecutive numbers to have two distinct prime factors are:

14 = 2 * 7
15 = 3 * 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2*2 * 7 * 23
645 = 3 * 5 * 43
646 = 2 * 17 * 19.

Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?

ANSWER: 134043
Solve time: ~ 0.072 seconds
"""

import unittest
from itertools import count
from util.utils import timeit


class Problem47:
    def __init__(self, consecutive_n):
        self.consecutive_n = consecutive_n
        self.ans = None

    @timeit
    def solve(self):
        sieve = {}  # {(x = multiple of prime p) >= i: [p, known factor count in x]}
        for i in count(2):  # count from 2 upwards
            if i not in sieve:  # if i is prime:
                want = self.consecutive_n  # want 4 consecutive integers
                p = i
            else:
                p, factors = sieve.pop(i)  # have now noted all factors of i
                if factors < self.consecutive_n:  # non-prime i has less than 4 prime factors
                    want = self.consecutive_n
                else:
                    want -= 1
                    if want == 0:
                        self.ans = i - self.consecutive_n + 1
                        return self.ans
            # p divides i; find next unoccupied multiple of p in sieve
            while True:
                i += p
                if i not in sieve:
                    break
                sieve[i][1] += 1  # found one more factor (p) of i
            sieve[i] = [p, 1]  # so far, i has 1 known factor (p)

    def get_solution(self):
        return self.ans


class Solution47(unittest.TestCase):
    def setUp(self):
        self.problem = Problem47(consecutive_n=4)

    def test_solution(self):
        self.assertEqual(134043, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
