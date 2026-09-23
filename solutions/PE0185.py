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
Solve time: ~0.26 seconds

Alternative / Experimental Solutions:
- Stochastic Hill Climbing / Local Search (~180 seconds):
  ../experimental_solutions/PE0185_simulated_annealing.py
- Recursive Backtracking with Constraint Propagation (~0.05s for 5-digit sample):
  ../experimental_solutions/PE0185_recursive.py
"""

import unittest
from typing import List, Tuple
import numpy as np
from scipy.optimize import milp, LinearConstraint
from util.utils import timeit


# Alternative solutions in the repository:
# - [`experimental_solutions/PE0185_simulated_annealing.py`](../experimental_solutions/PE0185_simulated_annealing.py):
#   Original randomized local search / hill-climbing solver (~180 seconds).
# - [`experimental_solutions/PE0185_recursive.py`](../experimental_solutions/PE0185_recursive.py):
#   Recursive depth-first search with heuristic probability sorting (~0.05s for 5-digit game).
#
# See also: https://github.com/raphey/number-mind
#
# MATHEMATICAL DERIVATION:
#
# 1. 0-1 Integer Linear Programming Formulation:
#    Let n be the number of digits in the secret sequence (n = 16).
#    Define binary decision variables x_{j, d} in {0, 1} for each position j in [0, n-1]
#    and digit d in [0, 9], where x_{j, d} = 1 if the j-th digit of the secret is d.
#
# 2. Constraints:
#    a) Unique digit per position:
#       sum_{d=0}^{9} x_{j, d} = 1   for each j in [0, n-1]   (n constraints)
#
#    b) Clue consistency:
#       For each attempt (guess g_i, count k_i):
#       sum_{j=0}^{n-1} x_{j, int(g_i[j])} = k_i              (m constraints)
#
# 3. Exact Solution via MILP:
#    This forms an exact system of (n + m) linear equality constraints on (10 * n) binary variables.
#    Solved deterministically via scipy.optimize.milp in ~0.26s.


class Problem185:
    def __init__(self, ls_attempts: List[Tuple[str, int]]):
        self.ls_attempts = [(str(g), int(k)) for g, k in ls_attempts]
        self.digits = len(self.ls_attempts[0][0])

    @timeit
    def solve(self) -> str:
        num_vars = self.digits * 10
        c = np.zeros(num_vars)
        a_rows = []
        b_vals = []

        # 1. Exactly one digit per position
        for j in range(self.digits):
            row = np.zeros(num_vars)
            row[j * 10:(j + 1) * 10] = 1
            a_rows.append(row)
            b_vals.append(1)

        # 2. Clue equality constraints
        for g, k in self.ls_attempts:
            row = np.zeros(num_vars)
            for j in range(self.digits):
                d = int(g[j])
                row[j * 10 + d] = 1
            a_rows.append(row)
            b_vals.append(k)

        a_mat = np.array(a_rows)
        b_vec = np.array(b_vals)
        constraints = LinearConstraint(a_mat, b_vec, b_vec)

        res = milp(c=c, integrality=np.ones(num_vars), constraints=constraints)
        if not res.success:
            raise ValueError("No consistent sequence found for the given clues.")

        sol_vars = np.round(res.x).astype(int)
        secret = []
        for j in range(self.digits):
            digit = np.argmax(sol_vars[j * 10:(j + 1) * 10])
            secret.append(str(digit))

        return ''.join(secret)


class Solution185(unittest.TestCase):
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
