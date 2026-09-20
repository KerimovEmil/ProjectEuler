"""
PROBLEM

In the game, Monopoly, the standard board is set up in the following way: p084_monopoly_board.png

A player starts on the GO square and adds the scores on two 6-sided dice to determine the number of squares they advance
 in a clockwise direction. Without any further rules we would expect to visit each square with equal probability: 2.5%.
 However, landing on G2J (Go To Jail), CC (community chest), and CH (chance) changes this distribution.

In addition to G2J, and one card from each of CC and CH, that orders the player to go directly to jail, if a player
rolls three consecutive doubles, they do not advance the result of their 3rd roll.
Instead, they proceed directly to jail.

At the beginning of the game, the CC and CH cards are shuffled. When a player lands on CC or CH they take a card from
the top of the respective pile and, after following the instructions, it is returned to the bottom of the pile.
There are sixteen cards in each pile, but for the purpose of this problem we are only concerned with cards that order a
 movement; any instruction not concerned with movement will be ignored and the player will remain on the CC/CH square.

Community Chest (2/16 cards):
-Advance to GO
-Go to JAIL

Chance (10/16 cards):
-Advance to GO
-Go to JAIL
-Go to C1
-Go to E3
-Go to H2
-Go to R1
-Go to next R (railway company)
-Go to next R
-Go to next U (utility company)
-Go back 3 squares.

The heart of this problem concerns the likelihood of visiting a particular square. That is, the probability of finishing
at that square after a roll. For this reason it should be clear that, with the exception of G2J for which the
probability of finishing on it is zero, the CH squares will have the lowest probabilities, as 5/8 request a movement to
another square, and it is the final square that the player finishes at on each roll that we are interested in. We
shall make no distinction between "Just Visiting" and being sent to JAIL, and we shall also ignore the rule about
requiring a double to "get out of jail", assuming that they pay to get out on their next turn.

By starting at GO and numbering the squares sequentially from 00 to 39 we can concatenate these two-digit numbers to
produce strings that correspond with sets of squares.

Statistically it can be shown that the three most popular squares, in order, are JAIL (6.24%) = Square 10, E3 (3.18%) =
Square 24, and GO (3.09%) = Square 00. So these three most popular squares can be listed with the six-digit modal
string: 102400.

If, instead of using two 6-sided dice, two 4-sided dice are used, find the six-digit modal string.

ANSWER: 101524
Solve time: ~0.002 seconds
"""
from util.utils import timeit
import unittest
import numpy as np


class Problem84:
    def __init__(self):
        self.total = 40
        self.squares = [i for i in range(self.total)]
        self.community_chest = [2, 17, 33]
        self.chance = [7, 22, 36]
        self.go_to_jail = [30]
        self.jail = 10
        self.railway = [5, 15, 25, 35]
        self.ls_utility = [12, 28]

        self.transition_matrix = np.zeros((self.total, self.total))

    @staticmethod
    def get_all_rolls(die_sides):
        for r1 in range(1, die_sides + 1):  # roll 1
            for r2 in range(1, die_sides + 1):  # roll 2
                yield r1, r2

    def create_transition_matrix(self, die_sides=6):
        """
        Create transition matrix.
        Note that this implementation ignores the 3-doubles in a row rule for jail.
        """
        # create basic transition matrix
        for s in range(self.total):  # each square
            for r1, r2 in self.get_all_rolls(die_sides=die_sides):
                next_pos = (s + r1 + r2) % self.total
                prob = 1 / (die_sides*die_sides)
                self.transition_matrix[s, next_pos] += prob

        # handle special cases
        for cc in self.community_chest:
            self.transition_matrix[cc, :] = self.transition_matrix[cc, :] * 14 / 16  # 14/16 elsewhere
            self.transition_matrix[cc, self.jail] += 1 / 16  # 1/16 go to jail
            self.transition_matrix[cc, 0] += 1 / 16  # 1/16 advance to go

        for cc in self.chance:
            self.transition_matrix[cc, :] = self.transition_matrix[cc, :] * 6 / 16  # 6/16 elsewhere
            self.transition_matrix[cc, 0] += 1 / 16  # go
            self.transition_matrix[cc, self.jail] += 1 / 16  # go to jail
            self.transition_matrix[cc, 11] += 1 / 16  # C1
            self.transition_matrix[cc, 24] += 1 / 16  # E3
            self.transition_matrix[cc, 39] += 1 / 16  # H2
            self.transition_matrix[cc, 5] += 1 / 16  # R1
            self.transition_matrix[cc, (cc - 3) % self.total] += 1 / 16  # go back 3 squares
            self.transition_matrix[cc, (((cc - 5) // 10) * 10 + 15) % self.total] += 2/16  # Go to next R (railway company)

            u1, u2 = self.ls_utility[0], self.ls_utility[1]
            next_u = u2 if u1 < cc < u2 else u1
            self.transition_matrix[cc, next_u] += 1 / 16  # Go to next U (utility company)

        for cc in self.go_to_jail:
            self.transition_matrix[cc, :] = 0
            self.transition_matrix[cc, self.jail] = 1

        assert abs(self.transition_matrix.sum() - self.total) < 1e-10

    @timeit
    def solve(self, die_sides=6, top=3):
        self.create_transition_matrix(die_sides=die_sides)

        # calculating the steady state probabilities
        eig_val, eig_vec = np.linalg.eig(self.transition_matrix.T)
        eig_vec = eig_vec[:, np.isclose(eig_val, 1)]
        pi = eig_vec / eig_vec.sum()

        # get top squares
        top = sorted(range(len(pi)), key=lambda x: pi[x])[-top:][::-1]

        ans = ''
        for i in top:
            # print(f'Square {i}, has a probability of {pi[i][0].real:%}')
            ans += f'{i:02}'

        return ans


class Solution84(unittest.TestCase):
    def setUp(self):
        self.problem = Problem84()

    def test_6_dice_solution(self):
        self.assertEqual('102400', self.problem.solve(die_sides=6, top=3))

    def test_4_dice_solution(self):
        self.assertEqual('101524', self.problem.solve(die_sides=4, top=3))


if __name__ == '__main__':
    unittest.main()
