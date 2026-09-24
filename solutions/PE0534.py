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
Solve time: ~75 seconds

---
MATHEMATICAL DERIVATION & ALGORITHMIC ARCHITECTURE:

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

3. Hybrid Dual Algorithmic Approach:
   As d varies from 0 to n - 1, the constraint structure shifts between two regimes:

   (A) Order-d Markov Transition Graph DP with Contiguous Prefix Slices (for d <= 8):
       - For smaller d, queens placed more than d rows apart exert no mutual constraints.
         The system behaves as an order-d Markov chain where the valid state at row r depends
         solely on the d-tuple of previous column placements (c_{r-d}, ..., c_{r-1}).
       - All valid d-tuples are generated in lexicographical order. Consequently, all states
         sharing the same (d-1)-prefix form a contiguous slice [start, end) in the state array.
       - The transition from state u = (c_0, tail) to state v = (tail, c_d) requires only
         checking that c_0 does not threaten c_d at distance d.
       - Each row transition from r to r+1 is a flat integer array addition:
             new_counts[v] += counts[u]
         which completely avoids Python dictionary/tuple overhead.

   (B) Fast Bitmask DFS with Branch-Free Sliding-Window Expirations (for d >= 9):
       - For large d, the search space is narrow. We use bitwise DFS tracking active bitmasks
         for columns (`cols`), left-diagonals (`d1`), and right-diagonals (`d2`).
       - When placing a queen at row r with bitmask `bit` (where bit = 1 << c), we record
         `bit_hist[r] = bit`.
       - When advancing from row r to r+1 with r >= d, the queen from row r - d expires.
         Its columns and diagonals are expired in O(1) branch-free bit operations:
             old_bit = bit_hist[r - d]
             nxt_cols = (cols | bit) ^ old_bit
             nxt_d1 = (((d1 | bit) << 1) & mask_all) ^ ((old_bit << (d + 1)) & mask_all)
             nxt_d2 = ((d2 | bit) >> 1) ^ (old_bit >> (d + 1))

4. Symmetry Reduction:
   Left-right reflection (c <-> n - 1 - c) is an automorphism of the board and attack relations.
   Fixing c_0 to {0, ..., floor(n/2) - 1} and multiplying by 2 (plus the center column if n is odd)
   cuts the state exploration in half for both DP and DFS.
"""

from typing import List, Tuple
import unittest
from util.utils import timeit


def solve_dp_graph(n: int, d: int) -> int:
    """Compute Q(n, w) where d = n - 1 - w using precomputed state graph DP with prefix slices."""
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

    states: List[Tuple[int, ...]] = []

    def build_states(cur: Tuple[int, ...]):
        if len(cur) == d:
            states.append(cur)
            return
        forb = 0
        for k, prev_c in enumerate(reversed(cur), 1):
            forb |= attack[k][prev_c]
        avail = mask_all & ~forb
        while avail:
            bit = avail & -avail
            avail &= avail - 1
            c = (bit - 1).bit_count()
            build_states(cur + (c,))

    build_states(())
    num_states = len(states)

    # Prefix slices: map each (d-1)-prefix to (start_idx, end_idx)
    # Since states are generated in lexicographical order, states with same prefix form a contiguous slice
    prefix_slices = {}
    curr_prefix = None
    start_idx = 0
    for idx, st in enumerate(states):
        pref = st[:-1]
        if pref != curr_prefix:
            if curr_prefix is not None:
                prefix_slices[curr_prefix] = (start_idx, idx)
            curr_prefix = pref
            start_idx = idx
    if curr_prefix is not None:
        prefix_slices[curr_prefix] = (start_idx, num_states)

    last_cols = [st[-1] for st in states]

    adj: List[List[int]] = [[] for _ in range(num_states)]
    for u, st in enumerate(states):
        c0 = st[0]
        tail = st[1:]
        forb_d = attack[d][c0]
        if tail in prefix_slices:
            s_idx, e_idx = prefix_slices[tail]
            for v in range(s_idx, e_idx):
                if not ((1 << last_cols[v]) & forb_d):
                    adj[u].append(v)

    counts = [0] * num_states
    half = n // 2
    for i, st in enumerate(states):
        if st[0] < half:
            counts[i] = 1

    for _ in range(d, n):
        new_counts = [0] * num_states
        for u in range(num_states):
            cnt = counts[u]
            if cnt:
                for v in adj[u]:
                    new_counts[v] += cnt
        counts = new_counts

    total = sum(counts) * 2

    if n % 2 == 1:
        counts = [0] * num_states
        mid = n // 2
        for i, st in enumerate(states):
            if st[0] == mid:
                counts[i] = 1
        for _ in range(d, n):
            new_counts = [0] * num_states
            for u in range(num_states):
                cnt = counts[u]
                if cnt:
                    for v in adj[u]:
                        new_counts[v] += cnt
            counts = new_counts
        total += sum(counts)

    return total


def compute_q_dfs_fast(n: int, d: int) -> int:
    """Compute Q(n, w) where d = n - 1 - w using fast bitmask DFS with sliding-window expirations."""
    mask_all = (1 << n) - 1
    shift = d + 1
    bit_hist = [0] * n
    count = 0

    if d >= n - 1:
        def dfs_full(r: int, cols: int, d1: int, d2: int):
            nonlocal count
            if r == n:
                count += 1
                return
            avail = mask_all & ~(cols | d1 | d2)
            while avail:
                bit = avail & -avail
                avail &= avail - 1
                dfs_full(r + 1, cols | bit, ((d1 | bit) << 1) & mask_all, (d2 | bit) >> 1)

        for c0 in range(n // 2):
            bit0 = 1 << c0
            dfs_full(1, bit0, (bit0 << 1) & mask_all, bit0 >> 1)
        total = count * 2
        if n % 2 == 1:
            bit0 = 1 << (n // 2)
            count = 0
            dfs_full(1, bit0, (bit0 << 1) & mask_all, bit0 >> 1)
            total += count
        return total

    def dfs(r: int, cols: int, d1: int, d2: int):
        nonlocal count
        if r == n:
            count += 1
            return

        avail = mask_all & ~(cols | d1 | d2)
        if r < d:
            while avail:
                bit = avail & -avail
                avail &= avail - 1
                bit_hist[r] = bit
                dfs(r + 1, cols | bit, ((d1 | bit) << 1) & mask_all, (d2 | bit) >> 1)
        else:
            while avail:
                bit = avail & -avail
                avail &= avail - 1
                bit_hist[r] = bit

                old_bit = bit_hist[r - d]
                nxt_cols = (cols | bit) ^ old_bit
                nxt_d1 = (((d1 | bit) << 1) & mask_all) ^ ((old_bit << shift) & mask_all)
                nxt_d2 = ((d2 | bit) >> 1) ^ (old_bit >> shift)

                dfs(r + 1, nxt_cols, nxt_d1, nxt_d2)

    for c0 in range(n // 2):
        bit0 = 1 << c0
        bit_hist[0] = bit0
        dfs(1, bit0, (bit0 << 1) & mask_all, bit0 >> 1)
    total = count * 2
    if n % 2 == 1:
        bit0 = 1 << (n // 2)
        bit_hist[0] = bit0
        count = 0
        dfs(1, bit0, (bit0 << 1) & mask_all, bit0 >> 1)
        total += count
    return total


class Problem534:
    def __init__(self):
        pass

    def q(self, n: int, w: int) -> int:
        """Calculate Q(n, w)."""
        d = n - 1 - w
        if d <= 9:
            return solve_dp_graph(n, d)
        return compute_q_dfs_fast(n, d)

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
