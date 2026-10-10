"""
PROBLEM

A Fibonacci tree is a binary tree recursively defined as:
- T(0) is the empty tree.
- T(1) is the binary tree with only one node.
- T(k) consists of a root node that has T(k-1) and T(k-2) as children.

On such a tree two players play a take-away game. On each turn a player selects a node and removes that node along with
the subtree rooted at that node.
The player who is forced to take the root node of the entire tree loses.

Here are the winning moves of the first player on the first turn for T(k) from k=1 to k=6.
Let f(k) be the number of winning moves of the first player (i.e. the moves for which the second player has no winning
strategy) on the first turn of the game when this game is played on T(k).

For example, f(5) = 1 and f(10) = 17.

Find f(10000). Give the last 18 digits of your answer.

ANSWER: 438505383468410633
Solve time: ~7.2 seconds

---
MATHEMATICAL DERIVATION:

1. Equivalence to Green Hackenbush on Trees:
   The game is played on the nodes of T(k), excluding the root (since taking the root loses immediately).
   Selecting a node v != root and removing its subtree is isomorphic to cutting the edge between v and its parent.
   Any node whose path to the root passed through v is disconnected and removed.
   Thus, the game is identical to Green Hackenbush on trees with the root at ground level, played under normal play convention.

2. The Colon Principle and Grundy Values:
   By the Colon Principle for impartial games on trees:
   - An edge connected to a subtree of Grundy value g behaves as a nim-heap of size g + 1.
   - Subtrees branching from the root combine via the XOR sum of their nim-values.
   Thus, the Grundy values G(k) of the full trees T(k) satisfy:
   G(0) = 0, G(1) = 0, G(2) = 1,
   G(k) = (G(k-1) + 1) ^ (G(k-2) + 1) for k >= 3.

3. Vectorized Dynamic Programming via Injective Nim-Value Mappings:
   A move is winning if and only if the resulting game state has Grundy value 0.
   Let W(k, g) denote the number of non-root nodes in T(k) whose removal yields a remaining state with Grundy value g.
   The moves available in T(k) decompose into:
   - Removing the left child: yields Grundy value r_val = (G(k-2) + 1 if k-2 >= 1 else 0).
   - Removing a node inside the left child: if the left child changes to value g_L, the whole tree becomes
     whole_g = (g_L + 1) ^ r_val. Because g_L -> (g_L + 1) ^ r_val is a bijection, each distinct state in W(k-1)
     maps injectively to a unique value.
   - Removing the right child (k >= 3): yields Grundy value l_val = G(k-1) + 1.
   - Removing a node inside the right child: if the right child changes to value g_R, the whole tree becomes
     whole_g = (g_R + 1) ^ l_val, which is also an injective mapping.

   Instead of hash map overhead, we vectorize the state updates across a contiguous flat array using NumPy fancy
   indexing and non-zero tracking. This achieves an order-of-magnitude speedup (~7.2 seconds for k = 10000).
"""

import unittest
import numpy as np
from util.utils import timeit


class Problem400:
    def __init__(self):
        pass

    def compute_f(self, target_k: int) -> int:
        mod = 10 ** 18
        max_g = 160000

        g_vals = [0] * (target_k + 1)
        g_vals[1] = 0
        if target_k >= 2:
            g_vals[2] = 1
        for k in range(3, target_k + 1):
            g_vals[k] = (g_vals[k - 1] + 1) ^ (g_vals[k - 2] + 1)

        keys_prev2 = np.empty(0, dtype=np.int64)
        vals_prev2 = np.empty(0, dtype=np.int64)

        keys_prev1 = np.array([0], dtype=np.int64)
        vals_prev1 = np.array([1], dtype=np.int64)

        buf = np.zeros(max_g, dtype=np.int64)
        max_seen = 0

        for k in range(3, target_k + 1):
            r_val = g_vals[k - 2] + 1 if k - 2 >= 1 else 0
            l_val = g_vals[k - 1] + 1

            idx_l = (keys_prev1 + 1) ^ r_val
            buf[idx_l] = vals_prev1
            buf[r_val] += 1

            cur_max = r_val
            if idx_l.size > 0:
                m = int(np.max(idx_l))
                if m > cur_max:
                    cur_max = m

            if k - 2 >= 1:
                buf[l_val] += 1
                if keys_prev2.size > 0:
                    idx_r = (keys_prev2 + 1) ^ l_val
                    buf[idx_r] += vals_prev2
                    m = int(np.max(idx_r))
                    if m > cur_max:
                        cur_max = m
                if l_val > cur_max:
                    cur_max = l_val

            if cur_max > max_seen:
                max_seen = cur_max

            active_keys = np.flatnonzero(buf[:max_seen + 1])
            active_vals = buf[active_keys] % mod

            buf[active_keys] = 0

            keys_prev2 = keys_prev1
            vals_prev2 = vals_prev1

            keys_prev1 = active_keys
            vals_prev1 = active_vals

        if keys_prev1.size > 0 and keys_prev1[0] == 0:
            return int(vals_prev1[0])
        return 0

    @timeit
    def solve(self) -> int:
        return self.compute_f(10000)


class Solution400(unittest.TestCase):
    def setUp(self):
        self.problem = Problem400()

    def test_sample(self):
        self.assertEqual(1, self.problem.compute_f(5))
        self.assertEqual(17, self.problem.compute_f(10))

    def test_solution(self):
        self.assertEqual(438505383468410633, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
