"""
PROBLEM

The function f is defined for all positive integers as follows:
f(1) = 1
f(2n) = 2f(n)
f(2n + 1) = 2n + 1 + 2f(n) + f(n)/n

It can be proven that f(n) is integer for all values of n.

The function S(n) is defined as S(n) = sum_{i=1 to n} f(i)^2.

For example, S(10) = 1530 and S(10^2) = 4798445.

Find S(10^16). Give your answer modulo 1,000,000,007.

ANSWER: 282771304
Solve time: ~0.002 seconds

---
MATHEMATICAL DERIVATION:

1. Reduction of f(n) to n * popcount(n):
   Let h(n) = f(n) / n.
   - Base case: h(1) = f(1) / 1 = 1.
   - Even recurrence:
       h(2n) = f(2n) / (2n) = 2 f(n) / (2n) = f(n) / n = h(n).
   - Odd recurrence:
       h(2n + 1) = f(2n + 1) / (2n + 1)
                 = (2n + 1 + 2 f(n) + f(n) / n) / (2n + 1)
                 = (2n + 1 + 2n h(n) + h(n)) / (2n + 1)
                 = (2n + 1)(1 + h(n)) / (2n + 1)
                 = 1 + h(n).
   By mathematical induction on the binary representation of n, h(n) equals the
   number of set bits (popcount / Hamming weight) in the binary expansion of n:
       h(n) = popcount(n) = w(n).
   Therefore, f(n) = n * w(n), and the target summation becomes:
       S(N) = sum_{n=1}^N f(n)^2 = sum_{n=1}^N n^2 w(n)^2 (mod 10^9 + 7).

2. Binary Prefix Decomposition (Digit DP / Divide & Conquer):
   To compute sum_{n=0}^N n^2 w(n)^2 (note n=0 contributes 0) for N = 10^16:
   We inspect the binary digits of N + 1. For every bit position k where the
   bit of N + 1 is 1, branching the k-th bit to 0 allows all lower k bits to
   freely span the entire range y in [0, 2^k - 1].
   Each number x in this complete block has:
       x = P + y,  w(x) = w_p + w(y)
   where P is the fixed prefix value shifted to position k + 1, and w_p is the
   popcount of the prefix.

3. Summation Expansion over Complete Blocks:
   Expanding x^2 w(x)^2 for x = P + y and w(x) = w_p + w_y:
       x^2 w(x)^2 = (P + y)^2 (w_p + w_y)^2
                  = (sum_{a=0}^2 binom(2, a) P^{2-a} y^a) * (sum_{b=0}^2 binom(2, b) w_p^{2-b} w_y^b)
   Summing over all y in [0, 2^k - 1]:
       sum_{y=0}^{2^k - 1} x^2 w(x)^2 = sum_{a=0}^2 sum_{b=0}^2 binom(2, a) binom(2, b) P^{2-a} w_p^{2-b} E_k(a, b)
   where E_k(a, b) = sum_{y=0}^{2^k - 1} y^a (w(y))^b.

4. Moment Recurrence for E_k(a, b):
   Partitioning [0, 2^k - 1] into lower half [0, 2^{k-1} - 1] and upper half [2^{k-1}, 2^k - 1]:
   Upper half values are B + y and have popcounts 1 + w(y), with B = 2^{k-1}.
   Using the binomial theorem:
       E_k(a, b) = E_{k-1}(a, b) + sum_{i=0}^a sum_{j=0}^b binom(a, i) binom(b, j) B^{a-i} E_{k-1}(i, j).
   Base case (k = 0, set {0}):
       E_0(0, 0) = 1, and E_0(a, b) = 0 for (a, b) != (0, 0).

5. Complexity:
   Precomputing E_k(a, b) for k <= 60 takes O(log N) operations with a tiny constant (3x3 state).
   The prefix scan also takes O(log N). Total runtime is ~0.002 seconds.
"""

from typing import List
import unittest
from util.utils import timeit


def compute_block_moments(max_k: int, mod: int) -> List[List[List[int]]]:
    """
    Compute E_k(a, b) = sum_{y=0}^{2^k - 1} y^a w(y)^b mod `mod`
    for 0 <= k <= max_k and 0 <= a, b <= 2.
    """
    e_table = [[[0] * 3 for _ in range(3)] for _ in range(max_k + 1)]
    e_table[0][0][0] = 1  # 0^0 * w(0)^0 = 1

    binom = [[1, 0, 0], [1, 1, 0], [1, 2, 1]]
    for k in range(1, max_k + 1):
        b = pow(2, k - 1, mod)
        for a in range(3):
            for b_idx in range(3):
                val = e_table[k - 1][a][b_idx]
                for i in range(a + 1):
                    for j in range(b_idx + 1):
                        coeff = binom[a][i] * binom[b_idx][j] * pow(b, a - i, mod) % mod
                        val = (val + coeff * e_table[k - 1][i][j]) % mod
                e_table[k][a][b_idx] = val
    return e_table


class Problem759:
    def __init__(self, mod: int = 1_000_000_007):
        self.mod = mod
        self.e_table = compute_block_moments(65, self.mod)
        self.binom = [[1, 0, 0], [1, 1, 0], [1, 2, 1]]

    @timeit
    def solve(self, n: int = 10**16) -> int:
        """
        Compute S(n) = sum_{i=1}^n f(i)^2 mod self.mod in O(log n) time.
        """
        mod = self.mod
        total = 0
        cur_p = 0
        cur_w = 0

        # Binary digits of n + 1
        bits = [int(c) for c in bin(n + 1)[2:]]
        length = len(bits)

        for idx, bit in enumerate(bits):
            k = length - 1 - idx
            if bit == 1:
                # Set bit k to 0; lower k bits range freely in [0, 2^k - 1]
                p_val = (cur_p * pow(2, k + 1, mod)) % mod
                w_val = cur_w

                for i in range(3):
                    for j in range(3):
                        coeff_p = self.binom[2][i] * pow(p_val, 2 - i, mod) % mod
                        coeff_w = self.binom[2][j] * pow(w_val, 2 - j, mod) % mod
                        coeff = (coeff_p * coeff_w) % mod
                        total = (total + coeff * self.e_table[k][i][j]) % mod

                cur_p = (cur_p * 2 + 1) % mod
                cur_w += 1
            else:
                cur_p = (cur_p * 2) % mod

        return total % mod


class Solution759(unittest.TestCase):
    def setUp(self):
        self.problem = Problem759()

    def test_solution_very_small(self):
        self.assertEqual(1530, self.problem.solve(n=10))

    def test_solution_small(self):
        self.assertEqual(4798445, self.problem.solve(n=100))

    def test_solution_1e5(self):
        self.assertEqual(405942229, self.problem.solve(n=int(1e5)))

    def test_solution_final(self):
        self.assertEqual(282771304, self.problem.solve(n=10**16))


if __name__ == '__main__':
    unittest.main()
