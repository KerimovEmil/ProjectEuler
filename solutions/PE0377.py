r"""
PROBLEM

There are 16 positive integers that do not contain the digit zero and have a digit sum of 5, namely:
5, 14, 23, 32, 41, 113, 122, 131, 212, 221, 311, 1112, 1121, 1211, 2111, and 11111.
Their sum is 17,891.

Let $f(n)$ be the sum of all positive integers that do not contain the digit zero and have a digit sum of $n$.

Find $\sum_{i=1}^{17} f(13^i)$.
Give the last 9 digits as your answer.

ANSWER: 732385277
Solve time: ~0.005 seconds

---
MATHEMATICAL DERIVATION:

1. Recurrence Relations for Count and Sum of Numbers:
   Let $c(n)$ denote the number of positive integers without the digit 0 whose digits sum to $n$.
   Let $f(n)$ denote the sum of all such positive integers.

   Any valid integer with digit sum $n$ can be uniquely obtained by taking a valid integer
   with digit sum $n - d$ and appending the digit $d \in \{1, 2, \dots, 9\}$ to the right.
   Appending digit $d$ to an integer $x$ produces $10x + d$.

   Summing over all valid integers $x$ with digit sum $n - d$:
   $$\sum_{x} (10x + d) = 10 \sum_x x + d \sum_x 1 = 10 f(n - d) + d \cdot c(n - d)$$

   Summing across all possible choices for the last digit $d \in \{1, \dots, 9\}$:
   $$c(n) = \sum_{d=1}^9 c(n - d)$$
   $$f(n) = 10 \sum_{d=1}^9 f(n - d) + \sum_{d=1}^9 d \cdot c(n - d)$$

   Base conditions at $n = 0$:
   - Empty sequence has digit sum 0: $c(0) = 1, f(0) = 0$.
   - For $k < 0$: $c(k) = 0, f(k) = 0$.

2. Linear State Space Formulation:
   We define the 18-dimensional state vector at step $n$:
   $$V(n) = [c(n), c(n-1), \dots, c(n-8), f(n), f(n-1), \dots, f(n-8)]^T$$

   The step transition $V(n+1) = M V(n)$ is represented by an $18 \times 18$ matrix $M$:
   - Row 0: $c(n+1) = \sum_{j=0}^8 c(n-j) \implies M[0, j] = 1$ for $0 \le j \le 8$.
   - Rows 1..8: $c(n+1-i) = c(n - (i-1)) \implies M[i, i-1] = 1$ for $1 \le i \le 8$.
   - Row 9: $f(n+1) = \sum_{j=0}^8 (j+1) c(n-j) + 10 \sum_{j=0}^8 f(n-j) \implies M[9, j] = j+1$ and $M[9, 9+j] = 10$ for $0 \le j \le 8$.
   - Rows 10..17: $f(n+1-i) = f(n - (i-1)) \implies M[9+i, 9+i-1] = 1$ for $1 \le i \le 8$.

3. Fast Matrix Exponentiation Modulo $10^9$:
   Given initial vector $V(0) = [1, 0, \dots, 0]^T$:
   $$V(N) = M^N V(0) \implies f(N) = V(N)[9] = (M^N)[9, 0] \pmod{10^9}$$

   Using binary exponentiation `mat_pow(M, N, 10^9)`, computing each $f(13^i)$ requires
   $O(18^3 \log(13^i))$ operations.
   For $i = 1, \dots, 17$, the total sum is computed in just a few milliseconds.
"""

import unittest
from typing import List
from util.utils import timeit, mat_pow


def build_transition_matrix() -> List[List[int]]:
    """
    Constructs the 18x18 companion transition matrix for (c(n), f(n)).
    """
    m = [[0] * 18 for _ in range(18)]

    # Row 0: c(n+1) = sum_{j=0..8} c(n-j)
    for j in range(9):
        m[0][j] = 1

    # Rows 1..8: shift c history
    for i in range(1, 9):
        m[i][i - 1] = 1

    # Row 9: f(n+1) = sum_{j=0..8} (j+1)*c(n-j) + 10*sum_{j=0..8} f(n-j)
    for j in range(9):
        m[9][j] = j + 1
        m[9][9 + j] = 10

    # Rows 10..17: shift f history
    for i in range(1, 9):
        m[9 + i][9 + i - 1] = 1

    return m


def compute_f(n: int, mod: int = 10**9) -> int:
    """
    Compute f(n) mod `mod`, where f(n) is the sum of positive integers
    without digit 0 whose digits sum to n.
    """
    if n <= 0:
        return 0
    m = build_transition_matrix()
    m_pow = mat_pow(m, n, mod=mod)
    # V(0) has V(0)[0] = 1 and all other entries 0.
    # Therefore, f(n) = V(n)[9] = (M^n)[9][0].
    return m_pow[9][0] % mod


class Problem377:
    def __init__(self):
        pass

    @timeit
    def solve(self, max_power: int = 17, base: int = 13, mod: int = 10**9) -> int:
        """
        Compute sum_{i=1}^{max_power} f(base^i) mod `mod`.
        """
        m = build_transition_matrix()
        total = 0
        power_val = base
        for _ in range(1, max_power + 1):
            m_pow = mat_pow(m, power_val, mod=mod)
            total = (total + m_pow[9][0]) % mod
            power_val *= base
        return total


class Solution377(unittest.TestCase):
    def setUp(self):
        self.problem = Problem377()

    def test_sample_f5(self):
        self.assertEqual(17891, compute_f(5))

    def test_sample_small_cases(self):
        self.assertEqual(1, compute_f(1))
        self.assertEqual(13, compute_f(2))
        self.assertEqual(147, compute_f(3))
        self.assertEqual(1625, compute_f(4))

    def test_solution(self):
        self.assertEqual(732385277, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
