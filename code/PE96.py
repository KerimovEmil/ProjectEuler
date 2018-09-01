''''By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner
of each solution grid; for example, 483 is the 3-digit number found in the top left corner of
the solution grid above.'''

import os
import sys

scriptpath = "../util/"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

from dlx import DancingLinks, LeftIterator

def load_sudoku():
    with open(r'../problem_data/p096_sudoku.txt', 'r') as f:
        lines = f.read().splitlines()
        sudokus = []
        for i in range(0, len(lines), 10):
            sudoku = lines[i + 1: i + 10]
            sudokus.append(sudoku)
    return sudokus

def gen_row(row_id, col_id, value):
    # each box filled once
    # only once in row,
    # only once in column,
    # only one in group,
    constraints = [False for _ in range(81*4)]
    eid = value - 1

    # box(i,j) is filled
    constraints[row_id * 9 + col_id] = True
    # value only exists in row-i once
    constraints[81 + eid * 9 + row_id] = True
    # value only exists in col-j once
    constraints[2*81 + eid*9 + col_id] = True
    # value only exists in group-k once
    group_row = row_id // 3
    group_col = col_id // 3

    idx = group_row * 3 + group_col
    constraints[3*81 + eid * 9 + idx] = True
    return tuple(constraints)

def to_exact_cover(sudoku_matrix):
    existing_rows = []
    other_rows = []
    mat_ref = {}

    for row_id in range(len(sudoku_matrix)):
        row = sudoku_matrix[row_id]
        for col_id in range(len(row)):
            e = int(row[col_id])
            for value in range(1,10):
                constraint_row = gen_row(row_id, col_id, value)
                mat_ref[constraint_row] = (row_id, col_id, value)
                if (value == e):
                    existing_rows.append(constraint_row)
                else:
                    other_rows.append(constraint_row)
    return existing_rows, other_rows, mat_ref


def solve_sudoku(sudoku_matrix):
    sudoku = [['0' for _ in range(9)] for _ in range(9)]

    existing_rows, other_rows, mat_ref = to_exact_cover(sudoku_matrix)
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

if __name__ == '__main__':
    moving_sum = 0
    for sudoku in load_sudoku():
        solved_sudoku = solve_sudoku(sudoku)
        val = int(''.join(solved_sudoku[0][:3]))
        moving_sum += val

    assert moving_sum == 24702