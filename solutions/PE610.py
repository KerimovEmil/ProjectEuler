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
n=4: 1163.97561450
n=5: 1335.55436650
n=6: 1426.50414520 (~1.5 seconds)
n=7: 1469.04149634
n=8: 1483.60117187  (~15.8 seconds) (options took 8 seconds, get_matrix tool 5.5 seconds)
n=9: 1487.92740977  (~65 seconds) (options took 52 seconds, get_matrix tool 8 seconds)
...
n=big_enough_number: ...

pd.DataFrame([1163.97561450, 1335.55436650, 1426.50414520,1469.04149634, 1483.60117187, 1487.92740977 ]).plot()

Solve time ~ a bit too many seconds
"""

from util.utils import timeit
import unittest
import pandas as pd
import numpy as np
from solutions.PE89 import RomanNumeral
from itertools import product
from itertools import combinations


class ProbMatrix:
    OPTIONS = ['M', 'D', 'C', 'L', 'X', 'V', 'I', ' ']

    @staticmethod
    @timeit
    def options(n=5):  # todo, speed up whole function, this is bottle neck

        dc = {' ': n, 'M': n, 'CM': 1, 'D': 1, 'CD': 1, 'C': 3, 'XC': 1, 'L': 1, 'XL': 1,
              'X': 3, 'IX': 1, 'V': 1, 'IV': 1, 'I': 3}
        raw_all_options = ''.join([k*v for k, v in dc.items()])
        all_options = set(combinations(raw_all_options, n))

        # all_options = list(product(ProbMatrix.OPTIONS, repeat=n))
        # all_str_options = [''.join(x) for x in product(ProbMatrix.OPTIONS, repeat=n)]
        all_str_options = [''.join(x) for x in all_options]
        # filter out incorrect space cases
        all_str_options = [x for x in all_str_options if ' ' not in x.lstrip()]

        print('Generated options')
        valid_options = [x for x in all_str_options if RomanNumeral.isvalid(x)]  # todo speed up, this is one bottle neck
        print('Generated valid options')
        return valid_options

    @staticmethod
    @timeit
    def get_matrix(n=4):
        options = ProbMatrix.options(n=n)

        ls_values = []
        for row in options:
            rowsub = row[1:]

            vals = [0.14 if c.startswith(rowsub) else 0 for c in options] + [0.02]
            ls_values.append(vals)
        ls_values.append([0]*len(options) + [1])

        df = pd.DataFrame(ls_values, index=options + ["#"], columns=options + ['#'])

        starting = ' '*n
        df.loc[starting, starting] = 0
        print('Done computing the transition matrix')
        return df.divide(df.sum(axis=1), axis=0)


class Problem610:
    def __init__(self):
        pass

    @timeit
    def solve(self, n=4):
        prob_matrix = ProbMatrix.get_matrix(n=n)
        q_matrix = prob_matrix.drop('#', axis=1)
        q_matrix = q_matrix.drop('#', axis=0)
        states = q_matrix.index

        eye = pd.DataFrame(np.eye(len(states)), index=states, columns=states)
        N = eye - q_matrix
        N_inv = np.linalg.inv(N.values)
        df_N_inv = pd.DataFrame(N_inv, index=states, columns=states)

        starting_state = ' '*n

        expected_value = 0
        print(len(states))
        # todo fix this, as we need to keep track of previous states as well, in the meantime just have many more states
        for state in states:
            expected_value += RomanNumeral.parse(state.strip()) * df_N_inv.loc[starting_state, state]

        return expected_value


class Solution610(unittest.TestCase):
    def setUp(self):
        self.problem = Problem610()

    def test_solution_6(self):
        self.assertEqual(1426.50414520, round(self.problem.solve(n=6), 8))

    def test_solution_8(self):
        self.assertEqual(1483.60117187, round(self.problem.solve(n=8), 8))
        # n=8: 1483.60117187  (~328 seconds)

    def test_solution_9(self):
        self.assertEqual(1487.92740977, round(self.problem.solve(n=9), 8))

    def test_option_generation(self):
        valid_options = set(ProbMatrix.options(n=5))
        self.assertTrue(' IIII' not in valid_options)
        self.assertTrue('  III' in valid_options)

    def test_prob_matrix(self):
        prob_matrix = ProbMatrix.get_matrix(n=4)
        self.assertAlmostEqual(prob_matrix.loc[' MMM', 'MMMM'], 0.14, 10)
        self.assertAlmostEqual(prob_matrix.loc['   V', '  VI'], 7/8, 10)
        self.assertAlmostEqual(prob_matrix.loc['  II', ' III'], 7/8, 10)
        self.assertAlmostEqual(prob_matrix.loc['    ', '   M'], 0.14, 10)
        self.assertAlmostEqual(prob_matrix.loc['#', '#'], 1, 10)


if __name__ == '__main__':
    unittest.main()

