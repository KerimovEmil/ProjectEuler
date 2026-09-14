"""
PROBLEM

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2,
3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The
lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

ANSWER: 2783915460
Solve time: ~0.001 seconds
"""

import unittest
from util.utils import timeit, basic_factorial


class Problem24:
    def __init__(self, digits, target_index):
        self.digits = digits
        self.target_index = target_index

    @timeit
    def solve(self):
        # Factoradic representation of the 0-indexed permutation
        n = len(self.digits)
        digits = list(self.digits)
        target = self.target_index - 1
        result = []
        for i in range(n):
            fact = basic_factorial(n - 1 - i)
            index = target // fact
            result.append(str(digits.pop(index)))
            target %= fact
        return int(''.join(result))


class Solution24(unittest.TestCase):
    def setUp(self):
        self.problem = Problem24(list(range(10)), 1000000)

    def test_solution(self):
        self.assertEqual(2783915460, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
