"""
PROBLEM

A common security method used for online banking is to ask the user for three random characters from a
passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the
expected reply would be: 317.

The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine the
shortest possible secret passcode of unknown length.

ANSWER: 73162890
Solve time: ~0.001 seconds
"""

import os
import unittest
from collections import defaultdict
from util.utils import timeit


class Problem79:
    def __init__(self, file_path):
        self.file_path = file_path
        self.graph = defaultdict(set)

    def build_graph(self):
        with open(self.file_path) as f:
            for line in (code.strip() for code in f):
                if len(line) != 3:
                    continue
                self.graph[line[0]].add(line[1])
                self.graph[line[1]].add(line[2])

    def topological_sort(self):
        result = []
        visited = set()

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for next_node in self.graph[node]:
                visit(next_node)
            result.append(node)

        for node in sorted(self.graph):
            visit(node)
        result.reverse()
        return result

    @timeit
    def solve(self):
        self.build_graph()
        return ''.join(self.topological_sort())


class Solution79(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(
            os.path.dirname(__file__), '..', 'problem_data', 'p079_keylog.txt')
        self.problem = Problem79(file_path=file_path)

    def test_solution(self):
        self.assertEqual('73162890', self.problem.solve())


if __name__ == '__main__':
    unittest.main()
