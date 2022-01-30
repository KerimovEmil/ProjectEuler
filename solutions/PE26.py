"""
A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to
10 are given:

1/2	= 	0.5
1/3	= 	0.(3)
1/4	= 	0.25
1/5	= 	0.2
1/6	= 	0.1(6)
1/7	= 	0.(142857)
1/8	= 	0.125
1/9	= 	0.(1)
1/10	= 	0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring
cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

ANSWER: 983
Solve time ~ <0.01 seconds
"""
from util.utils import timeit, cycle_length
import unittest


class Problem26:
    def __init__(self, max_d):
        self.max_d = max_d

    @timeit
    def solve(self):
        max_cycle = 0
        ans = None
        for i in range(3, self.max_d):
            c_len = cycle_length(i)
            if c_len > max_cycle:
                max_cycle = c_len
                ans = i
        return ans


class Solution26(unittest.TestCase):
    def setUp(self):
        self.problem = Problem26(max_d=1000)

    def test_solution(self):
        self.assertEqual(983, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

