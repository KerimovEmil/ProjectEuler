"""
PROBLEM

The game Number Mind is a variant of the well known game Master Mind.
Instead of coloured pegs, you have to guess a secret sequence of digits.
After each guess you're only told in how many places you've guessed the correct digit.
So, if the sequence was 1234 and you guessed 2036, you'd be told that you have one correct digit;
however, you would NOT be told that you also have another digit in the wrong place.

For instance, given the following guesses for a 5-digit secret sequence,

90342 ;2 correct
70794 ;0 correct
39458 ;2 correct
34109 ;1 correct
51545 ;2 correct
12531 ;1 correct

The correct sequence 39542 is unique.

Based on the following guesses,

5616185650518293 ;2 correct
3847439647293047 ;1 correct
5855462940810587 ;3 correct
9742855507068353 ;3 correct
4296849643607543 ;3 correct
3174248439465858 ;1 correct
4513559094146117 ;2 correct
7890971548908067 ;3 correct
8157356344118483 ;1 correct
2615250744386899 ;2 correct
8690095851526254 ;3 correct
6375711915077050 ;1 correct
6913859173121360 ;1 correct
6442889055042768 ;2 correct
2321386104303845 ;0 correct
2326509471271448 ;2 correct
5251583379644322 ;2 correct
1748270476758276 ;3 correct
4895722652190306 ;1 correct
3041631117224635 ;3 correct
1841236454324589 ;3 correct
2659862637316867 ;2 correct

Find the unique 16-digit secret sequence.

ANSWER: 4640261571849533
Solve time: ~21 seconds to 3 minutes
"""

# See many possible algorithm solutions to this here: https://github.com/raphey/number-mind

import unittest
from util.utils import timeit
import random


def solution_distance(pos_sol, guess, correct):
    return abs(sum([x == y for (x, y) in zip(pos_sol, guess)]) - correct)


def check_all_guesses(ls_attempts, possible_sol):
    dist = 0
    for attempt in ls_attempts:
        guess = attempt[0]
        num_corr = attempt[1]
        dist += solution_distance(possible_sol, guess, num_corr)
    return dist


def mutate_guess(old_guess):
    rand_index = random.randint(0, len(old_guess) - 1)
    return mutate_guess_i(old_guess, rand_index)


def mutate_guess_i(old_guess, i):
    """randomly mutate single element in string"""
    ls_old_guess = list(old_guess)
    rand_value = str(random.randint(0, 9))
    ls_old_guess[i] = rand_value
    return ''.join(ls_old_guess)


class Problem185:
    def __init__(self, ls_attempts):
        self.ls_attempts = ls_attempts
        self.max_try_wo_improvement = 10
        self.digits = len(self.ls_attempts[0][0])

    def solve_attempt(self):
        best_guess = ''.join([str(random.randint(0, 9)) for _ in range(self.digits)])
        min_dist = check_all_guesses(self.ls_attempts, best_guess)
        if min_dist == 0:
            return best_guess, min_dist
        w = self.max_try_wo_improvement
        # print("Trying new seed")
        while w > 0:
            w -= 1
            indexes = list(range(self.digits))
            random.shuffle(indexes)
            for i in indexes:
                possible_sol = mutate_guess_i(best_guess, i)
                dist = check_all_guesses(self.ls_attempts, possible_sol)
                if dist < min_dist:
                    # print(min_dist, best_guess)
                    min_dist = dist
                    w = self.max_try_wo_improvement
                    best_guess = possible_sol
                    if min_dist == 0:
                        return best_guess, min_dist

        return best_guess, min_dist

    @timeit
    def solve(self):
        min_dist = self.digits * len(self.ls_attempts)
        is_solved = False
        while is_solved is False:
            best_guess, dist = self.solve_attempt()
            if dist < min_dist:
                min_dist = dist
                print(min_dist, best_guess)
            if dist == 0:
                return best_guess


class Solution185(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_solution_small(self):

        ls_attempts = [
            (90342, 2),
            (70794, 0),
            (39458, 2),
            (34109, 1),
            (51545, 2),
            (12531, 1),
        ]
        ls_attempts_str = [(str(x), y) for (x, y) in ls_attempts]
        problem = Problem185(ls_attempts_str)
        self.assertEqual('39542', problem.solve())

    def test_solution(self):
        ls_attempts = [
            (5616185650518293, 2),
            (3847439647293047, 1),
            (5855462940810587, 3),
            (9742855507068353, 3),
            (4296849643607543, 3),
            (3174248439465858, 1),
            (4513559094146117, 2),
            (7890971548908067, 3),
            (8157356344118483, 1),
            (2615250744386899, 2),
            (8690095851526254, 3),
            (6375711915077050, 1),
            (6913859173121360, 1),
            (6442889055042768, 2),
            (2321386104303845, 0),
            (2326509471271448, 2),
            (5251583379644322, 2),
            (1748270476758276, 3),
            (4895722652190306, 1),
            (3041631117224635, 3),
            (1841236454324589, 3),
            (2659862637316867, 2)
        ]

        ls_attempts_str = [(str(x), y) for (x, y) in ls_attempts]
        problem = Problem185(ls_attempts_str)
        self.assertEqual('4640261571849533', problem.solve())


if __name__ == '__main__':
    unittest.main()
