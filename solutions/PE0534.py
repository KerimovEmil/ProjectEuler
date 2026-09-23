"""
PROBLEM

The problem of placing n queens on an n×n chessboard such that no two queens threaten each
other is known as the n-queens puzzle. For n = 8, there are 92 distinct solutions.

A weak queen can move any number of squares horizontally, but can move a maximum of
(n - 1 - w) squares vertically or diagonally, where w is the "weakness" parameter (0 ≤ w < n).
When w = 0, a weak queen is a normal queen. When w = n - 1, it cannot threaten any squares
vertically or diagonally.

Let Q(n, w) be the number of ways to place n weak queens with weakness w on an n×n chessboard
such that no two queens threaten each other.

For example, Q(4, 0) = 2, Q(4, 2) = 16, and Q(4, 3) = 256.
Also define S(n) = sum_{w=0}^{n-1} Q(n, w).
You are given S(4) = 276 and S(5) = 3347.

Find S(14).

ANSWER: 11726115562784664
Solve time: ~180 seconds

---
MATHEMATICAL DERIVATION:

1. Threat Condition & Distance Parameter d:
   Horizontal movement is unrestricted, so exactly one queen must occupy each of the n rows.
   Let the queen on row r be placed at column c_r in {0, 1, ..., n-1}.
   Let d = n - 1 - w denote the maximum vertical/diagonal attack distance.
   Two queens at rows r_1 and r_2 (with 1 <= |r_1 - r_2| <= d) threaten each other iff:
       c_{r_1} == c_{r_2}  (same column)
       OR |c_{r_1} - c_{r_2}| == |r_1 - r_2|  (same diagonal).
   If |r_1 - r_2| > d, they do not threaten each other even if sharing a column or diagonal.

2. Boundary Cases:
   - When d = 0 (w = n - 1): queens only threaten along the horizontal row. Since each row
     has one queen, each row chooses any column independently: Q(n, n - 1) = n^n.
   - When d = n - 1 (w = 0): this is the standard N-Queens problem.

3. Hybrid Algorithmic Architecture:
   As d varies from 0 to n - 1, the nature of the constraints shifts drastically:
   - For small d (large w, wide search tree):
     Constraints only extend back d rows. The system behaves as an order-d Markov process.
     We use Dynamic Programming with state (c_{r-d}, ..., c_{r-1}) remembering only the last
     d queen placements. State space is small and transitions take O(1) bitwise operations.
   - For large d (small w, tight search tree):
     The search tree is very narrow. We use Depth-First Search with O(1) Bitwise Expirations:
     Maintain active bitmasks for columns (`cols`), main diagonals (`d1`), and anti-diagonals (`d2`).
     Within any sliding window of length d, all active queens occupy pairwise distinct columns and
     diagonals. When stepping from row r to r+1, the queen placed at row r - d expires, allowing
     its column, d1, and d2 bits to be removed via XOR (`^=`) in O(1) time.

4. Symmetry Reduction:
   Left-right reflection (c <-> n - 1 - c) is an automorphism of the board and attack relations.
   For row 0, restricting c_0 to {0, ..., floor(n/2) - 1} and multiplying by 2 (plus the center
   column if n is odd) halves the required computation.
"""

from typing import Dict, List, Tuple
import unittest
from util.utils import timeit


def compute_q_dp(n: int, d: int) -> int:
    """Compute Q(n, w) where d = n - 1 - w using dynamic programming over the last d rows."""
    if d == 0:
        return n**n
    if d == 1:
        dp = [1] * n
        for _ in range(n - 1):
            new_dp = [0] * n
            for c_prev in range(n):
                val = dp[c_prev]
                if not val:
                    continue
                for c in range(n):
                    if c != c_prev and abs(c - c_prev) != 1:
                        new_dp[c] += val
            dp = new_dp
        return sum(dp)

    # Precompute attack bitmasks
    attack = [[0] * n for _ in range(d + 1)]
    for k in range(1, d + 1):
        for c in range(n):
            mask = (1 << c)
            if c + k < n:
                mask |= (1 << (c + k))
            if c - k >= 0:
                mask |= (1 << (c - k))
            attack[k][c] = mask

    mask_all = (1 << n) - 1

    # Symmetry on row 0
    dp: Dict[Tuple[int, ...], int] = {(c,): 1 for c in range(n // 2)}
    for r in range(1, n):
        new_dp: Dict[Tuple[int, ...], int] = {}
        for state, count in dp.items():
            forb = 0
            for k, prev_c in enumerate(reversed(state), 1):
                forb |= attack[k][prev_c]
            avail = mask_all & ~forb
            while avail:
                bit = avail & -avail
                avail &= avail - 1
                c = (bit - 1).bit_count()
                nxt = (state + (c,)) if len(state) < d else (state[1:] + (c,))
                new_dp[nxt] = new_dp.get(nxt, 0) + count
        dp = new_dp

    total = sum(dp.values()) * 2

    if n % 2 == 1:
        c0 = n // 2
        dp_mid: Dict[Tuple[int, ...], int] = {(c0,): 1}
        for r in range(1, n):
            new_dp = {}
            for state, count in dp_mid.items():
                forb = 0
                for k, prev_c in enumerate(reversed(state), 1):
                    forb |= attack[k][prev_c]
                avail = mask_all & ~forb
                while avail:
                    bit = avail & -avail
                    avail &= avail - 1
                    c = (bit - 1).bit_count()
                    nxt = (state + (c,)) if len(state) < d else (state[1:] + (c,))
                    new_dp[nxt] = new_dp.get(nxt, 0) + count
            dp_mid = new_dp
        total += sum(dp_mid.values())

    return total


def compute_q_dfs(n: int, d: int) -> int:
    """Compute Q(n, w) where d = n - 1 - w using bitmask DFS with O(1) sliding window expirations."""
    if d == 0:
        return n**n

    mask_all = (1 << n) - 1
    history = [0] * n
    count = 0

    for c0 in range(n // 2):
        history[0] = c0
        bit0 = 1 << c0

        def dfs(r: int, cols: int, d1: int, d2: int):
            nonlocal count
            if r == n:
                count += 1
                return

            avail = mask_all & ~(cols | d1 | d2)
            while avail:
                bit = avail & -avail
                avail &= avail - 1
                c = (bit - 1).bit_count()
                history[r] = c

                nxt_cols = cols | bit
                nxt_d1 = ((d1 | bit) << 1) & mask_all
                nxt_d2 = (d2 | bit) >> 1

                # Expire queen from row r - d
                if r >= d:
                    old_c = history[r - d]
                    nxt_cols ^= (1 << old_c)
                    shift1 = old_c + d + 1
                    if shift1 < n:
                        nxt_d1 ^= (1 << shift1)
                    shift2 = old_c - (d + 1)
                    if shift2 >= 0:
                        nxt_d2 ^= (1 << shift2)

                dfs(r + 1, nxt_cols, nxt_d1, nxt_d2)

        init_cols = bit0
        init_d1 = (bit0 << 1) & mask_all
        init_d2 = bit0 >> 1
        dfs(1, init_cols, init_d1, init_d2)

    total = count * 2

    if n % 2 == 1:
        c0 = n // 2
        history[0] = c0
        bit0 = 1 << c0
        count_mid = 0

        def dfs_mid(r: int, cols: int, d1: int, d2: int):
            nonlocal count_mid
            if r == n:
                count_mid += 1
                return

            avail = mask_all & ~(cols | d1 | d2)
            while avail:
                bit = avail & -avail
                avail &= avail - 1
                c = (bit - 1).bit_count()
                history[r] = c

                nxt_cols = cols | bit
                nxt_d1 = ((d1 | bit) << 1) & mask_all
                nxt_d2 = (d2 | bit) >> 1

                if r >= d:
                    old_c = history[r - d]
                    nxt_cols ^= (1 << old_c)
                    shift1 = old_c + d + 1
                    if shift1 < n:
                        nxt_d1 ^= (1 << shift1)
                    shift2 = old_c - (d + 1)
                    if shift2 >= 0:
                        nxt_d2 ^= (1 << shift2)

                dfs_mid(r + 1, nxt_cols, nxt_d1, nxt_d2)

        init_cols = bit0
        init_d1 = (bit0 << 1) & mask_all
        init_d2 = bit0 >> 1
        dfs_mid(1, init_cols, init_d1, init_d2)
        total += count_mid

    return total


class Problem534:
    def __init__(self):
        pass

    def q(self, n: int, w: int) -> int:
        """Calculate Q(n, w)."""
        d = n - 1 - w
        if d <= 7:
            return compute_q_dp(n, d)
        return compute_q_dfs(n, d)

    @timeit
    def solve(self, n: int = 14) -> int:
        """Calculate S(n) = sum_{w=0}^{n-1} Q(n, w)."""
        return sum(self.q(n, w) for w in range(n))


class Solution534(unittest.TestCase):
    def setUp(self):
        self.problem = Problem534()

    def test_sample_q(self):
        self.assertEqual(2, self.problem.q(4, 0))
        self.assertEqual(16, self.problem.q(4, 2))
        self.assertEqual(256, self.problem.q(4, 3))

    def test_sample_s(self):
        self.assertEqual(276, self.problem.solve(4))
        self.assertEqual(3347, self.problem.solve(5))

    def test_solution_final(self):
        self.assertEqual(11726115562784664, self.problem.solve(14))


if __name__ == '__main__':
    unittest.main()
