"""
PROBLEM

Barbara is a mathematician and a basketball player. She has found that the probability of scoring a
point when shooting from a distance x is exactly (1 - x / q), where q is a real constant greater than 50.

During each practice run, she takes 50 shots from distances x = 1, 2, ..., 50.
Write a program to determine the value of q (rounded to 10 decimal places) such that Barbara has an exact
2% chance of scoring exactly 20 points in 50 shots.

ANSWER: 52.6494571953
Solve time: ~0.003 seconds
"""

import unittest
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Problem Formulation:
#    Barbara takes n = 50 shots with distance x = 1, 2, ..., 50.
#    For each shot from distance x:
#      - Probability of scoring: p(x, q) = 1 - x / q
#      - Probability of missing: 1 - p(x, q) = x / q
#    The shots are independent Bernoulli trials with non-identical success probabilities p(x, q).
#    Let X be the total number of points scored: X = sum_{x=1}^{50} I_x.
#    We are given that P(X = 20) = 0.02, and q > 50.
#    We need to find q rounded to 10 decimal places.
#
# 2. Probability Generating Function & Dynamic Programming:
#    The probability generating function for shot x is:
#      G_x(t) = (x / q) + (1 - x / q) * t
#    The generating function for the total score X after n shots is:
#      G(t) = prod_{x=1}^{n} ((x / q) + (1 - x / q) * t)
#    The probability P(X = k) is the coefficient of t^k in G(t).
#
#    We can compute the distribution using Dynamic Programming:
#    Let dp[k] be the probability of scoring exactly k points after considering shots 1, ..., x:
#      dp_{x}[k] = dp_{x-1}[k] * (x / q) + dp_{x-1}[k-1] * (1 - x / q)
#    with base case:
#      dp_{0}[0] = 1,  dp_{0}[k] = 0 for k > 0.
#
#    Since we only need the probability for k up to 20 points, the DP state size at step x
#    is capped at min(x, 20) + 1. The total work to evaluate P(X = 20; q) is:
#      sum_{x=1}^{50} min(x, 20) = O(n * k) ~ 1000 operations per function evaluation.
#
# 3. Monotonicity & Root Finding:
#    As q increases (with q > 50):
#      - Each success probability p(x, q) = 1 - x / q increases strictly.
#      - The expected number of points E[X] = sum_{x=1}^{50} (1 - x / q) increases.
#      - For q close to 50 (e.g. q = 50.1), expected points is low and P(X = 20) > 0.04.
#      - As q -> inf, p(x, q) -> 1, so P(X = 20) -> 0.
#      - In the region q in [50, 60], P(X = 20; q) is strictly decreasing.
#
#    Therefore, the equation P(X = 20; q) = 0.02 has a unique root in (50, inf).
#    Using binary search (bisection) over [50 + eps, 100]:
#    Each bisection iteration halves the search interval.
#    After 80 iterations, the interval width is (50) / 2^80 ~ 4 * 10^-23, providing full
#    double-precision floating point accuracy well beyond the required 10 decimal places.


class Problem286:
    def __init__(self, shots: int = 50, target_points: int = 20, target_prob: float = 0.02, precision: int = 10):
        self.shots = shots
        self.target_points = target_points
        self.target_prob = target_prob
        self.precision = precision

    def compute_prob(self, q: float) -> float:
        """
        Computes P(X = target_points) for a given q using dynamic programming.
        """
        dp = [0.0] * (self.target_points + 1)
        dp[0] = 1.0

        for x in range(1, self.shots + 1):
            miss_prob = x / q
            score_prob = 1.0 - miss_prob

            # Update DP table in-place from right to left
            max_k = min(x, self.target_points)
            for k in range(max_k, 0, -1):
                dp[k] = dp[k] * miss_prob + dp[k - 1] * score_prob
            dp[0] = dp[0] * miss_prob

        return dp[self.target_points]

    @timeit
    def solve(self) -> float:
        low = float(self.shots) + 1e-9
        high = 100.0

        # Run bisection to converge to machine precision
        for _ in range(80):
            mid = (low + high) / 2.0
            p = self.compute_prob(mid)
            if p > self.target_prob:
                low = mid
            else:
                high = mid

        return round(mid, self.precision)


class Solution286(unittest.TestCase):
    def setUp(self):
        self.problem = Problem286()

    def test_solution(self):
        self.assertEqual(52.6494571953, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
