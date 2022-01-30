"""
PROBLEM

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner
of each solution grid; for example, 483 is the 3-digit number found in the top left corner of
the solution grid above.

ANSWER:
24702
Solve time ~ 68 seconds
"""

import unittest
from util.dlx import DancingLinks, LeftIterator
from util.utils import timeit
import os


class Problem96:
    def __init__(self, filename):
        self.filename = filename
        pass

    def load_sudoku(self):
        with open(self.filename, 'r') as f:
            lines = f.read().splitlines()
            sudokus = []
            for i in range(0, len(lines), 10):
                sudoku = lines[i + 1: i + 10]
                sudokus.append(sudoku)
        return sudokus

    @staticmethod
    def gen_row(row_id, col_id, value):
        # each box filled once
        # only once in row,
        # only once in column,
        # only one in group,
        constraints = [False for _ in range(81 * 4)]
        eid = value - 1

        # box(i,j) is filled
        constraints[row_id * 9 + col_id] = True
        # value only exists in row-i once
        constraints[81 + eid * 9 + row_id] = True
        # value only exists in col-j once
        constraints[2 * 81 + eid * 9 + col_id] = True
        # value only exists in group-k once
        group_row = row_id // 3
        group_col = col_id // 3

        idx = group_row * 3 + group_col
        constraints[3 * 81 + eid * 9 + idx] = True
        return tuple(constraints)

    @staticmethod
    def to_exact_cover(sudoku_matrix):
        existing_rows = []
        other_rows = []
        mat_ref = {}

        for row_id in range(len(sudoku_matrix)):
            row = sudoku_matrix[row_id]
            for col_id in range(len(row)):
                e = int(row[col_id])
                for value in range(1, 10):
                    constraint_row = Problem96.gen_row(row_id, col_id, value)
                    mat_ref[constraint_row] = (row_id, col_id, value)
                    if (value == e):
                        existing_rows.append(constraint_row)
                    else:
                        other_rows.append(constraint_row)
        return existing_rows, other_rows, mat_ref

    @staticmethod
    def solve_sudoku(sudoku_matrix):
        sudoku = [['0' for _ in range(9)] for _ in range(9)]

        existing_rows, other_rows, mat_ref = Problem96.to_exact_cover(
            sudoku_matrix)
        solver = DancingLinks(other_rows)

        cols_to_cover = set()
        for row in existing_rows:
            for col_id in range(len(row)):
                if (row[col_id]):
                    cols_to_cover.add(col_id)

        for head in LeftIterator(solver.smat.ghead):
            if (head.col_idx in cols_to_cover):
                solver._cover(head)

        solving_nodes = solver.solve()
        solving_rows = set(other_rows[node.row_idx] for node in solving_nodes)
        overall_rows = list(solving_rows) + existing_rows

        for row in overall_rows:
            row_id, col_id, value = mat_ref[row]
            sudoku[row_id][col_id] = str(value)
        return sudoku

    @timeit
    def solve(self):
        moving_sum = 0
        for sudoku in self.load_sudoku():
            solved_sudoku = self.solve_sudoku(sudoku)
            val = int(''.join(solved_sudoku[0][:3]))
            moving_sum += val
        return moving_sum


class Solution96(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p096_sudoku.txt')
        self.problem = Problem96(file_path)

    def test_solution(self):
        self.assertEqual(24702, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
