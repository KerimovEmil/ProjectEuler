"""
PROBLEM

Find the minimal path sum from the top left to the bottom right by moving left, right, up, and down in matrix.txt
a 31K text file containing a 80 by 80 matrix.

ANSWER: 425185
Solve time: ~0.9 seconds
Related problems: 81, 82
"""
import os
from util.utils import timeit
import unittest


class Problem83:
    def __init__(self, data_path):
        self.problem_data = self.load_data(data_path, max_row=None)

        self.len_rows = len(self.problem_data)
        self.len_cols = len(self.problem_data[0])

        self.min_cost_path_matrix = [[None for _ in range(self.len_cols)] for _ in range(self.len_rows)]

    @staticmethod
    def load_data(data_path, max_row=None):
        with open(data_path, 'r') as f:
            problem_data = [[int(n) for n in s.split(',')] for s in f.readlines()]

        if max_row is None:
            return problem_data
        else:
            return [x[:max_row] for x in problem_data[:max_row]]

    def is_valid_move(self, new: tuple) -> bool:
        if new[0] < 0:  # above grid
            return False
        elif new[0] == self.len_rows:  # below grid
            return False
        if new[1] < 0:  # left of grid
            return False
        elif new[1] == self.len_cols:  # right of grid
            return False
        else:
            return True

    def is_good_move(self, current_cost: int, new: tuple) -> bool:
        new_path_cost = self.min_cost_path_matrix[new[0]][new[1]]
        if new_path_cost is None:
            return True
        new_cost = self.problem_data[new[0]][new[1]]

        if (new_cost + current_cost) < new_path_cost:
            return True

        return False

    def populate(self, pos_row, pos_col, prev_cost):
        current_cost = prev_cost + self.problem_data[pos_row][pos_col]
        # print(f'row:{pos_row}, col:{pos_col}, cost:{current_cost}')
        self.min_cost_path_matrix[pos_row][pos_col] = current_cost

        ls_moves = []

        # go up
        if self.is_valid_move(new=(pos_row - 1, pos_col)):
            if self.is_good_move(current_cost=current_cost, new=(pos_row - 1, pos_col)):
                # self.populate(pos_row=pos_row - 1, pos_col=pos_col, prev_cost=current_cost)
                ls_moves.append((pos_row - 1, pos_col, current_cost))

        # go down
        if self.is_valid_move(new=(pos_row + 1, pos_col)):
            if self.is_good_move(current_cost=current_cost, new=(pos_row + 1, pos_col)):
                # self.populate(pos_row=pos_row + 1, pos_col=pos_col, prev_cost=current_cost)
                ls_moves.append((pos_row + 1, pos_col, current_cost))

        # go left
        if self.is_valid_move(new=(pos_row, pos_col - 1)):
            if self.is_good_move(current_cost=current_cost, new=(pos_row, pos_col - 1)):
                # self.populate(pos_row=pos_row, pos_col=pos_col - 1, prev_cost=current_cost)
                ls_moves.append((pos_row, pos_col-1, current_cost))

        # go right
        if self.is_valid_move(new=(pos_row, pos_col + 1)):
            if self.is_good_move(current_cost=current_cost, new=(pos_row, pos_col + 1)):
                # self.populate(pos_row=pos_row, pos_col=pos_col + 1, prev_cost=current_cost)
                ls_moves.append((pos_row, pos_col + 1, current_cost))

        return ls_moves

    @staticmethod
    def prune_moves(ls_moves):
        ls_filtered_moves = []
        for move in ls_moves:
            move_in_filtered_move = False
            for f_move in ls_filtered_moves:
                if f_move[0] == move[0] and f_move[1] == move[1]:
                    move_in_filtered_move = True

                    move_better_than_f_move = move[2] < f_move[2]
                    if move_better_than_f_move:
                        remove_f_move = f_move

            if not move_in_filtered_move:
                ls_filtered_moves.append(move)
            if move_in_filtered_move and move_better_than_f_move:
                ls_filtered_moves.remove(remove_f_move)
                ls_filtered_moves.append(move)

        return ls_filtered_moves

    @timeit
    def solve(self):
        # top left
        row_start, col_start = 0, 0
        # bottom right
        row_end, col_end = self.len_rows - 1, self.len_cols - 1

        # generate min_cost_path_matrix matrix
        ls_moves = [(row_start, col_start, 0)]
        while len(ls_moves) != 0:
            ls_new_moves = []
            for move in ls_moves:
                ls_new_moves.extend(self.populate(pos_row=move[0], pos_col=move[1], prev_cost=move[2]))

            # print(f'new moves:{ls_new_moves}')
            pruned_new_moves = self.prune_moves(ls_new_moves)
            # print(f'new pruned moves:{pruned_new_moves}')
            ls_moves = pruned_new_moves

        return self.min_cost_path_matrix[row_end][col_end]


class Solution83(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p083_matrix.txt')
        self.problem = Problem83(file_path)

    def test_solution(self):
        self.assertEqual(425185, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

