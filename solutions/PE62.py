"""
PROBLEM

The cube, 41063625 (345^3), can be permuted to produce two other cubes: 56623104 (384^3) and 66430125 (405^3).
 In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.

ANSWER: 127035954683
Solve time: ~0.02 seconds
"""

from util.utils import timeit
import unittest


class Problem62:
    def __init__(self, max_num):
        self.max_num = max_num

    @timeit
    def solve(self, num_permutations):

        dc_seen = dict()
        for i in range(1, self.max_num):
            i3 = i ** 3

            # create unique key of sorted digits
            f = ''.join(sorted(str(i3)))

            dc_seen[f] = dc_seen.get(f, []) + [i3]

            if len(dc_seen[f]) == num_permutations:
                return dc_seen[f][0]


class Solution62(unittest.TestCase):
    def setUp(self):
        self.problem = Problem62(max_num=10000)

    def test_solution(self):
        self.assertEqual(127035954683, self.problem.solve(num_permutations=5))


if __name__ == '__main__':
    unittest.main()

