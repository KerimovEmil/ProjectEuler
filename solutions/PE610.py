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
n=15: 319.30206518  (~97 seconds) (options took 0.47 seconds, get_matrix tool 45 seconds) (10000 valid options)
n=19: 319.30207832  (~215 seconds) (options took 0.74 seconds, get_matrix tool 78 seconds) (14000 valid options)
n=20: 319.30207833  (~ seconds) (options took 0.9 seconds, get_matrix tool 98 seconds) (15000 valid options)
...

Solve time ~ a bit too many seconds
"""

from util.utils import timeit
import unittest
import pandas as pd
import numpy as np
from solutions.PE89 import RomanNumeral


class ProbMatrix:

    @staticmethod
    @timeit
    def options(n=5):

        ls_tup = [
            ('M', n), ('CM', 1), ('D', 1), ('CD', 1), ('C', 3), ('XC', 1), ('L', 1), ('XL', 1), ('X', 3),
            ('IX', 1), ('V', 1), ('IV', 1), ('I', 3)]

        # ls_tup = [
        #     ('CM', 1), ('D', 1), ('CD', 1), ('C', 3), ('XC', 1), ('L', 1), ('XL', 1), ('X', 3),
        #     ('IX', 1), ('V', 1), ('IV', 1), ('I', 3)]

        all_str_options = ProbMatrix.options_recursive(n=n, tup_available=ls_tup, ls_opts=[' '*n], input_string='')
        print('Generated options: {}'.format(len(all_str_options)))
        return all_str_options

    @staticmethod
    def options_recursive(n, tup_available, ls_opts, input_string):
        if n == 0:
            return []
        new_tup_available = [(k, v) for k, v in tup_available if v != 0]

        if len(new_tup_available) == 0:
            return []

        ls_opt_final = ls_opts
        for i, (char, sample) in enumerate(new_tup_available):
            if not RomanNumeral.isvalid(input_string + char):
                # filer out cases like 'IXIII' or 'IVIII' or 'IXI'
                continue
            char_left = n - len(char)
            if char_left < 0:
                continue

            if sample == 1:
                temp_tup_available = new_tup_available[i+1:].copy()
            else:
                temp_tup_available = new_tup_available[i:].copy()
                temp_tup_available[0] = (char, sample - 1)

            ls_opt_final += [' '*char_left + input_string + char] + ProbMatrix.options_recursive(
                n=char_left, ls_opts=[], tup_available=temp_tup_available, input_string=input_string+char)
        return ls_opt_final

    @staticmethod
    @timeit
    def get_matrix(n=4):
        options = ProbMatrix.options(n=n)

        ls_values = [[0.14 if c.startswith(row[1:]) else 0 for c in options] + [0.02] for row in options]
        ls_values.append([0]*len(options) + [1])  # termination state only maps to termination state
        # adjust first row
        assert options[0] == ' '*n
        ls_values[0][0] = 0  # ' '*n should not be able to go to ' '*n

        np_val = np.array(ls_values)
        # normalize each row
        np_prob = (np_val.T / np_val.sum(axis=1)).T
        print('Done computing the transition matrix')
        return np_prob, options


class Problem610:
    def __init__(self):
        pass

    @timeit
    def solve(self, n=4):
        prob_matrix, states = ProbMatrix.get_matrix(n=n)
        q_matrix = prob_matrix[:-1, :-1]

        N = np.eye(len(states)) - q_matrix
        print('starting to take the inverse')
        N_inv = np.linalg.inv(N)  # todo speed up, this is the bottleneck
        print('finished taking the inverse')

        # N_inv_approx = np.eye(len(states))
        # for i in range(5):
        #     N_inv_approx += N_inv_approx@q_matrix
        # print(abs(N_inv - N_inv_approx).sum())

        # prob(starting at ' '*n, ending at state_i)*prob(state_i, terminal state #)
        w = N_inv[0] * prob_matrix[:-1, -1]
        print('Done computing termination state probability from starting state')
        # todo fix this, as we need to keep track of previous states as well, in the meantime just have many more states

        # expected_value = sum(RomanNumeral.parse(state.strip()) * np_row[i] * prob_matrix[i, -1] for i, state in enumerate(states))
        expected_value = sum(RomanNumeral.parse(state.strip()) * w[i] for i, state in enumerate(states))

        return expected_value


class Solution610(unittest.TestCase):
    def setUp(self):
        self.problem = Problem610()

    # def test_solution_7(self):
    #     self.assertEqual(304.7424028, round(self.problem.solve(n=7), 8))

    def test_solution(self):
        self.assertEqual(319.30207833, round(self.problem.solve(n=10), 8))

    # def test_solution(self):
    #     self.assertEqual(319.30207833, round(self.problem.solve(n=20), 8))

    def test_option_generation(self):
        valid_options = set(ProbMatrix.options(n=5))
        self.assertTrue(' IIII' not in valid_options)
        self.assertTrue('  III' in valid_options)

    # def test_option_generation_speed(self):
    #     for n in range(1, 20):
    #         print('n = {}'.format(n))
    #         valid_options = ProbMatrix.options(n=n)

    def test_prob_matrix(self):
        np_prob_matrix, options = ProbMatrix.get_matrix(n=4)

        prob_matrix = pd.DataFrame(np_prob_matrix, index=options + ["#"], columns=options + ['#'])

        self.assertAlmostEqual(prob_matrix.loc[' MMM', 'MMMM'], 0.14, 10)
        self.assertAlmostEqual(prob_matrix.loc['   V', '  VI'], 7/8, 10)
        self.assertAlmostEqual(prob_matrix.loc['  II', ' III'], 7/8, 10)
        self.assertAlmostEqual(prob_matrix.loc['    ', '   M'], 0.14, 10)
        self.assertAlmostEqual(prob_matrix.loc['#', '#'], 1, 10)


if __name__ == '__main__':
    unittest.main()

