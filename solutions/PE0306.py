"""
PROBLEM

The following game is a classic example of Combinatorial Game Theory:

Two players start with a strip of $n$ white squares and they take alternate turns.

On each turn, a player picks two contiguous white squares and paints them black.

The first player who cannot make a move loses.

$n = 1$: No valid moves, so the first player loses automatically.
$n = 2$: Only one valid move, after which the second player loses.
$n = 3$: Two valid moves, but both leave a situation where the second player loses.
$n = 4$: Three valid moves for the first player, who is able to win the game by painting the two middle squares.
$n = 5$: Four valid moves for the first player (shown below in red), but no matter what the player does, the second player (blue) wins.

So, for $1 \\le n \\le 5$, there are 3 values of $n$ for which the first player can force a win.

Similarly, for $1 \\le n \\le 50$, there are 40 values of $n$ for which the first player can force a win.

For $1 \\le n \\le 1\\,000\\,000$, how many values of $n$ are there for which the first player can force a win?

ANSWER: 852938
Solve time: ~0.0002 seconds

---
MATHEMATICAL DERIVATION:

1. Game Reduction to Combinatorial Game Theory (Sprague-Grundy Theorem):
   This game is an impartial game played under normal play convention (last player to move wins).
   A game state consists of independent disjoint white strips of lengths $(s_1, s_2, \\dots, s_k)$.
   By the Sprague-Grundy theorem, each strip of length $n$ is equivalent to a Nim-pile of size $G(n)$,
   where $G(n)$ is the Grundy value (or nim-value) of a single strip of length $n$.

2. Sprague-Grundy Recurrence:
   - For $n = 0$ or $n = 1$, no valid moves are possible:
       $G(0) = 0, \\quad G(1) = 0$
   - For $n \\ge 2$, painting two adjacent squares at offset $i$ (where $0 \\le i \\le n - 2$) splits the
     strip into two independent sub-strips of lengths $i$ and $n - 2 - i$.
   - The nim-sum of the resulting position is $G(i) \\oplus G(n - 2 - i)$, where $\\oplus$ is bitwise XOR.
   - The Grundy value $G(n)$ is the minimum excluded non-negative integer (mex):
       $$G(n) = \\text{mex}\\{ G(i) \\oplus G(n - 2 - i) : 0 \\le i \\le \\lfloor (n - 2)/2 \\rfloor \\}$$

3. Relation to Dawson's Chess (Octal Game 0.07) & Ultimate Periodicity:
   In the classification of octal games by Guy and Smith (1956) and Conway (Winning Ways, Vol. 1),
   this game is mathematically isomorphic to Dawson's Chess (octal game .07, or Dawson's Bowling).
   The recurrence exhibits ultimate periodicity:
   - For all $n \\ge 87$, $G(n) = G(n - 34)$ with period $p = 34$.
   - The pre-period consists of values $n < 87$.
   - Because $87 + 2 \\times 34 + 2 \\ll 200$, the periodicity extends indefinitely to all $n \\to \\infty$
     by mathematical induction on the finite-memory nim-sum transition set.

4. Fast Counting of Winning Positions:
   A starting position $n$ is a first-player win (N-position) if and only if $G(n) > 0$.
   Conversely, the second player wins (P-position) if and only if $G(n) = 0$.
   - We compute the base Grundy values $G(n)$ for $n \\le 150$ via DP.
   - For any query $N$:
     - Count zeros in the pre-period $n \\in [1, \\min(N, 86)]$.
     - If $N \\ge 87$, count full periods $q = (N - 86) // 34$ and the remainder $r = (N - 86) \\% 34$.
     - Total zeros for $n \\ge 87$ is $q \\times (\\text{zeros in one period}) + (\\text{zeros in first } r \\text{ elements of period})$.
     - The number of winning $n$ is simply $N - (\\text{total zeros})$.

5. Complexity Analysis:
   - Base DP computation: $O(K^2)$ where $K = 150$, taking $< 0.1$ ms.
   - Evaluation for $N = 10^6$: $O(1)$ arithmetic operations.
   - Space Complexity: $O(1)$ auxiliary storage for the first 150 Grundy values.
"""

import unittest
from util.utils import timeit


class Problem306:
    def __init__(self):
        # Compute base Grundy values up to index 150
        # Period p = 34 starts strictly at n = 87
        limit = 150
        self.g = [0] * (limit + 1)
        for n in range(2, limit + 1):
            seen = [False] * 64
            for i in range((n - 1) // 2 + 1):
                val = self.g[i] ^ self.g[n - 2 - i]
                if val < 64:
                    seen[val] = True
            mex = 0
            while seen[mex]:
                mex += 1
            self.g[n] = mex

        self.pre_period_end = 86
        self.period = 34

        # Precompute zeros in the pre-period and in one period [87, 120]
        self.pre_zeros = sum(1 for n in range(1, self.pre_period_end + 1) if self.g[n] == 0)
        self.period_zeros = [
            1 if self.g[self.pre_period_end + 1 + i] == 0 else 0
            for i in range(self.period)
        ]
        self.period_zeros_sum = sum(self.period_zeros)

    def count_zeros(self, n: int) -> int:
        """Count the number of 1 <= k <= n with G(k) == 0."""
        if n <= self.pre_period_end:
            return sum(1 for k in range(1, n + 1) if self.g[k] == 0)

        total_zeros = self.pre_zeros
        remaining = n - self.pre_period_end
        q, r = divmod(remaining, self.period)
        total_zeros += q * self.period_zeros_sum
        total_zeros += sum(self.period_zeros[:r])
        return total_zeros

    @timeit
    def solve(self, n: int = 1_000_000) -> int:
        zeros = self.count_zeros(n)
        return n - zeros


class Solution306(unittest.TestCase):
    def setUp(self):
        self.problem = Problem306()

    def test_sample_5(self):
        self.assertEqual(3, self.problem.solve(5))

    def test_sample_50(self):
        self.assertEqual(40, self.problem.solve(50))

    def test_solution(self):
        self.assertEqual(852938, self.problem.solve(1_000_000))


if __name__ == "__main__":
    unittest.main()
