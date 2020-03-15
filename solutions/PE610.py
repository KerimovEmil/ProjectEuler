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

ANSWER: Euler says the answer is still wrong
n=4: 1163.97561450
n=5: 1335.55436650
n=6: 1426.50414520 (~1.5 seconds)
n=7: 1469.04149634 (~2.5 seconds)
n=8: 1483.60117187  (~15.8 seconds) (options took 8 seconds, get_matrix tool 5.5 seconds) (3039 valid options)
n=9: 1487.92740977  (~65 seconds) (options took 52 seconds, get_matrix tool 8 seconds)  (4008 valid options)
n=10: 1488.9219717  (~26 seconds) (options took 0.5 seconds, get_matrix tool 18 seconds) (5001 valid options)
n=11: ____________   (~_ seconds) (options took __ seconds, get_matrix tool __ seconds) (6000 valid options)
n=12: ____________   (~_ seconds) (options took __ seconds, get_matrix tool __ seconds) (7000 valid options)
n=13: ____________   (~_ seconds) (options took __ seconds, get_matrix tool __ seconds) (8000 valid options)
n=14: 1489.16034837  (~73 seconds) (options took 0.4 seconds, get_matrix tool 33 seconds) (9000 valid options)
n=15: 1489.1604423  (~___ seconds) (options took 3.2 seconds, get_matrix tool __ seconds) (10000 valid options)
n=16: 1489.16045545  (~129 seconds) (options took 4.2 seconds, get_matrix tool 55 seconds) (11000 valid options)
n=17: 1489.16045729  (~160 seconds) (options took 0.6 seconds, get_matrix tool 62 seconds) (12000 valid options)
n=18: 1489.16045755  (~209 seconds) (options took 0.7 seconds, get_matrix tool 85 seconds) (13000 valid options)
n=19: 1489.16045759  (~247 seconds) (options took 0.77 seconds, get_matrix tool 103.6 seconds) (14000 valid options)
n=20: 1489.16045759  (~304 seconds) (options took 0.9 seconds, get_matrix tool 118 seconds) (15000 valid options)
...

pd.DataFrame([1163.97561450, 1335.55436650, 1426.50414520,1469.04149634, 1483.60117187, 1487.92740977,
              1488.9219717, 1489.16034837, 1489.1604423, 1489.16045545,   ]).plot()

Solve time ~ a bit too many seconds
"""

from util.utils import timeit
import unittest
import pandas as pd
import numpy as np
from solutions.PE89 import RomanNumeral

# for n in range(1, 10):
#     print(n, 1000*n*(0.14**n))

# 1 140.0
# 2 39.2
# 3 8.232000000000003
# 4 1.5366400000000007
# 5 0.2689120000000001
# 6 0.04517721600000003
# 7 0.0073789452800000046
# 8 0.001180631244800001
# 9 0.00018594942105600016
# 10 2.8925465497600025e-05
# 11 4.454521686630405e-06
# 12 6.803269485035528e-07
# 13 1.0318292052303885e-07
# 14 1.5556809555781244e-08

# n=14: 1489.16034837
# n=15: 1489.1604423 (+ 9.393000004820351e-05)
# n=16: 1489.16045545 (+ 1.3149999858796946e-05)


class ProbMatrix:

    @staticmethod
    @timeit
    def options(n=5):

        ls_tup = [
            ('M', n), ('CM', 1), ('D', 1), ('CD', 1), ('C', 3), ('XC', 1), ('L', 1), ('XL', 1), ('X', 3),
            ('IX', 1), ('V', 1), ('IV', 1), ('I', 3)]

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

        np_row = N_inv[0]

        print('Done computing termination state probability from starting state')
        # todo fix this, as we need to keep track of previous states as well, in the meantime just have many more states

        expected_value = sum(RomanNumeral.parse(state.strip()) * np_row[i] for i, state in enumerate(states))

        return expected_value


class Solution610(unittest.TestCase):
    def setUp(self):
        self.problem = Problem610()

    def test_solution_7(self):
        self.assertEqual(1469.04149634, round(self.problem.solve(n=7), 8))

    # def test_solution_14(self):
    #     self.assertEqual(1489.16034837, round(self.problem.solve(n=14), 8))

    def test_solution(self):
        self.assertEqual(None, round(self.problem.solve(n=20), 8))

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

