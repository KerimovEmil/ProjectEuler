"""
PROBLEM

In the game of darts a player throws three darts at a target board which is split into twenty equal sized sections
numbered one to twenty.

The score of a dart is determined by the number of the region that the dart lands in. A dart landing outside the
red/green outer ring scores zero. The black and cream regions inside this ring represent single scores. However,
the red/green outer ring and middle ring score double and treble scores respectively.

At the centre of the board are two concentric circles called the bull region, or bulls-eye. The outer bull is worth
25 points and the inner bull is a double, worth 50 points.

There are many variations of rules but in the most popular game the players will begin with a score 301 or 501 and
the first player to reduce their running total to zero is a winner. However, it is normal to play a "doubles out"
system, which means that the player must land a double (including the double bulls-eye at the centre of the board)
on their final dart to win; any other dart that would reduce their running total to one or lower means the score
for that set of three darts is "bust".

When a player is able to finish on their current score it is called a "checkout" and the highest checkout is 170:
T20 T20 D25 (two treble 20s and double bull).

There are exactly eleven distinct ways to checkout on a score of 6:
  D3, D1 D2, S2 D2, D2 D1, S4 D1, S1 S1 D2, S1 T1 D1, S1 S3 D1, D1 D1 D1, D1 S2 D1, S2 S2 D1

Note that D1 D2 is considered different to D2 D1 as they finish on different doubles. However, the combination
S1 T1 D1 is considered the same as T1 S1 D1.
In addition we shall not include misses in considering combinations; for example, D3 is the same as 0 D3 and 0 0 D3.

Incredibly there are 42336 distinct ways of checking out in total.
How many distinct ways can a player checkout with a score less than 100?

ANSWER: 38182
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Structure of a Valid Checkout:
   Every checkout consists of:
   - An unordered pair of preliminary darts {d_1, d_2}, where each dart is chosen from the 63 possible outcomes:
     * Miss (0): 1 outcome
     * Singles (S1..S20, S25): 21 outcomes
     * Doubles (D1..D20, D25): 21 outcomes
     * Trebles (T1..T20): 20 outcomes
     (Choosing 0 for both d_1 and d_2 represents a 1-dart checkout; choosing 0 for exactly one represents a 2-dart
     checkout; choosing non-zero for both represents a 3-dart checkout.)
   - A final ordered dart d_3 chosen from the 21 Doubles (D1..D20, D25).

2. Total Checkout Count Verification:
   There are comb(63 + 2 - 1, 2) = 63 * 64 / 2 = 2016 unordered pairs {d_1, d_2} and 21 choices for d_3, giving
   2016 * 21 = 42,336 total distinct checkouts across all scores.

3. Counting Checkouts Below 100:
   Enumerating all 2016 unordered pairs {d_1, d_2} with indices 0 <= i <= j < 63 and all 21 doubles d_3, we count
   those satisfying score(d_i) + score(d_j) + score(d_3) < 100.
"""

import unittest
from util.utils import timeit


class Problem109:
    def __init__(self):
        singles = list(range(1, 21)) + [25]
        self.doubles = [2 * x for x in range(1, 21)] + [50]
        trebles = [3 * x for x in range(1, 21)]
        self.all_darts = [0] + singles + self.doubles + trebles

    def count_checkouts(self, max_score_exclusive: int | None = None, exact_score: int | None = None) -> int:
        n = len(self.all_darts)
        count = 0
        for i in range(n):
            s1 = self.all_darts[i]
            for j in range(i, n):
                s12 = s1 + self.all_darts[j]
                for d in self.doubles:
                    total = s12 + d
                    if exact_score is not None:
                        if total == exact_score:
                            count += 1
                    elif max_score_exclusive is not None:
                        if total < max_score_exclusive:
                            count += 1
                    else:
                        count += 1
        return count

    @timeit
    def solve(self) -> int:
        return self.count_checkouts(max_score_exclusive=100)


class Solution109(unittest.TestCase):
    def setUp(self):
        self.problem = Problem109()

    def test_sample(self):
        self.assertEqual(11, self.problem.count_checkouts(exact_score=6))
        self.assertEqual(42336, self.problem.count_checkouts())

    def test_solution(self):
        self.assertEqual(38182, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
