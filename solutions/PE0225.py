"""
PROBLEM

The sequence 1, 1, 1, 3, 5, 9, 17, 31, 57, 105, 193, 355, 653, 1201 ... is defined by
T1 = T2 = T3 = 1 and Tn = T(n-1) + T(n-2) + T(n-3).

It can be shown that 27 does not divide any terms of this sequence. In fact, 27 is the first odd
number with this property.

Find the 124th odd number that does not divide any terms of the above sequence.

ANSWER: 2009
Solve time: ~0.519 seconds
"""

import unittest
from util.utils import timeit


class Problem225:
    def __init__(self, target_index):
        self.target_index = target_index

    @staticmethod
    def is_non_divisor(m):
        """Return True if m divides no term of the tribonacci sequence."""
        a, b, c = 1, 1, 1
        while True:
            a, b, c = b, c, (a + b + c) % m
            if a == 0:
                return False
            if a == 1 and b == 1 and c == 1:
                return True

    @timeit
    def solve(self):
        found = 0
        candidate = 1
        while True:
            candidate += 2
            if self.is_non_divisor(candidate):
                found += 1
                if found == self.target_index:
                    return candidate


class Solution225(unittest.TestCase):
    def setUp(self):
        self.problem = Problem225(target_index=124)

    def test_solution(self):
        self.assertEqual(2009, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
