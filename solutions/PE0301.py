r"""
PROBLEM

Nim is a game played with heaps of stones, where two players take it in turn to remove any number of stones from any heap until no stones remain.

We'll consider the three-heap normal-play version of Nim, which works as follows:
- At the start of the game there are three heaps of stones.
- On each player's turn, the player may remove any positive number of stones from any single heap.
- The first player unable to move (because no stones remain) loses.

If $(n_1,n_2,n_3)$ indicates a Nim position consisting of heaps of size $n_1$, $n_2$, and $n_3$, then there is a simple function, which you may look up or attempt to deduce for yourself, $X(n_1,n_2,n_3)$ that returns:

zero if, with perfect strategy, the player about to move will eventually lose; or
non-zero if, with perfect strategy, the player about to move will eventually win.

For example $X(1,2,3) = 0$ because, no matter what the current player does, the opponent can respond with a move that leaves two heaps of equal size, at which point every move by the current player can be mirrored by the opponent until no stones remain; so the current player loses. To illustrate:

- current player moves to $(1,2,1)$
- opponent moves to $(1,0,1)$
- current player moves to $(0,0,1)$
- opponent moves to $(0,0,0)$, and so wins.

For how many positive integers $n \le 2^{30}$ does $X(n,2n,3n) = 0$ ?

ANSWER: 2178309
Solve time: ~0.000001 seconds

---
MATHEMATICAL DERIVATION:

1. Nim-Sum and Winning/Losing Positions:
   In normal-play Nim with heap sizes $(n_1, n_2, n_3)$, Bouton's Theorem (1901) establishes that a position
   is a losing position (P-position) if and only if the bitwise XOR sum (nim-sum) across all heap sizes is zero:
       $$X(n_1, n_2, n_3) = n_1 \oplus n_2 \oplus n_3 = 0$$

2. Algebraic Reduction for $X(n, 2n, 3n) = 0$:
   Here $n_1 = n$, $n_2 = 2n$, and $n_3 = 3n = n + 2n$.
   Since bitwise XOR is associative, commutative, and self-inverting ($a \oplus a = 0$):
       $$n \oplus 2n \oplus 3n = 0 \iff n \oplus 2n = 3n$$
   For any non-negative integers $a$ and $b$, arithmetic addition and XOR addition are related by:
       $$a + b = (a \oplus b) + 2(a \ \& \ b)$$
   where $\&$ denotes bitwise AND.
   Therefore:
       $$a \oplus b = a + b \iff a \ \& \ b = 0$$
   Substituting $a = n$ and $b = 2n$:
       $$n \oplus 2n = 3n \iff n \ \& \ (2n) = 0$$

3. Binary Representation Condition:
   Because $2n = n \ll 1$ (shifting $n$ left by 1 bit in binary), the condition $n \ \& \ (2n) = 0$ holds
   if and only if there is no bit index $i$ where both the $i$-th and $(i+1)$-th bits of $n$ are 1.
   Thus, $X(n, 2n, 3n) = 0$ is equivalent to:
       "The binary representation of $n$ contains no adjacent ones (no consecutive `11` substrings)."

4. Counting via Fibonacci Numbers:
   - For any integer $0 \le n < 2^k$, its binary representation consists of at most $k$ bits.
   - Let $a_k$ be the number of binary strings of length $k$ containing no adjacent 1s.
   - Any valid string of length $k$ either:
     - Ends in `0`: preceded by any valid string of length $k-1$ ($a_{k-1}$ possibilities).
     - Ends in `1`: must be preceded by `0` (for $k \ge 2$), hence preceded by any valid string of length $k-2$ ($a_{k-2}$ possibilities).
   - This yields the standard Fibonacci recurrence:
       $$a_k = a_{k-1} + a_{k-2}, \quad a_0 = 1, \; a_1 = 2, \; a_2 = 3, \; a_3 = 5, \dots$$
   - In terms of the standard Fibonacci sequence ($F_1 = 1, F_2 = 1, F_3 = 2, F_4 = 3, \dots$):
       $$a_k = F_{k+2}$$
   - The range $0 \le n < 2^k$ contains $F_{k+2}$ valid integers.
   - Excluding $n = 0$, there are $F_{k+2} - 1$ valid positive integers strictly less than $2^k$.
   - The upper bound $n = 2^k$ has binary form $100\dots0_2$ ($1$ followed by $k$ zeros), which contains no adjacent 1s,
     and indeed $2^k \ \& \ 2^{k+1} = 0$. Thus $n = 2^k$ is always valid.
   - Total valid positive integers $1 \le n \le 2^k$:
       $$\text{Count}(2^k) = (F_{k+2} - 1) + 1 = F_{k+2}$$

5. Final Calculation for $n \le 2^{30}$:
   Setting $k = 30$:
       $$\text{Count}(2^{30}) = F_{30+2} = F_{32} = 2\,178\,309$$

6. Complexity Analysis:
   - Time Complexity: $O(k)$ to compute the $(k+2)$-th Fibonacci term (or $O(\log k)$ via matrix exponentiation).
     For $k = 30$, execution time is $< 1\,\mu\text{s}$.
   - Space Complexity: $O(1)$ auxiliary memory.
"""

import unittest
from util.utils import timeit


class Problem301:
    def __init__(self):
        pass

    @staticmethod
    def fibonacci(m: int) -> int:
        """Compute the m-th Fibonacci number with F_1 = 1, F_2 = 1, F_3 = 2, ..."""
        if m <= 0:
            return 0
        a, b = 0, 1
        for _ in range(m):
            a, b = b, a + b
        return a

    @timeit
    def solve(self, max_exp: int = 30) -> int:
        """
        Count the number of positive integers 1 <= n <= 2^max_exp such that X(n, 2n, 3n) = 0.
        By reduction, this equals the (max_exp + 2)-th Fibonacci number F_{max_exp + 2}.
        """
        return self.fibonacci(max_exp + 2)


class Solution301(unittest.TestCase):
    def setUp(self):
        self.problem = Problem301()

    def test_samples_brute_force(self):
        """Verify against direct simulation / brute force for small exponents."""
        for exp in range(1, 14):
            limit = 1 << exp
            expected = sum(1 for n in range(1, limit + 1) if (n ^ (2 * n) ^ (3 * n)) == 0)
            self.assertEqual(expected, self.problem.solve(exp))

    def test_sample_exp_1(self):
        self.assertEqual(2, self.problem.solve(1))

    def test_sample_exp_2(self):
        self.assertEqual(3, self.problem.solve(2))

    def test_sample_exp_3(self):
        self.assertEqual(5, self.problem.solve(3))

    def test_solution(self):
        self.assertEqual(2178309, self.problem.solve(30))


if __name__ == '__main__':
    unittest.main()
