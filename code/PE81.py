# PROBLEM

# Find the minimal path sum, in matrix.txt (right click and "Save Link/Target As..."),
# a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by only moving right and down.

# ANSWER
# 427337

import copy


class Problem81:
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
        B = self.working_matrix
        n = self.n

        # Calculate the right side and bottom side
        for i in range(n):
            B[n - 1][n - 2 - i] += B[n - 1][n - 2 - i + 1]
            B[n - 2 - i][n - 1] += B[n - 2 - i + 1][n - 1]

        # All other numbers
        for i in range(n - 1):
            for j in range(n - 1):
                B[n - 2 - i][n - 2 - j] += min(B[n - 1 - i][n - 2 - j], B[n - 2 - i][n - 1 - j])

        return B[0][0]


if __name__ == "__main__":
    obj = Problem81(r'..\problem_data\p081_matrix.txt')
    sol = obj.solve()
    print(sol)
