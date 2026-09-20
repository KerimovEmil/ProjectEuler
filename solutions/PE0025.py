"""
PROBLEM

The Fibonacci sequence is defined by the recurrence relation:

F(n) = F(n-1) + F(n-2), where F(1) = 1 and F(2) = 1.
Hence the first 12 terms will be:

F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(9) = 34
F(10) = 55
F(11) = 89
F(12) = 144
The 12th term, F(12), is the first term to contain three digits.

What is the index of the first term in the Fibonacci sequence to contain 1000 digits?

ANSWER: 4782
Solve time: ~0.01 seconds
"""

import unittest
from util.utils import timeit


class Problem25:
    def __init__(self, num_digits):
        self.num_digits = num_digits

    @timeit
    def solve(self):
        a, b = 1, 1
        index = 2
        while len(str(b)) < self.num_digits:
            a, b = b, a + b
            index += 1
        return index


class Solution25(unittest.TestCase):
    def setUp(self):
        self.problem = Problem25(1000)

    def test_solution(self):
        self.assertEqual(4782, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
