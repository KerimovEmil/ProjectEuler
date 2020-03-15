"""
PROBLEM

A random generator produces a sequence of symbols drawn from the set {I, V, X, L, C, D, M, #}.
Each item in the sequence is determined by selecting one of these symbols at random, independently of the other items
in the sequence. At each step, the seven letters are equally likely to be selected, with probability 14% each, but
the # symbol only has a 2% chance of selection.

We write down the sequence of letters from left to right as they are generated, and we stop at the first occurrence
of the # symbol (without writing it). However, we stipulate that what we have written down must always (when non-empty)
 be a valid Roman numeral representation in minimal form. If appending the next letter would contravene this then we
 simply skip it and try again with the next symbol generated.

Please take careful note of About... Roman Numerals for the definitive rules for this problem on what constitutes a
"valid Roman numeral representation" and "minimal form". For example, the (only) sequence that represents 49 is XLIX.
 The subtractive combination IL is invalid because of rule (ii), while XXXXIX is valid but not minimal. The rules do
 not place any restriction on the number of occurrences of M, so all positive integers have a valid representation.
  These are the same rules as were used in Problem 89, and members are invited to solve that problem first.

Find the expected value of the number represented by what we have written down when we stop. (If nothing is written
down then count that as zero.) Give your answer rounded to 8 places after the decimal point.

ANSWER: 319.30207833

Solve time ~0.58 seconds
"""

from util.utils import timeit
import unittest
import numpy as np
from solutions.PE89 import RomanNumeral


class Problem610:
    def __init__(self):
        pass

    @staticmethod
    @timeit
    def get_transition_matrix():
        # Get all Roman Numerals less than 1000 (not starting with M)
        options = [RomanNumeral.construct(n) for n in range(1000)]

        ls_values = [[0.14 if c[:-1] == row else 0 for c in options] + [0.02] for row in options]
        ls_values.append([0] * len(options) + [1])  # termination state only maps to termination state
        # adjust first row (starting position)
        ls_values[0][0] = 0  # ' ' should not be able to go to ' '

        np_val = np.array(ls_values)
        # normalize each row
        np_prob = (np_val.T / np_val.sum(axis=1)).T
        print('Done computing the transition matrix')
        return np_prob, options

    @timeit
    def solve(self):
        prob_matrix, states = self.get_transition_matrix()
        # Get non-absorbing sub-matrix
        q_matrix = prob_matrix[:-1, :-1]

        # sum_{n=0}^{inf} Q^n = (I-Q)^-1
        inf_sum_q = np.linalg.inv(np.eye(len(states)) - q_matrix)

        # prob(starting at '', ending at state_i)*prob(state_i, terminal state #)
        w = inf_sum_q[0] * prob_matrix[:-1, -1]

        # The value of all roman numerals that don't start with M
        expected_value = sum(RomanNumeral.parse(state.strip()) * w[i] for i, state in enumerate(states))

        # The expected value added of all roman numerals that start with M are 1000*0.14/(1-0.14)
        return expected_value + 1000*0.14/(1-0.14)


class Solution610(unittest.TestCase):
    def setUp(self):
        self.problem = Problem610()

    def test_solution(self):
        self.assertEqual(319.30207833, round(self.problem.solve(), 8))


if __name__ == '__main__':
    unittest.main()
