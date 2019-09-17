"""
PROBLEM

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
 fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:
1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.
How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d ≤ 12,000?

ANSWER:
7295372
Solve time ~14 seconds
"""

from util.utils import timeit, farey, len_faray_seq
import unittest


class Problem73:
    def __init__(self, d):
        self.d = d

    @timeit
    def quicker_solve(self):
        n = self.d
        a, b, c, d = 0, 1, 1, n
        ok = False
        ans = 0
        while c <= n:
            k = int((n + b) / d)
            a, b, c, d = c, d, k * c - a, k * d - b
            if a == 1 and b == 2:
                break
            if ok:
                ans += 1
            if a == 1 and b == 3:
                ok = True
        return ans

    @timeit
    def solve(self):
        len_f = len_faray_seq(self.d)  # very fast
        f = farey(self.d)  # super slow way

        # note that the middle value will always be 1/2 for all n>1
        # therefore there are always (|F_n| - 1)/2 elements that are less than 1/2
        index_of_half = int((len_f - 1)/2)

        index_of_one_third = f.index((1, 3))  # also slow

        return index_of_half - index_of_one_third - 1


class Solution73(unittest.TestCase):
    def setUp(self):
        self.problem = Problem73(d=12000)

    def test_solution(self):
        # self.assertEqual(7295372, self.problem.solve())
        self.assertEqual(7295372, self.problem.quicker_solve())

    def test_solution_small(self):
        # self.assertEqual(3, Problem73(d=8).solve())
        self.assertEqual(3, Problem73(d=8).quicker_solve())


if __name__ == '__main__':
    unittest.main()
