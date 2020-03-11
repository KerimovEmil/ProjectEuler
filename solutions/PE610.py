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

ANSWER:
1163.97561450 (??? Euler saying it's wrong)
Solve time ~  seconds
"""

from util.utils import timeit
import unittest
import pandas as pd
import numpy as np
from solutions.PE89 import RomanNumeral


class ProbMatrix:
    OPTIONS = ['M', 'D', 'C', 'L', 'X', 'V', 'I', ' ']

    @staticmethod
    def options():
        all_options = []
        for opt1 in ProbMatrix.OPTIONS:
            for opt2 in ProbMatrix.OPTIONS:
                if opt2 == ' ' and opt1 != ' ':
                    continue
                for opt3 in ProbMatrix.OPTIONS:
                    if opt3 == ' ' and opt2 != ' ':
                        continue
                    for opt4 in ProbMatrix.OPTIONS:
                        if opt4 == ' ' and opt3 != ' ':
                            continue

                        string = opt1 + opt2 + opt3 + opt4
                        all_options.append(string)

        valid_options = [x for x in all_options if RomanNumeral.isvalid(x)]
        return valid_options

    @staticmethod
    def get_matrix():
        options = ProbMatrix.options()
        df = pd.DataFrame(0, index=options + ["#"], columns=options + ['#'])
        df[['#']] = 0.02
        df.loc['#', '#'] = 1
        for row in options:
            rowsub = row[-3:]
            for col in options:
                if col.startswith(rowsub):
                    df.loc[row, col] = 0.14
        df.loc['    ', '    '] = 0
        return df.divide(df.sum(axis=1), axis=0)


class Problem610:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        prob_matrix = ProbMatrix.get_matrix()
        q_matrix = prob_matrix.drop('#', axis=1)
        q_matrix = q_matrix.drop('#', axis=0)
        eye = pd.DataFrame(np.eye(len(q_matrix.index)), index=q_matrix.index, columns=q_matrix.columns)
        N = eye - q_matrix
        N_inv = np.linalg.inv(N.values)
        df_N_inv = pd.DataFrame(N_inv, index=q_matrix.index, columns=q_matrix.columns)

        df_terminal = df_N_inv.loc[['    ']]  # expected last value before termination given started at '    '
        expected_value = 0
        for state in df_terminal.columns:
            expected_value += RomanNumeral.parse(state.strip()) * df_terminal.loc['    ', state]

        return expected_value


class Solution610(unittest.TestCase):
    def setUp(self):
        self.problem = Problem610()

    def test_solution(self):
        self.assertEqual(None, self.problem.solve())

    def test_option_generation(self):
        valid_options = set(ProbMatrix.options())
        self.assertTrue('IIII' not in valid_options)
        self.assertTrue(' III' in valid_options)

    def test_prob_matrix(self):
        prob_matrix = ProbMatrix.get_matrix()
        self.assertAlmostEqual(prob_matrix.loc[' MMM', 'MMMM'], 0.14, 10)
        self.assertAlmostEqual(prob_matrix.loc['   V', '  VI'], 7/8, 10)
        self.assertAlmostEqual(prob_matrix.loc['  II', ' III'], 7/8, 10)
        self.assertAlmostEqual(prob_matrix.loc['    ', '   M'], 0.14, 10)
        self.assertAlmostEqual(prob_matrix.loc['#', '#'], 1, 10)


if __name__ == '__main__':
    unittest.main()

