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
Solve time: ~0.58 seconds
"""

import numpy as np

import unittest
from solutions.PE89 import RomanNumeral
from util.utils import timeit


# Idea:
#   Each roman numeral can be written as starting_portion + ending_portion
#   Where starting_portion is empty or some number of 'M's, and ending_portion is under the value of 1000
#   The key to note is that the ending_portion requires the construction of a Markov chain, the start_portion does not.

# We construct the transition matrix of all the roman numerals that do not start with M (i.e. less than 1000).

# Computation references:
# 1) Given the eigenvalues of S are < 1 (Non-absorbing Probability transition matrices have this property). Then
#    N = I + S + S^2 + S^3 + ...
#   SN =     S + S^2 + s^3 + ...
#   (I-S)N = I
#   N = (I-S)^-1

# 2) If the markov chain state is described as s_{t+1} = Q * s_{t} then
# The probability of starting at state i and ending at the j after k moves = (Q^k)_{i, j}
# The probability of being terminated ending at state j after starting at state i, and after k+1 moves is:
#   (Q^k)_{i, j} * Q_{j, termination}

# 3) For all numbers less than 1000, we need to compute the following:
#  ANSWER = sum_{k moves} sum_{j states} (Q^k)_{starting_state = '', j} * Q_{j, termination} * Roman_value_of_state_j
# using equation 1 we can remove the sum over k moves by computing the infinite sum of matrix powers:
#  ANSWER = sum_{j states} sum_{k moves} (Q^k)_{starting_state = '', j} * Q_{j, termination} * Roman_value_of_state_j
#  ANSWER = sum_{j states} ((I-Q)^-1)_{starting_state = '', j} * Q_{j, termination} * Roman_value_of_state_j

# 4) Accounting for the sequences that start with some sequence of 'M's
#  all roman numerals = ('' or 'M' or 'MM' or 'MMM' or 'MMMM' or ....) + ending_portion
#  where ending_portion is less than 1000.
# The expected value added if our initial sequence began with 'M' is 0.14*1000
# The expected value added if our initial sequence has another 'M' after one 'M' is 0.14^2*1000
# The expected value added if our initial sequence has another 'M' after two 'M's is 0.14^3*1000
# Since for each M we gain a value of 1000 but it is weighted with a smaller probability
# Therefore:
# Expected value = (0 + 1000*0.14 + 1000*0.14^2 + 1000*0.14^3 + ...) + ExpectedValue(ending_portion)
# using 1000 * (0.14 + 0.14^2 + 0.14^3 + ...) = 1000*0.14/(1-0.14) we get
# Expected value = 1000*0.14/(1-0.14) + ExpectedValue(ending_portion)

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
        expected_value = sum(RomanNumeral.parse(state) * w[i] for i, state in enumerate(states))

        # The expected value added of all roman numerals that start with M are 1000*0.14/(1-0.14)
        return expected_value + 1000 * 0.14 / (1 - 0.14)


class Solution610(unittest.TestCase):
    def setUp(self):
        self.problem = Problem610()

    def test_solution(self):
        self.assertEqual(319.30207833, round(self.problem.solve(), 8))


if __name__ == '__main__':
    unittest.main()
