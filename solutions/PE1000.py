"""
PROBLEM

This problem contains three sub-problems (I, X, C) and a meta-problem (M).

1. Sub-problem: Max And (I)
   The numbers 1 to n are to be divided into two groups A and B. Let I(n) be the maximum possible value of
     sum_{a in A} sum_{b in B} (a & b)
   where & is the bitwise AND operator.
   I(10) = 50. Find I(1000).

2. Sub-problem: Max Xor Sum (X)
   For two integers x, y, write [x, y] for the bitwise XOR of x^2 and y^2.
   A finite sequence of integers a_0, a_1, ..., a_r satisfies:
   - 1 <= a_i <= N for all 0 <= i <= r;
   - [a_{i-1}, a_i] < [a_i, a_{i+1}] for all 0 < i < r.
   Let X(N) be the maximal possible value of sum_{i=1}^r [a_{i-1}, a_i].
   X(4) = 71 and X(10) = 702. Find X(1000).

3. Sub-problem: Unreachable Nim (C)
   Two players are playing a three-pile Nim game. The game status is an ordered triple (a, b, c).
   A player will always make a winning move if there is at least one; otherwise, any valid move can be made.
   A game status is called unreachable if it never appears during the game, unless when it is the initial position.
   Let C(N) be the number of unreachable statuses with 0 <= a, b, c < N.
   C(10) = 123. Find C(1000).

4. Meta-problem (M)
   A sequence M is defined by:
   - M(0) = I(1000);
   - M(1) = X(1000);
   - M(2) = C(1000);
   - M(k) = M(k-1) * M(k-2) * M(k-3) for k >= 3.
   You are given M(4) = 457587170 (mod 10^9 + 7).
   Find M(1000) mod (10^9 + 7).

ANSWER: 891213201
Solve time: ~0.6 seconds

---
MATHEMATICAL & ALGEBRAIC DERIVATION:

1. Sub-problem I (Max And):
   Decomposing the bitwise AND by bit positions k >= 0 (where b_k(x) in {0, 1} is the k-th bit of x):
     sum_{a in A} sum_{b in B} (a & b) = sum_{k >= 0} 2^k * (sum_{a in A} b_k(a)) * (sum_{b in B} b_k(b)).
   Let S_k = sum_{x=1}^n b_k(x) be the count of integers in {1, ..., n} with bit k set, and a_k = sum_{a in A} b_k(a).
   Then sum_{b in B} b_k(b) = S_k - a_k, and each product a_k * (S_k - a_k) is bounded above by
   floor(S_k / 2) * ceil(S_k / 2).
   Constructive Proof of Simultaneous Achievability:
   Place 1 in B, and group all remaining integers into pairs (2m, 2m + 1) for m >= 1.
   Since 2m and 2m + 1 share identical bits at all positions k >= 1, placing one member of each pair in A and the
   other in B gives zero discrepancy (a_k - b_k = 0) on every completed pair for all k >= 1, while alternating
   which member goes to A balances bit k = 0 so |a_0 - b_0| <= 1. At most one element (n when n is even) is
   unpaired, ensuring |a_k - b_k| <= 1 for every bit k >= 0 simultaneously.
   Hence:
     I(n) = sum_{k >= 0} 2^k * floor(S_k / 2) * ceil(S_k / 2),   giving I(1000) = 61,217,340.

2. Sub-problem X (Max Xor Sum):
   A valid sequence a_0, a_1, ..., a_r is a walk in the complete graph K_N with strictly increasing edge weights
   w(u, v) = u^2 ^ v^2.
   Because u -> u^2 is injective on {1, ..., N}, if two edges (u, v_1) and (u, v_2) share an endpoint u and have
   the same weight u^2 ^ v_1^2 = u^2 ^ v_2^2, then v_1^2 = v_2^2 => v_1 = v_2.
   Thus, edges of any fixed weight w are strictly vertex-disjoint (they form a matching).
   Sorting all N(N - 1)/2 edges in increasing order of weight w and updating endpoints simultaneously:
     dp[u], dp[v] = max(dp[u], dp[v] + w), max(dp[v], dp[u] + w)
   computes the exact maximum walk sum X(1000) = 728,513,240.

3. Sub-problem C (Unreachable Nim):
   In 3-pile Nim:
   - Every P-position (a ^ b ^ c = 0) is reachable from an N-position (e.g., (a + 1, b, c) -> (a, b, c)).
   - From any N-position (a' ^ b' ^ c' != 0), at least one winning move exists, so the player must transition to
     a P-position.
   - Therefore, an N-position (a, b, c) is reachable if and only if it can be reached in one move from some
     P-position (a', b, c), (a, b', c), or (a, b, c'), which requires a' = b ^ c > a, b' = a ^ c > b, or
     c' = a ^ b > c.
   Consequently, (a, b, c) is unreachable if and only if:
     (a ^ b ^ c != 0)  AND  (b ^ c < a)  AND  (a ^ c < b)  AND  (a ^ b < c).
   Let k be the most significant bit of x = a ^ b ^ c != 0. For all bits i > k, (a ^ b ^ c)_i = 0, so
   (b ^ c)_i = a_i, (a ^ c)_i = b_i, and (a ^ b)_i = c_i (all three comparisons are tied above bit k).
   At bit k, (a ^ b ^ c)_k = 1, so either one of (a_k, b_k, c_k) is 1 (which violates two inequalities) or all
   three are 1: a_k = b_k = c_k = 1 (which satisfies all three strict inequalities simultaneously!).
   Counting triples (a, b, c) in {0, ..., N - 1}^3 by the highest bit k where a_k = b_k = c_k = 1 and
   (a >> (k + 1)) ^ (b >> (k + 1)) ^ (c >> (k + 1)) = 0 gives C(1000) = 232,607,184.

4. Meta-problem M:
   With M(0) = 61,217,340, M(1) = 728,513,240, and M(2) = 232,607,184:
   - M(3) = M(0) * M(1) * M(2)
   - M(4) = M(3) * M(2) * M(1) = M(0) * M(1)^2 * M(2)^2 = 457,587,170 (mod 10^9 + 7), matching the given check!
   Iterating M(k) = M(k-1) * M(k-2) * M(k-3) mod (10^9 + 7) up to k = 1000 yields M(1000) = 891,213,201.
"""

import unittest
from util.utils import timeit


class Problem1000:
    MOD = 10**9 + 7

    def __init__(self):
        pass

    @staticmethod
    def compute_i(n: int) -> int:
        total = 0
        k = 0
        while (1 << k) <= n:
            full_cycles = (n + 1) >> (k + 1)
            rem = (n + 1) & ((1 << (k + 1)) - 1)
            s_k = full_cycles * (1 << k) + max(0, rem - (1 << k))
            total += (1 << k) * (s_k // 2) * (s_k - s_k // 2)
            k += 1
        return total

    @staticmethod
    def compute_x(n: int) -> int:
        sq = [i * i for i in range(n + 1)]
        edges = [
            ((sq[u] ^ sq[v]) << 20) | (u << 10) | v
            for u in range(1, n + 1)
            for v in range(u + 1, n + 1)
        ]
        edges.sort()
        dp = [0] * (n + 1)
        for e in edges:
            w = e >> 20
            u = (e >> 10) & 0x3FF
            v = e & 0x3FF
            du = dp[u]
            dv = dp[v]
            if dv + w > du:
                dp[u] = dv + w
            if du + w > dv:
                dp[v] = du + w
        return max(dp)

    @staticmethod
    def compute_c(n: int) -> int:
        total = 0
        k = 0
        while (1 << k) < n:
            max_u = n >> (k + 1)
            rem = n & ((1 << (k + 1)) - 1)
            w = [1 << k] * max_u + [max(0, rem - (1 << k))]
            m = len(w)
            for ua in range(m):
                wa = w[ua]
                if wa == 0:
                    continue
                for ub in range(m):
                    wb = w[ub]
                    if wb == 0:
                        continue
                    uc = ua ^ ub
                    if uc < m:
                        total += wa * wb * w[uc]
            k += 1
        return total

    def compute_m(self, target_k: int) -> int:
        m = [
            self.compute_i(1000) % self.MOD,
            self.compute_x(1000) % self.MOD,
            self.compute_c(1000) % self.MOD,
        ]
        for k in range(3, target_k + 1):
            m.append((m[k - 1] * m[k - 2] * m[k - 3]) % self.MOD)
        return m[target_k]

    @timeit
    def solve(self) -> int:
        return self.compute_m(1000)


class Solution1000(unittest.TestCase):
    def setUp(self):
        self.problem = Problem1000()

    def test_sample(self):
        self.assertEqual(50, self.problem.compute_i(10))
        self.assertEqual(71, self.problem.compute_x(4))
        self.assertEqual(702, self.problem.compute_x(10))
        self.assertEqual(123, self.problem.compute_c(10))
        self.assertEqual(457587170, self.problem.compute_m(4))

    def test_solution(self):
        self.assertEqual(891213201, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
