"""
PROBLEM

Peter has nine four-sided (pyramidal) dice, each with faces numbered 1, 2, 3, 4.
Colin has six six-sided (cubic) dice, each with faces numbered 1, 2, 3, 4, 5, 6.

Peter and Colin roll their dice and compare totals: the highest total wins. The result is a draw if the totals are equal.

What is the probability that Pyramidal Peter beats Cubic Colin? Give your answer rounded to seven decimal places in the form 0.abcdefg.

ANSWER: 0.5731441
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Probability Generating Functions for Dice Sums:
   When rolling n independent fair s-sided dice (faces 1, ..., s), the generating function for the sum S is:
   G_{n, s}(x) = (x + x^2 + ... + x^s)^n = x^n * ((1 - x^s) / (1 - x))^n.

2. Closed-Form Inclusion-Exclusion for Sum Frequencies:
   Expanding (1 - x^s)^n via the binomial theorem and (1 - x)^{-n} via the negative binomial series:
   [x^k] G_{n, s}(x) = sum_{j=0}^{floor((k - n) / s)} (-1)^j * comb(n, j) * comb(k - j*s - 1, n - 1).
   This gives the exact number of outcomes c(n, s, k) out of s^n total rolls that sum to k.

3. Winning Probability Calculation:
   Let P_k = c(9, 4, k) for 9 <= k <= 36 (out of 4^9 = 262,144 total outcomes),
   and C_k = c(6, 6, k) for 6 <= k <= 36 (out of 6^6 = 46,656 total outcomes).
   Since Peter and Colin roll independently, the probability that Peter's total strictly exceeds Colin's total is:
   P(S_Peter > S_Colin) = (1 / (4^9 * 6^6)) * sum_{k=9}^{36} P_k * (sum_{m=6}^{k-1} C_m).
"""

import math
import unittest
from util.utils import timeit


class Problem205:
    def __init__(self):
        pass

    @staticmethod
    def sum_frequencies(num_dice: int, num_sides: int) -> list[int]:
        max_sum = num_dice * num_sides
        counts = [0] * (max_sum + 1)
        for k in range(num_dice, max_sum + 1):
            total = 0
            for j in range((k - num_dice) // num_sides + 1):
                term = math.comb(num_dice, j) * math.comb(k - j * num_sides - 1, num_dice - 1)
                if j & 1:
                    total -= term
                else:
                    total += term
            counts[k] = total
        return counts

    def win_probability(self, p_dice: int, p_sides: int, c_dice: int, c_sides: int) -> float:
        p_counts = self.sum_frequencies(p_dice, p_sides)
        c_counts = self.sum_frequencies(c_dice, c_sides)

        max_sum = max(len(p_counts), len(c_counts)) - 1
        win_ways = 0
        c_prefix_sum = 0

        for s in range(1, max_sum + 1):
            if s < len(p_counts):
                win_ways += p_counts[s] * c_prefix_sum
            if s < len(c_counts):
                c_prefix_sum += c_counts[s]

        total_ways = (p_sides ** p_dice) * (c_sides ** c_dice)
        return win_ways / total_ways

    @timeit
    def solve(self) -> str:
        prob = self.win_probability(p_dice=9, p_sides=4, c_dice=6, c_sides=6)
        return f"{prob:.7f}"


class Solution205(unittest.TestCase):
    def setUp(self):
        self.problem = Problem205()

    def test_sample(self):
        # 1 fair 4-sided die vs 1 fair 4-sided die: 6 winning pairs out of 16 -> 0.375
        self.assertAlmostEqual(6 / 16, self.problem.win_probability(1, 4, 1, 4), places=10)
        # 1 fair 6-sided die vs 1 fair 6-sided die: 15 winning pairs out of 36 -> 5/12
        self.assertAlmostEqual(15 / 36, self.problem.win_probability(1, 6, 1, 6), places=10)

    def test_solution(self):
        self.assertEqual("0.5731441", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
