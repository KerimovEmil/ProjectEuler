"""
PROBLEM

An irrational decimal fraction is created by concatenating the positive integers:
0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.
If dn represents the nth digit of the fractional part, find the value of the following expression.
d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000

ANSWER:
210
Solve time ~0.063 seconds
"""

import unittest
from util.utils import timeit


class Problem40:
    def __init__(self, ls_index, max_int):
        self.max_int = max_int
        self.ls_index = ls_index
        self.ans = 1

    @timeit
    def solve(self):
        s = ''.join([str(i) for i in range(1, self.max_int)])

        for index in self.ls_index:
            self.ans *= int(s[index])
        return self.ans


class Solution40(unittest.TestCase):
    def setUp(self):
        ls_index = [0, 9, 99, 999, 9999, 99999, 999999]
        self.problem = Problem40(ls_index=ls_index, max_int=500000)

    def test_solution(self):
        self.assertEqual(210, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
