"""
PROBLEM

Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0,
where each “_” is a single digit.

ANSWER:
1389019170
Solve time ~20 seconds
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
        upper = int(int(template.replace('_', '9'))**0.5) + 1

        for n in range(lower, upper):
            test = str(n ** 2)
            if all(test[i] == template[i] for i in range(0, len(test), 2)):
                return 10*n


class Solution206(unittest.TestCase):
    def setUp(self):
        self.problem = Problem206()

    def test_solution(self):
        self.assertEqual(1389019170, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

