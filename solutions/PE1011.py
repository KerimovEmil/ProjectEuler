r"""
PROBLEM

In a modified Euclidean algorithm for two numbers $a, b$, at each step we perform Euclidean division of the larger number by the smaller number and then replace the larger number with the integer quotient (rather than the remainder, as in the normal Euclidean algorithm).

This operation is repeatedly performed until one of the two numbers becomes $1$; when this happens, the value of the other number is denoted $f(a, b)$.

For example, $f(123, 456) = 3$ as shown below:
$$(123, 456) \to (123, 3) \to (41, 3) \to (13, 3) \to (4, 3) \to (1, 3) \mapsto 3.$$

Let $E(N)$ be the sum $\sum\limits_{1 \le a, b \lt N} f(a, b)$.

You are given $E(10) = 343$ and $E(100) = 269288$.

Find $E(3\,000\,000)$.

ANSWER: 6750031298491815420
Solve time: ~1.54 seconds

---
MATHEMATICAL DERIVATION:

1. Symmetry and Quotient Partitioning:
   - By symmetry, $f(a, b) = f(b, a)$ and $f(a, a) = a$. Thus:
     $$E(N) = \sum_{a=1}^{N-1} a + 2 \sum_{1 \le a < b < N} f(a, b) = \frac{(N-1)N}{2} + 2 S(N)$$
   - For a fixed $a$ and $b > a$, let $q = \lfloor b/a \rfloor \ge 1$. Then $(a, b) \to (a, q)$, so $f(a, b) = f(a, q)$.
   - For each quotient $q \in [1, \lfloor (N-1)/a \rfloor]$, $b$ ranges in $[\max(a+1, q a), \min(N-1, (q+1)a - 1)]$.
   - For $q = 1$: $f(a, 1) = a$. The count of such $b$'s is:
     $$c(a, 1) = \begin{cases} a - 1 & \text{if } a \le \lfloor N/2 \rfloor \\ N - 1 - a & \text{if } a > \lfloor N/2 \rfloor \end{cases}$$
     The sum $\sum_{a=1}^{N-1} a \cdot c(a, 1)$ evaluates in $O(1)$ using quadratic/linear power sums.
   - For $a = 1, q \ge 2$: $c(1, q) = 1$ and $f(1, q) = q$, contributing $\sum_{q=2}^{N-1} q = \frac{(N-1)N}{2} - 1$.

2. Hyperbolic Interval Aggregation & Recurrence:
   - For $a \ge 2, q \ge 2$ with $a \cdot q < N$, we have $\min(a, q) \le \sqrt{N-1}$.
   - For a fixed parameter $d = \min(a, q) \le \sqrt{N-1}$:
     - When $a < q$: $q$ ranges in $[d+1, \lfloor (N-1)/d \rfloor]$. Setting $k = \lfloor q/d \rfloor$, $f(d, q) = f(d, k)$
       remains constant on intervals of $q \in [k \cdot d, \min((N-1)/d, (k+1)d - 1)]$.
     - When $a > q$: $a$ ranges in $[d+1, \lfloor (N-1)/d \rfloor]$. Setting $k = \lfloor a/d \rfloor$, $f(a, d) = f(d, k)$
       remains constant on intervals of $a \in [k \cdot d, \min((N-1)/d, (k+1)d - 1)]$.
   - On each interval, the sum of coefficients $c(a, q)$ is an arithmetic progression computed in $O(1)$ time.
   - The total number of intervals across all $d \le \sqrt{N}$ is $2 \sum_{d=2}^{\sqrt{N}} \frac{N}{d^2} \approx 2 N (\pi^2/6 - 1) \approx 1.29 N$.

3. Precomputed Recurrence Table:
   - $f(x, y)$ for $x \le \sqrt{N}$ and $y \le (N-1)/x^2$ is precomputed in $O(N)$ total time via memoized DAG traversal:
     $$f(x, y) = f(\min(x, \lfloor y/x \rfloor), \max(x, \lfloor y/x \rfloor))$$

4. Complexity Analysis:
   - Time Complexity: $O(N)$ operations ($\approx 3.8 \times 10^6$ intervals for $N = 3 \times 10^6$), running in ~1.5 seconds.
   - Space Complexity: $O(\sum_{d=2}^{\sqrt{N}} N/d^2) = O(N)$ integers (~1.93 million entries, < 16 MB).
"""

import unittest
from util.utils import timeit


class Problem1011:
    def __init__(self, n: int = 3_000_000):
        self.n = n

    @timeit
    def solve(self) -> int:
        n = self.n
        if n <= 1:
            return 0

        half = n // 2
        limit_sqrt = int((n - 1) ** 0.5)

        # Precompute table for f(x, k) where x <= limit_sqrt and k <= (n - 1) // (x * x)
        f_table: list[list[int] | None] = [None] * (limit_sqrt + 1)
        for x in range(2, limit_sqrt + 1):
            max_k = (n - 1) // (x * x)
            f_table[x] = [0] * (max_k + 1)

        def compute_f(x: int, y: int) -> int:
            if x == 1:
                return y
            if x == y:
                return x
            k = y // x
            if k == 1:
                return x
            if k <= x:
                tbl_k = f_table[k]
                if k <= limit_sqrt and tbl_k is not None and x < len(tbl_k) and tbl_k[x] != 0:
                    return tbl_k[x]
                return compute_f(k, x)
            else:
                tbl_x = f_table[x]
                if x <= limit_sqrt and tbl_x is not None and k < len(tbl_x) and tbl_x[k] != 0:
                    return tbl_x[k]
                return compute_f(x, k)

        for x in range(2, limit_sqrt + 1):
            tbl = f_table[x]
            assert tbl is not None
            max_k = len(tbl) - 1
            for k in range(2, max_k + 1):
                if k <= x:
                    q = x // k
                    if q == 1:
                        tbl[k] = k
                    elif q <= k:
                        tbl[k] = compute_f(q, k)
                    else:
                        tbl[k] = compute_f(k, q)
                else:
                    q = k // x
                    if q == 1:
                        tbl[k] = x
                    elif q <= x:
                        tbl[k] = tbl[q] if q < len(tbl) and tbl[q] else compute_f(q, x)
                    else:
                        tbl[k] = tbl[q] if q < len(tbl) and tbl[q] else compute_f(x, q)

        # Closed form for q = 1 cases: sum_{a=1}^{n-1} a * count(a, 1)
        sum_part1 = (half - 1) * half * (half + 1) // 3
        sum_linear = lambda m: m * (m + 1) // 2
        sum_squares = lambda m: m * (m + 1) * (2 * m + 1) // 6
        sum_a = sum_linear(n - 1) - sum_linear(half)
        sum_a2 = sum_squares(n - 1) - sum_squares(half)
        sum_part2 = (n - 1) * sum_a - sum_a2
        sum_q1 = sum_part1 + sum_part2

        # a = 1, q in [2, n - 1]: f(1, q) = q
        sum_a1 = (n - 1) * n // 2 - 1

        sum_pairs = 0
        for d in range(2, limit_sqrt + 1):
            # 1. d == q (diagonal of product region)
            c_diag = d if (d + 1) * d <= n else n - d * d
            sum_pairs += c_diag * d

            max_other = (n - 1) // d
            if max_other <= d:
                continue

            tbl = f_table[d]
            assert tbl is not None
            max_k = (n - 1) // (d * d)
            m_cutoff = n // (d + 1)

            # k = 1 interval: d + 1 <= other <= min(max_other, 2d - 1)
            other_end_k1 = min(max_other, 2 * d - 1)
            if d + 1 <= other_end_k1:
                if other_end_k1 < max_other:
                    c_sum_less = (other_end_k1 - d) * d
                else:
                    c_sum_less = (max_other - d - 1) * d + (n - max_other * d)

                low, high = d + 1, other_end_k1
                if high <= m_cutoff:
                    c_sum_greater = (low + high) * (high - low + 1) // 2
                elif low > m_cutoff:
                    cnt = high - low + 1
                    c_sum_greater = n * cnt - d * ((low + high) * cnt // 2)
                else:
                    cnt1 = m_cutoff - low + 1
                    cnt2 = high - m_cutoff
                    c_sum_greater = (
                        (low + m_cutoff) * cnt1 // 2
                        + n * cnt2
                        - d * ((m_cutoff + 1 + high) * cnt2 // 2)
                    )

                sum_pairs += (c_sum_less + c_sum_greater) * d

            # Intervals for k in [2, max_k]:
            for k in range(2, max_k + 1):
                start = k * d
                end = min(max_other, (k + 1) * d - 1)
                if start > end:
                    continue

                if end < max_other:
                    c_sum_less = (end - start + 1) * d
                else:
                    c_sum_less = (max_other - start) * d + (n - max_other * d)

                if end <= m_cutoff:
                    c_sum_greater = (start + end) * (end - start + 1) // 2
                elif start > m_cutoff:
                    cnt = end - start + 1
                    c_sum_greater = n * cnt - d * ((start + end) * cnt // 2)
                else:
                    cnt1 = m_cutoff - start + 1
                    cnt2 = end - m_cutoff
                    c_sum_greater = (
                        (start + m_cutoff) * cnt1 // 2
                        + n * cnt2
                        - d * ((m_cutoff + 1 + end) * cnt2 // 2)
                    )

                sum_pairs += (c_sum_less + c_sum_greater) * tbl[k]

        total_off_diag = sum_q1 + sum_a1 + sum_pairs
        diag = (n - 1) * n // 2
        return diag + 2 * total_off_diag


class Solution1011(unittest.TestCase):
    def setUp(self):
        self.problem = Problem1011()

    def test_samples(self):
        self.assertEqual(343, Problem1011(10).solve())
        self.assertEqual(269288, Problem1011(100).solve())

    def test_solution(self):
        self.assertEqual(6750031298491815420, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
