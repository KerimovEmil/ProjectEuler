r"""
PROBLEM

Consider the following configuration of $64$ triangles:

We wish to colour the interior of each triangle with one of three colours: red, green or blue, so that no two neighbouring triangles have the same colour. Such a colouring shall be called valid. Here, two triangles are said to be neighbouring if they share an edge.

Note: if they only share a vertex, then they are not neighbours.

For example, here is a valid colouring of the above grid:

A colouring $C^\prime$ which is obtained from a colouring $C$ by rotation or reflection is considered distinct from $C$ unless the two are identical.

How many distinct valid colourings are there for the above configuration?

ANSWER: 10834893628237824
Solve time: ~0.05 seconds

---
MATHEMATICAL DERIVATION:

1. Geometric Graph Decomposition & Bipartiteness:
   - A grid of side length $N$ contains $N^2$ unit equilateral triangles arranged into $N$ horizontal rows.
   - Row $r$ ($1 \le r \le N$) contains $2r - 1$ triangles:
     - $r$ upward-pointing triangles $U_{r, 0}, U_{r, 1}, \dots, U_{r, r-1}$.
     - $r-1$ downward-pointing triangles $D_{r, 0}, D_{r, 1}, \dots, D_{r, r-2}$.
   - Up-triangles only share edges with down-triangles, and down-triangles only share edges with up-triangles.
     Thus, the dual adjacency graph is bipartite.
   - Each down-triangle $D_{r, j}$ is adjacent to exactly three up-triangles:
     $U_{r-1, j}$ (above), $U_{r, j}$ (bottom-left), and $U_{r, j+1}$ (bottom-right).
   - Crucially, no two down-triangles share an edge.

2. Dynamic Programming with Broken Profile / Frontier:
   - Given an assignment of colours to the up-triangles of row $r-1$, $u \in \{0, 1, 2\}^{r-1}$, and row $r$,
     $v \in \{0, 1, 2\}^r$, each down-triangle $D_{r, j}$ ($0 \le j \le r-2$) can be coloured independently:
     $$w(u_j, v_j, v_{j+1}) = 3 - |\{u_j, v_j, v_{j+1}\}|$$
     where $w \in \{0, 1, 2\}$ is the number of valid colour choices.
   - The total number of ways to colour row $r$ given row $r-1$ factorizes as:
     $$W(u, v) = \prod_{j=0}^{r-2} w(u_j, v_j, v_{j+1})$$
   - To transition from row $r-1$ to row $r$ efficiently, we advance element-by-element along a sliding frontier:
     - Step 0: Choose $v_0 \in \{0, 1, 2\}$.
     - Step $j$ ($1 \le j \le r-1$): Choose $v_j \in \{0, 1, 2\}$, multiply by $w(u_{j-1}, v_{j-1}, v_j)$, and slide the frontier.
   - Color Symmetry: We fix the top triangle $U_{1, 0} = 0$ and multiply the final result by 3.

3. Complexity Analysis:
   - Time Complexity: At row $r$, advancing the frontier requires $r$ sub-steps over $3^r$ states.
     Total time is $\sum_{r=1}^N O(r \cdot 3^N) = O(N \cdot 3^N)$.
     For $N = 8$, this requires $\sim 5 \times 10^4$ state updates, completing in $\sim 0.05$ seconds.
   - Space Complexity: $O(3^N)$ to store the DP state count array of size $3^8 = 6561$.
"""

import unittest
from util.utils import timeit


class Problem189:
    def __init__(self, n: int = 8):
        self.n = n

    @timeit
    def solve(self) -> int:
        if self.n <= 0:
            return 0
        if self.n == 1:
            return 3

        # Precompute down-triangle valid coloring count: 3 - len({u, v1, v2})
        w = [[[0] * 3 for _ in range(3)] for _ in range(3)]
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    w[a][b][c] = 3 - len({a, b, c})

        # dp[state] = number of valid colorings for the frontier of up-triangles
        # Base case: top triangle fixed to color 0 (multiplied by 3 at the end for symmetry)
        dp = [0] * 3
        dp[0] = 1

        for r in range(2, self.n + 1):
            sz = 3**r
            pow3_r_minus_1 = 3 ** (r - 1)
            cur_dp = [0] * sz

            # Step 0: expand state from length r-1 (size 3^{r-1}) to length r by choosing v0
            for st, count in enumerate(dp):
                if count:
                    cur_dp[st * 3] += count
                    cur_dp[st * 3 + 1] += count
                    cur_dp[st * 3 + 2] += count

            # Steps 1 to r-1: choose v_j and resolve down-triangle D_{r, j-1}
            for _ in range(1, r):
                next_dp = [0] * sz
                for st, count in enumerate(cur_dp):
                    if not count:
                        continue
                    v_prev = st % 3
                    st //= 3
                    u_prev = st % 3
                    rest = st // 3
                    w_row = w[v_prev][u_prev]
                    base_nst = rest * 3 + v_prev * pow3_r_minus_1
                    for vj in (0, 1, 2):
                        ways = w_row[vj]
                        if ways:
                            next_dp[base_nst + vj] += count * ways
                cur_dp = next_dp

            # Rotate cyclic frontier to align canonical coordinate order (v_0, ..., v_{r-1})
            dp = [0] * sz
            for st, count in enumerate(cur_dp):
                if count:
                    rot = (st // 3) + (st % 3) * pow3_r_minus_1
                    dp[rot] += count

        return 3 * sum(dp)


class Solution189(unittest.TestCase):
    def setUp(self):
        self.problem = Problem189()

    def test_samples(self):
        self.assertEqual(3, Problem189(1).solve())
        self.assertEqual(24, Problem189(2).solve())
        self.assertEqual(528, Problem189(3).solve())
        self.assertEqual(31968, Problem189(4).solve())

    def test_solution(self):
        self.assertEqual(10834893628237824, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
