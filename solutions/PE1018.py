r"""
PROBLEM

Hex is a game for two players who take turns alternately placing stones on the empty hexagonal cells of a diamond shaped board like the one shown here:

[figure: 11x11 diamond hexagonal board]

The size of the board varies, but the $11 \times 11$ board seen in the figure is the most standard size.

The first player uses white stones, and the second player uses black stones. Once a stone is placed, it is never moved.

The first player wins the game by building a path of adjacent cells occupied by white stones that connects the two white sides of the board.
Similarly, the second player wins the game by building a path of adjacent cells occupied by black stones that connects the two black sides of the board.
The above figure shows a winning position of the second player. The stones forming the path are marked.

The game cannot end in a draw.

Let $H(N)$ be the number of different games that can be played on a $N \times N$ sized board. In other words, $H(N)$ is the number of possible sequences of moves until a player wins the game.

For example, $H(2)=24$, $H(3)=257760$, $H(4)=10663950528000$,
$H(5) = 5834112837767702970854400$,
$H(6) = 108665251059877521027015661242967432396800$.

Find $H(11)$ and give your answer modulo $1\,000\,000\,007$.

ANSWER: 838306569
Solve time: ~31.5 seconds

---
MATHEMATICAL DERIVATION:

1. Game Sequences and Terminal Board Positions:
   Let M = N^2 be the total number of cells on the N x N Hex board.
   A valid game is a sequence of moves (c_1, c_2, ..., c_k) such that:
   - White plays on odd turns 1, 3, 5, ... and Black plays on even turns 2, 4, 6, ...
   - The game terminates at turn k when the player who just moved forms a winning
     connection across their respective boundaries.
   - Neither player had formed a winning connection prior to turn k.

   Suppose White wins at turn k = 2w - 1. White has placed a set of w stones W,
   and Black has placed a set of b = w - 1 stones B, with W intersect B = empty.
   The final move was some stone x in W such that W is winning, but W \ {x}
   is not winning (i.e. x is an essential stone for W).

   By the fundamental Hex theorem (Jordan curve theorem on the planar hex lattice):
   For any subset S subseteq V, exactly one of S (for White) or V \ S (for Black)
   contains a winning connection.
   Because W contains a White winning path, the complement V \ W cannot contain
   a Black winning path. Since B subseteq V \ W, Black never has a winning connection
   for any subset B subseteq V \ W.
   Furthermore, by monotonicity of connectivity, since W \ {x} contains no White
   winning path, no subset of W \ {x} can contain a White winning path.
   Therefore, for any fixed pair (W, B) and essential move x in W, the preceding k - 1
   moves can be played in *any* of the (w - 1)! orderings for White and b! = (w - 1)!
   orderings for Black without either player winning early!

   The number of valid Black subsets of size b = w - 1 disjoint from W is C(M - w, w - 1).
   Hence, the number of games ending with terminal White configuration (W, x) is:
     (w - 1)! * (w - 1)! * C(M - w, w - 1) = (w - 1)! * (M - w)! / (M - 2w + 1)!
   An identical argument applies by symmetry for Black wins with |B| = b and |W| = b,
   yielding (b - 1)! * (M - b)! / (M - 2b)!.

2. Reduction from Essential Edge Counts E[s] to Spanning Subsets a_s:
   Let a_s be the number of subsets W subseteq V of size s that contain a White
   winning path connecting the top and bottom board boundaries.
   Let E[s] be the number of pairs (W, x) such that |W| = s, x in W, W is winning,
   and W \ {x} is not winning.
   In the Boolean hypercube {0, 1}^M, E[s] counts the boundary edges between level
   s - 1 and level s. Since every winning subset at level s - 1 has all M - (s - 1)
   supersets winning at level s, double-counting edges gives:
     E[s] = s * a_s - (M - s + 1) * a_{s-1}

   Substituting E[s] into the total game sum H(N) = sum_s E[s] * K[s] expresses H(N)
   as a direct linear combination of a_s:
     H(N) = sum_{s=N}^{floor((M+1)/2)} W[s] * a_s (mod 10^9 + 7)
   where the weights W[s] = s * K[s] - (M - s) * K[s + 1] vanish for all s > floor((M+1)/2).
   For N = 11, M = 121, so we only need a_s for s <= 61.

3. Frontier Transfer-Matrix Dynamic Programming:
   To count a_s, we sweep across the M = N^2 cells (r, c) in row-major order.
   At any point, the active boundary separating processed and unprocessed cells consists of
   exactly N cells. By planarity, the connected components along the frontier form
   non-crossing partitions, with at most one component connected to the top boundary (label 1).
   
   - If placing an empty cell leaves TOP disconnected with no remaining TOP cells on the frontier,
     the state is pruned (White can never connect top to bottom).
   - If placing a White stone in row N - 1 connects to TOP, the subset is winning: its
     polynomial contribution is accumulated directly into a_s convolved with (1 + z)^remaining,
     and the branch terminates early without needing further frontier tracking.
   - For N = 11, there are ~45,000 distinct frontier states. We precompute transition
     mappings into integer index arrays and vectorize state updates using NumPy `add.at`,
     computing H(11) (mod 10^9 + 7) in ~31 seconds in pure Python.
"""

import functools
import math
import unittest
import numpy as np
from util.utils import timeit


class Problem1018:
    def __init__(self, n: int = 11, mod: int = 1_000_000_007):
        self.n = n
        self.mod = mod

    @staticmethod
    @functools.lru_cache(maxsize=100_000)
    def _canonical_state(frontier: tuple[int, ...]) -> tuple[int, ...]:
        mapping = {0: 0, 1: 1}
        next_id = 2
        res = []
        for x in frontier:
            if x not in mapping:
                mapping[x] = next_id
                next_id += 1
            res.append(mapping[x])
        return tuple(res)

    def _get_transitions(self):
        n = self.n
        state_to_id = {tuple([0] * n): 0}
        id_to_state = [tuple([0] * n)]
        transitions = []
        current_layer = {0}

        for r in range(n):
            for c in range(n):
                t0: dict[int, int] = {}
                t1: dict[int, int] = {}
                next_layer = set()

                for sid in current_layer:
                    frontier = id_to_state[sid]
                    old_val = frontier[c]

                    # Option 0: cell (r, c) is empty (not in W)
                    new_f0 = list(frontier)
                    new_f0[c] = 0
                    if old_val != 1 or (1 in new_f0):
                        st0 = self._canonical_state(tuple(new_f0))
                        if st0 not in state_to_id:
                            state_to_id[st0] = len(id_to_state)
                            id_to_state.append(st0)
                        nid0 = state_to_id[st0]
                        t0[sid] = nid0
                        next_layer.add(nid0)
                    else:
                        t0[sid] = -1

                    # Option 1: cell (r, c) is White (in W)
                    nbr_labels = set()
                    if c > 0 and frontier[c - 1] != 0:
                        nbr_labels.add(frontier[c - 1])
                    if r > 0 and old_val != 0:
                        nbr_labels.add(old_val)
                    if r > 0 and c + 1 < n and frontier[c + 1] != 0:
                        nbr_labels.add(frontier[c + 1])
                    if r == 0:
                        nbr_labels.add(1)

                    new_f1 = list(frontier)
                    if not nbr_labels:
                        new_f1[c] = 999
                    elif 1 in nbr_labels:
                        new_f1[c] = 1
                        for i in range(n):
                            if i != c and new_f1[i] in nbr_labels:
                                new_f1[i] = 1
                    else:
                        min_l = min(nbr_labels)
                        new_f1[c] = min_l
                        for i in range(n):
                            if i != c and new_f1[i] in nbr_labels:
                                new_f1[i] = min_l

                    if r == n - 1 and new_f1[c] == 1:
                        t1[sid] = -2  # WIN
                    else:
                        st1 = self._canonical_state(tuple(new_f1))
                        if st1 not in state_to_id:
                            state_to_id[st1] = len(id_to_state)
                            id_to_state.append(st1)
                        nid1 = state_to_id[st1]
                        t1[sid] = nid1
                        next_layer.add(nid1)

                transitions.append((t0, t1))
                current_layer = next_layer

        return state_to_id, id_to_state, transitions

    @timeit
    def solve(self) -> int:
        n = self.n
        mod = self.mod
        m = n * n
        max_deg = (m + 1) // 2 + 1

        state_to_id, id_to_state, transitions = self._get_transitions()
        num_states = len(id_to_state)

        # Precompute binomial coefficients (1 + z)^rem mod MOD
        binom_poly = np.zeros((m + 1, max_deg), dtype=np.int64)
        for rem in range(m + 1):
            for k in range(min(rem + 1, max_deg)):
                binom_poly[rem, k] = math.comb(rem, k) % mod

        # Pre-extract transition arrays for vectorized NumPy DP
        step_data = []
        for cell_idx, (t0, t1) in enumerate(transitions):
            active = list(t0.keys())
            win_states = np.array([sid for sid in active if t1[sid] == -2], dtype=np.int32)
            v0 = np.array([sid for sid in active if t0[sid] >= 0], dtype=np.int32)
            tgt0 = np.array([t0[sid] for sid in v0], dtype=np.int32)
            v1 = np.array([sid for sid in active if t1[sid] >= 0], dtype=np.int32)
            tgt1 = np.array([t1[sid] for sid in v1], dtype=np.int32)
            step_data.append((win_states, v0, tgt0, v1, tgt1))

        dp = np.zeros((num_states, max_deg), dtype=np.int64)
        dp[0, 0] = 1
        a = np.zeros(max_deg, dtype=np.int64)

        cell_idx = 0
        for r in range(n):
            for c in range(n):
                rem_cells = m - 1 - cell_idx
                win_states, v0, tgt0, v1, tgt1 = step_data[cell_idx]
                cell_idx += 1

                if len(win_states) > 0:
                    win_sum = np.sum(dp[win_states], axis=0) % mod
                    shifted = np.zeros(max_deg, dtype=np.int64)
                    shifted[1:] = win_sum[:-1]
                    conv = np.convolve(shifted, binom_poly[rem_cells])[:max_deg] % mod
                    a = (a + conv) % mod

                next_dp = np.zeros((num_states, max_deg), dtype=np.int64)
                if len(v0) > 0:
                    np.add.at(next_dp, tgt0, dp[v0])
                if len(v1) > 0:
                    np.add.at(next_dp[:, 1:], tgt1, dp[v1, :-1])
                next_dp %= mod
                dp = next_dp

        # Factorials and inverse factorials for game weights
        fact = [1] * (m + 1)
        for i in range(1, m + 1):
            fact[i] = (fact[i - 1] * i) % mod

        inv_fact = [1] * (m + 1)
        inv_fact[m] = pow(fact[m], mod - 2, mod)
        for i in range(m - 1, -1, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % mod

        k_coef = [0] * (m + 2)
        for s in range(1, m + 1):
            cw = 0
            if 0 <= s - 1 <= m - s:
                cw = fact[s - 1] * fact[m - s] % mod * inv_fact[m - 2 * s + 1] % mod
            cb = 0
            if 0 <= s <= m - s:
                cb = fact[s - 1] * fact[m - s] % mod * inv_fact[m - 2 * s] % mod
            k_coef[s] = (cw + cb) % mod

        w_weights = [0] * (m + 1)
        for s in range(m + 1):
            w_weights[s] = (s * k_coef[s] - (m - s) * k_coef[s + 1]) % mod

        total_h = 0
        for s in range(len(a)):
            total_h = (total_h + a[s] * w_weights[s]) % mod

        return int(total_h)


class Solution1018(unittest.TestCase):
    def setUp(self):
        self.problem = Problem1018()

    def test_sample_2(self):
        self.assertEqual(24, Problem1018(n=2).solve())

    def test_sample_3(self):
        self.assertEqual(257760, Problem1018(n=3).solve())

    def test_sample_4(self):
        self.assertEqual(10663950528000 % 1_000_000_007, Problem1018(n=4).solve())

    def test_sample_5(self):
        self.assertEqual(5834112837767702970854400 % 1_000_000_007, Problem1018(n=5).solve())

    def test_sample_6(self):
        self.assertEqual(108665251059877521027015661242967432396800 % 1_000_000_007, Problem1018(n=6).solve())

    def test_solution(self):
        self.assertEqual(838306569, self.problem.solve())


if __name__ == "__main__":
    unittest.main()
