"""
PROBLEM

A bag contains one red disc and one blue disc. In a game of chance a player takes a disc at random and its
colour is noted. After each turn the disc is returned to the bag, an extra red disc is added, and another
disc is taken at random.

The player pays 1 pound to play and wins if they have taken more blue discs than red discs at the end of the game.

If the game is played for four turns, the probability of a player winning is exactly 11/120, and so the maximum
prize fund the banker should allocate for winning in this game would be 10 pounds before they would expect to
incur a loss. Note that any payout will be a whole number of pounds and also includes the original 1 pound paid
to play the game, so in the example given the player actually wins 9 pounds.

Find the maximum prize fund that should be allocated to a single game in which fifteen turns are played.

ANSWER: 2269
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Probability Generating Function and Unsigned Stirling Numbers of the First Kind:
   On turn k (for k = 1, 2, ..., n), the bag contains 1 blue disc and k red discs, for a total of k + 1 discs.
   Thus, on turn k:
     P(blue on turn k) = 1 / (k + 1),   P(red on turn k) = k / (k + 1).
   Across all n independent turns, the common denominator of the probability distribution is:
     prod_{k=1}^n (k + 1) = (n + 1)!.
   The numerator polynomial tracking the number of blue discs drawn is:
     P_n(x) = prod_{k=1}^n (x + k) = sum_{b=0}^n c(n + 1, b + 1) * x^b,
   where [x^b] P_n(x) = c(n + 1, b + 1) is the unsigned Stirling number of the first kind (the sum of products
   of (n - b) distinct integers chosen from {1, 2, ..., n}).

2. Winning Probability and Maximum Prize Fund:
   The player wins if and only if the number of blue discs b strictly exceeds the number of red discs n - b,
   i.e., b >= floor(n / 2) + 1.
   Therefore, the exact probability of winning is:
     p_win = W_n / (n + 1)!,   where W_n = sum_{b = floor(n / 2) + 1}^n [x^b] P_n(x).
   For the banker not to incur an expected loss when paying prize M with probability p_win (given a 1-pound entry fee):
     M * p_win <= 1   <=>   M <= floor(1 / p_win) = floor((n + 1)! / W_n).
"""

import math
import unittest
from util.utils import timeit


class Problem121:
    def __init__(self, turns: int = 15):
        self.turns = turns

    @staticmethod
    def max_prize_fund(turns: int) -> int:
        poly = [1]
        for k in range(1, turns + 1):
            next_poly = [0] * (len(poly) + 1)
            for b, coeff in enumerate(poly):
                next_poly[b + 1] += coeff      # Draw blue disc (weight 1)
                next_poly[b] += coeff * k      # Draw red disc (weight k)
            poly = next_poly

        winning_numer = sum(poly[turns // 2 + 1:])
        total_denom = math.factorial(turns + 1)
        return total_denom // winning_numer

    @timeit
    def solve(self) -> int:
        return self.max_prize_fund(self.turns)


class Solution121(unittest.TestCase):
    def setUp(self):
        self.problem = Problem121()

    def test_sample(self):
        self.assertEqual(10, self.problem.max_prize_fund(4))

    def test_solution(self):
        self.assertEqual(2269, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
