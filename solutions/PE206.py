"""
PROBLEM

Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0,
where each “_” is a single digit.

ANSWER:
1389019170
Solve time < 0.1 seconds
"""

from util.utils import timeit
import unittest


class Problem206:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        template = '1_2_3_4_5_6_7_8_9'
        lower = int(int(template.replace('_', '0'))**0.5)
        compare = template.replace('_', '')

        i = 138902657
        while i > lower:
            if str(i * i)[::2] == compare:
                break
            i -= 4
            if str(i * i)[::2] == compare:
                break
            i -= 6

        return i * 10


class Solution206(unittest.TestCase):
    def setUp(self):
        self.problem = Problem206()

    def test_solution(self):
        self.assertEqual(1389019170, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

