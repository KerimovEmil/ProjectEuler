"""
PROBLEM

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
fraction.
If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:
1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.
How many elements would be contained in the set of reduced proper fractions for d ≤ 1,000,000?

ANSWER:
303963552391
Solve time ~4 seconds
"""

from util.utils import timeit, len_faray_seq
import unittest


class Problem72:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        return len_faray_seq(self.n) - 2  # subtract the 0/n and n/n cases.


class Solution72(unittest.TestCase):
    def setUp(self):
        self.problem = Problem72(n=1000000)

    def test_solution(self):
        self.assertEqual(303963552391, self.problem.solve())

    def test_small_solution(self):
        self.assertEqual(21, Problem72(n=8).solve())


if __name__ == '__main__':
    unittest.main()

