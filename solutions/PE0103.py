r"""
PROBLEM

Let $S(A)$ represent the sum of elements in set $A$ of size $n$. We shall call it a special sum set if for any two non-empty disjoint subsets, $B$ and $C$, the following properties are true:

1. $S(B) \ne S(C)$; that is, sums of subsets cannot be equal.
2. If $B$ contains more elements than $C$ then $S(B) \gt S(C)$.

If $S(A)$ is minimised for a given $n$, we shall call it an optimum special sum set. The first five optimum special sum sets are given below.

$n = 1$: $\{1\}$
$n = 2$: $\{1, 2\}$
$n = 3$: $\{2, 3, 4\}$
$n = 4$: $\{3, 5, 6, 7\}$
$n = 5$: $\{6, 9, 11, 12, 13\}$

It seems that for a given optimum set, $A = \{a_1, a_2, \dots, a_n\}$, the next optimum set is of the form $B = \{b, a_1 + b, a_2 + b, \dots, a_n + b\}$, where $b$ is the "middle" element on the previous row.

By applying this "rule" we would expect the optimum set for $n = 6$ to be $A = \{11, 17, 20, 22, 23, 24\}$, with $S(A) = 117$. However, this is not the optimum set, as we have merely applied an algorithm to provide a near optimum set. The optimum set for $n = 6$ is $A = \{11, 18, 19, 20, 22, 25\}$, with $S(A) = 115$ and corresponding set string: 111819202225.

Given that $A$ is an optimum special sum set for $n = 7$, find its set string.

NOTE: This problem is related to Problem 105 and Problem 106.

ANSWER: 20313839404245
Solve time: ~0.18 seconds

---
MATHEMATICAL DERIVATION:

1. Special Sum Set Properties & Reductions:
   - Condition 1 (Subset Sum Uniqueness):
     No two non-empty disjoint subsets have equal sums. Equivalently, all $2^n$ subset sums must be distinct:
     if $S(X) = S(Y)$, then $X \setminus Y$ and $Y \setminus X$ are disjoint subsets with equal sum.
   - Condition 2 (Cardinality Dominance):
     If $|B| > |C|$, then $S(B) > S(C)$. For a sorted set $a_1 < a_2 < \dots < a_n$, it is necessary and sufficient
     that for all $k \in [1, \lfloor (n-1)/2 \rfloor]$, the sum of the smallest $k+1$ elements exceeds the sum
     of the largest $k$ elements:
     $$\sum_{i=1}^{k+1} a_i > \sum_{j=0}^{k-1} a_{n-j}$$
     By transitivity, this guarantees $S(B) > S(C)$ for any $B, C$ with $|B| > |C|$.

2. Branch-and-Bound Search:
   - Near-Optimum Upper Bound:
     Starting from the optimum set for $n-1$, we construct the near-optimum heuristic set:
     $B = \{b, a_1+b, \dots, a_{n-1}+b\}$ where $b = A_{n-1}[\lfloor (n-1)/2 \rfloor]$.
     Its sum provides a tight initial upper bound $S_{\max}$ on the search space.
   - Bitmask Subset Sum Collision Detection:
     We maintain an integer bitmask `mask` where bit $s$ is 1 iff subset sum $s$ is generated.
     Adding candidate element $v$ introduces new subset sums `mask << v`.
     If `mask & (mask << v) != 0`, a collision occurs and the branch is pruned in $O(1)$.
   - Pruning & Bounds:
     - Minimal remaining sum: with $rem = n - idx$ elements left, the minimal sum addition is
       $rem \cdot (a_{idx} + 1) + rem(rem - 1)/2$.
     - Upper bound on candidate $v$: $v \le \lfloor (S_{\max} - 1 - cur\_sum - rem(rem-1)/2) / rem \rfloor$.
     - Condition 2 upper bounds:
       $a_n < a_1 + a_2 \implies v \le a_1 + a_2 - rem$.
       When choosing the final element ($idx = n-1$), $v \le \sum_{i=1}^{k+1} a_i - 1 - \sum_{j=1}^{k-1} a_{n-j}$ for each $k$.

3. Complexity Analysis:
   - Time Complexity: The branch-and-bound tree with bitmask collision pruning explores < 5,000 nodes for $n=7$,
     executing in under 0.20 seconds in pure Python.
   - Space Complexity: $O(n)$ recursion stack and $O(1)$ bitmask storage (since sums are $\le 255$).
"""

import unittest
from util.utils import timeit


class Problem103:
    def __init__(self, n: int = 7):
        self.n = n

    def find_optimum(self, n: int, prev_opt: list[int] | None = None) -> list[int]:
        if n == 1:
            return [1]

        # Use near-optimum rule from previous row as initial upper bound
        if prev_opt is not None:
            mid = prev_opt[len(prev_opt) // 2]
            near = sorted([mid] + [x + mid for x in prev_opt])
        else:
            near = None

        best: list = [sum(near) if near else float('inf'), near]

        def dfs(idx: int, cur_set: tuple[int, ...], cur_sum: int, mask: int) -> None:
            if idx == n:
                # Validate condition 2
                for k in range(1, (n + 1) // 2):
                    if sum(cur_set[: k + 1]) <= sum(cur_set[-k:]):
                        return
                if cur_sum < best[0]:
                    best[0] = cur_sum
                    best[1] = list(cur_set)
                return

            rem_count = n - idx
            min_rem = (
                rem_count * (cur_set[-1] + 1) + rem_count * (rem_count - 1) // 2
                if idx > 0
                else rem_count * (rem_count + 1) // 2
            )
            if cur_sum + min_rem >= best[0]:
                return

            start_val = cur_set[-1] + 1 if idx > 0 else 1
            max_val = (best[0] - 1 - cur_sum - rem_count * (rem_count - 1) // 2) // rem_count

            if idx >= 2:
                max_val = min(max_val, cur_set[0] + cur_set[1] - rem_count)

            if idx == n - 1:
                for k in range(1, (n + 1) // 2):
                    bound = sum(cur_set[: k + 1]) - 1 - sum(cur_set[-(k - 1) :] if k > 1 else [])
                    max_val = min(max_val, bound)

            for val in range(start_val, max_val + 1):
                val_shift = mask << val
                if mask & val_shift:
                    continue

                dfs(idx + 1, cur_set + (val,), cur_sum + val, mask | val_shift)

        dfs(0, (), 0, 1)
        return best[1]

    @timeit
    def solve(self) -> str:
        # Build optimum sets iteratively from 1 to self.n
        opt: list[int] | None = None
        for k in range(1, self.n + 1):
            opt = self.find_optimum(k, opt)
        return "".join(map(str, opt))


class Solution103(unittest.TestCase):
    def setUp(self):
        self.problem = Problem103()

    def test_samples(self):
        # Known optimum sets from problem statement
        p = Problem103()
        self.assertEqual("1", Problem103(1).solve())
        self.assertEqual("12", Problem103(2).solve())
        self.assertEqual("234", Problem103(3).solve())
        self.assertEqual("3567", Problem103(4).solve())
        self.assertEqual("69111213", Problem103(5).solve())
        self.assertEqual("111819202225", Problem103(6).solve())

    def test_solution(self):
        self.assertEqual("20313839404245", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
