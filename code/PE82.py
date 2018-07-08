# PROBLEM

# Find the minimal path sum, in matrix.txt (right click and "Save Link/Target As..."),
# a 31K text file containing a 80 by 80 matrix, from the left column to the right column.

# ANSWER
# 260324

import copy


class Problem82:
    def __init__(self, data_path):
        self.problem_data = []
        self.load_data(data_path)
        self.n = len(self.problem_data)
        self.working_matrix = copy.deepcopy(self.problem_data)

    def load_data(self, data_path):
        f = open(data_path, 'r')
        for line in f:
            w = line.split(',')
            w = [int(x) for x in w]
            self.problem_data.append(w)

    def solve(self):
        a = self.problem_data
        B = self.working_matrix
        n = self.n

        for j in range(n - 1):  # loop over n-1 cols
            col = n - 2 - j  # dynamic programming
            # Loop over all rows
            for i in range(n):
                row = i

                # right
                m = B[row][col + 1]

                for loop_row in range(n):
                    s = B[loop_row][col + 1]

                    if loop_row > row:  # upper
                        for sum_row in range(row + 1, loop_row + 1):
                            s += a[sum_row][col]
                    elif loop_row < row:  # lower
                        for sum_row in range(loop_row, row):
                            s += a[sum_row][col]

                    m = min(m, s)

                B[row][col] += m

        return min([x[0] for x in B])


if __name__ == "__main__":
    obj = Problem82(r'..\problem_data\p082_matrix.txt')
    sol = obj.solve()
    print(sol)
