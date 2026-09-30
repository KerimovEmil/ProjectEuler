r"""
PROBLEM

Define $g(n, m)$ to be the largest integer $k$ such that $2^k$ divides $\binom{n}m$.
For example, $\binom{12}5 = 792 = 2^3 \cdot 3^2 \cdot 11$, hence $g(12, 5) = 3$.
Then define $F(n) = \max \{ g(n, m) : 0 \le m \le n \}$. $F(10) = 3$ and $F(100) = 6$.

Let $S(N)$ = $\displaystyle\sum_{n=1}^N{F(n)}$. You are given that $S(100) = 389$ and $S(10^7) = 203222840$.

Find $S(10^{16})$.

ANSWER: 501985601490518144
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Kummer's Theorem and Maximal Carry Analysis:
   - By Kummer's theorem, $g(n, m) = v_2\left(\binom{n}{m}\right)$ equals the number of carries when adding
     $m$ and $n - m$ in binary base 2.
   - Let $k = v_2(n+1)$, which represents the number of trailing 1s in the binary representation of $n$.
   - In any binary addition $m + (n - m) = n$, if bit $i$ of $n$ is 1, then $m_i + (n-m)_i + c_i = 1 + 2 c_{i+1}$,
     which forces $c_{i+1} = c_i$. Since $c_0 = 0$, no carries can occur at the first $k$ bit positions $0, \dots, k-1$.
   - At bit position $k$ (where $n_k = 0$), setting $m_k = 1$ and $(n-m)_k = 1$ produces carry $c_{k+1} = 1$.
   - This carry can be propagated across all remaining higher bit positions up to $\lfloor \log_2(n+1) \rfloor$.
   - Therefore, the maximal number of carries is:
     $$F(n) = \lfloor \log_2(n+1) \rfloor - v_2(n+1)$$

2. Closed-Form Summation via Legendre's Formula:
   - Setting $M = N + 1$, the prefix sum $S(N) = \sum_{n=1}^N F(n)$ transforms by shifting the index $m = n + 1$:
     $$S(N) = \sum_{m=2}^M (\lfloor \log_2(m) \rfloor - v_2(m)) = \sum_{m=1}^M \lfloor \log_2(m) \rfloor - \sum_{m=1}^M v_2(m)$$
   - The first term sums $\lfloor \log_2(m) \rfloor = j$ over intervals $[2^j, \min(M, 2^{j+1}-1)]$ in $O(\log M)$ steps.
   - By Legendre's formula, the total exponent of 2 in $M!$ is:
     $$\sum_{m=1}^M v_2(m) = v_2(M!) = M - s(M)$$
     where $s(M)$ is the popcount (number of set 1-bits) in the binary representation of $M$.
   - Thus, $S(N) = \left(\sum_{m=1}^{N+1} \lfloor \log_2(m) \rfloor\right) - (N + 1 - s(N + 1))$, computable in $O(\log N)$ time.
"""

import unittest
from util.utils import timeit


class Problem704:
    def __init__(self, n: int = 10**16):
        self.n = n

    @timeit
    def solve(self) -> int:
        m_val = self.n + 1

        # Term 1: sum_{m=1}^{M} floor(log2(m))
        sum_log = 0
        k = 0
        while (1 << k) <= m_val:
            low = 1 << k
            high = min(m_val, (1 << (k + 1)) - 1)
            count = high - low + 1
            sum_log += k * count
            k += 1

        # Term 2: sum_{m=1}^{M} v_2(m) = M - popcount(M)
        sum_v2 = m_val - m_val.bit_count()

        return sum_log - sum_v2


class Solution704(unittest.TestCase):
    def setUp(self):
        self.problem = Problem704()

    def test_samples(self):
        self.assertEqual(389, Problem704(100).solve())
        self.assertEqual(203222840, Problem704(10**7).solve())

    def test_solution(self):
        self.assertEqual(501985601490518144, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
