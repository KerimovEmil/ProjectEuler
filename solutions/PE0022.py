"""
PROBLEM

Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names,
begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value
by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the
938th name in the list. So, COLIN would obtain a score of 938 x 53 = 49714.

What is the total of all the name scores in the file?

ANSWER: 871198282
Solve time: ~0.007 seconds
"""

import unittest
from util.utils import timeit
import os


class Problem22:
    def __init__(self, names):
        self.names = names

    @timeit
    def solve(self):
        sorted_names = sorted(self.names)
        total = 0
        for i, name in enumerate(sorted_names, 1):
            value = sum(ord(ch) - ord('A') + 1 for ch in name)
            total += i * value
        return total


class Solution22(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p022_names.txt')
        with open(file_path) as f:
            import re
            names = re.findall(r'"([A-Z]+)"', f.read())
        self.problem = Problem22(names)

    def test_solution(self):
        self.assertEqual(871198282, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
