from util.utils import timeit
import unittest


class Reversi:
    def __init__(self, n=5):
        self.n = n

        self.ls_position = self.get_starting_position()

    def get_starting_position(self) -> list[list[bool]]:

        ls_position = []

        for x in range(self.n):
            ls_position.append([])
            for y in range(self.n):
                d = (x ** 2 + y ** 2) ** 0.5
                if self.n - 1 <= d < self.n:
                    ls_position[x].append(True)
                else:
                    ls_position[x].append(False)

        return ls_position

    def __str__(self):
        output = ''
        for x in range(len(self.ls_position)):
            for y in range(len(self.ls_position[0])):
                if self.ls_position[x][y]:
                    # print('x', end=' ')
                    output += 'x'
                else:
                    # print('_', end=' ')
                    output += '_'
                output += ' '
            # print('')
            output += '\n'
        return output

    def flip(self, x, y):
        # flip row
        for i in range(self.n):
            self.ls_position[x][i] = not self.ls_position[x][i]

        # flip column
        for i in range(self.n):
            self.ls_position[i][y] = not self.ls_position[i][y]

        # flip piece
        self.ls_position[x][y] = not self.ls_position[x][y]


class Problem331:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution331(unittest.TestCase):
    def setUp(self):
        self.problem = Problem331()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

