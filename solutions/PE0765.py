"""
PROBLEM

Starting with 1 gram of gold you play a game. Each round you bet a certain amount of your gold:
if you have x grams you can bet b grams for any 0 <= b <= x. You then toss an unfair coin:
with a probability of 0.6 you double your bet (so you now have x + b), otherwise you lose
your bet (so you now have x - b).

Choosing your bets to maximize your probability of having at least a trillion (10^12) grams of
gold after 1000 rounds, what is the probability that you become a trillionaire?

All computations are assumed to be exact (no rounding), but give your answer rounded to 10 digits
behind the decimal point.

ANSWER: 0.2429251641
Solve time: ~0.03 seconds

---
MATHEMATICAL DERIVATION:

1. Change of Measure (Risk-Neutral / Fair-Coin Measure):
   Consider the game under an artificial "fair-coin" probability measure Q where the coin lands
   heads or tails with equal probability 1/2.
   Under Q, the wealth process X_k is a martingale regardless of the betting strategy:
     E_Q[X_{k+1} | X_k] = 1/2 (X_k + b) + 1/2 (X_k - b) = X_k.
   Therefore, the expected terminal wealth under Q is fixed at the initial wealth:
     E_Q[X_N] = X_0 = 1.

2. Budget Constraint on Success Paths:
   Each of the 2^N outcome paths omega in {H, T}^N has probability Q(omega) = 1 / 2^N under Q.
   Reaching at least M = 10^12 grams at round N requires X_N(omega) >= M on any successful path omega.
   Let S be the set of successful paths on which X_N >= M.
   Since X_N >= 0 everywhere:
     1 = E_Q[X_N] >= sum_{omega in S} X_N(omega) Q(omega) >= M * |S| / 2^N.
   Therefore, with initial wealth 1, the total number of paths on which we can guarantee success is at most:
     |S| <= floor(2^N / M).
   Conversely, in a complete binary market (the binomial asset pricing model), any payoff vector X_N >= 0
   satisfying E_Q[X_N] <= 1 can be exactly replicated by dynamic backward induction betting.

3. Neyman-Pearson / Likelihood Ratio Optimization:
   Under the real probability measure P, heads has probability p = 3/5 and tails has probability q = 2/5.
   For a path omega with k heads (wins) and N - k tails (losses), its true probability is:
     P(omega) = (3/5)^k * (2/5)^{N - k} = 3^k * 2^{N - k} / 5^N.
   The likelihood ratio (Radon-Nikodym derivative dP/dQ):
     (dP/dQ)(omega) = 2^N * 3^k * 2^{N - k} / 5^N = (6/5)^k * (4/5)^{N - k}
   is strictly increasing in k (since 6/5 > 4/5).
   By the Neyman-Pearson Lemma, to maximize the total probability P(S) subject to the budget constraint
   |S| <= floor(2^N / M), the optimal set S must greedily select paths with the highest number of wins k!

4. Exact Computation:
   For N = 1000 and M = 10^12:
   - Total budget: B = floor(2^1000 / 10^12).
   - Find the threshold k_0 such that:
       sum_{k = k_0 + 1}^N comb(N, k) <= B < sum_{k = k_0}^N comb(N, k).
   - We take all paths with k >= k_0 + 1 wins, and rem = B - sum_{k = k_0 + 1}^N comb(N, k) paths
     with exactly k_0 wins.
   - The exact probability is computed using arbitrary-precision integer arithmetic over denominator 5^N:
       P(S) = [ sum_{k = k_0 + 1}^N comb(N, k) * 3^k * 2^{N - k} + rem * 3^{k_0} * 2^{N - k_0} ] / 5^N.
   - Round to 10 decimal digits: 0.2429251641.
"""

from math import comb
import unittest
from util.utils import timeit


class Problem765:
    def __init__(self, rounds: int = 1000, target: int = 10**12, p_num: int = 3, p_den: int = 5):
        self.rounds = rounds
        self.target = target
        self.p_num = p_num
        self.p_den = p_den
        self.q_num = p_den - p_num

    def compute_max_prob(self, digits: int = 10) -> str:
        n = self.rounds
        m = self.target

        total_paths = 1 << n
        budget = total_paths // m

        comb_n = [comb(n, k) for k in range(n + 1)]

        suffix = [0] * (n + 2)
        for k in range(n, -1, -1):
            suffix[k] = suffix[k + 1] + comb_n[k]

        k0 = 0
        for k in range(n, -1, -1):
            if suffix[k] > budget >= suffix[k + 1]:
                k0 = k
                break

        rem = budget - suffix[k0 + 1]

        pow_q = [1] * (n + 1)
        pow_p = [1] * (n + 1)
        for i in range(1, n + 1):
            pow_q[i] = pow_q[i - 1] * self.q_num
            pow_p[i] = pow_p[i - 1] * self.p_num

        num = 0
        for k in range(k0 + 1, n + 1):
            num += comb_n[k] * pow_p[k] * pow_q[n - k]
        if rem:
            num += rem * pow_p[k0] * pow_q[n - k0]

        den = self.p_den**n

        scale = 10**digits
        q_val, r_val = divmod(num * scale, den)
        if r_val * 2 >= den:
            q_val += 1

        int_part, frac_part = divmod(q_val, scale)
        return f"{int_part}.{str(frac_part).zfill(digits)}"

    @timeit
    def solve(self) -> str:
        return self.compute_max_prob(10)


class Solution765(unittest.TestCase):
    def setUp(self):
        self.problem = Problem765()

    def test_solution(self):
        self.assertEqual("0.2429251641", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
