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
Solve time: ~0.85 seconds

---
MATHEMATICAL DERIVATION:

1. Symmetry and Quotient Partitioning:
   - By symmetry, $f(a, b) = f(b, a)$ and $f(a, a) = a$. Thus:
     $$E(N) = \sum_{a=1}^{N-1} a + 2 \sum_{1 \le a < b < N} f(a, b) = \frac{(N-1)N}{2} + 2 S(N)$$
   - For a fixed $a$ and $b > a$, let $q = \lfloor b/a \rfloor \ge 1$. Then $(a, b) \to (a, q)$, so $f(a, b) = f(a, q)$.
   - For each quotient $q \in [1, \lfloor (N-1)/a \rfloor]$, $b$ ranges in $[\max(a+1, q a), \min(N-1, (q+1)a - 1)]$.
   - For $q = 1$: $f(a, 1) = a$. Evaluated in $O(1)$ via closed-form quadratic and linear sum identities.
   - For $a = 1, q \ge 2$: $c(1, q) = 1$ and $f(1, q) = q$, contributing $\sum_{q=2}^{N-1} q = \frac{(N-1)N}{2} - 1$.

2. Constant Invariant $f(2, b) = 2$ and $O(1)$ Closed Forms for $d = 2$:
   - For any $b \ge 2$, $(2, b) \to (2, \lfloor b/2 \rfloor) \to \dots \to (2, 2 \text{ or } 3) \to (2, 1) \mapsto 2$.
     Thus, $f(2, b) = 2$ identically for all $b \ge 2$.
   - The divisor $d = 2$ accounts for $N/4 = 750,000$ intervals ($\approx 38.8\%$ of all intervals across all $d$).
   - We replace all $d = 2$ computations with exact $O(1)$ closed forms:
     1. $a = 2, b \ge 4$: $\sum_{b=4}^{N-1} f(2, b) = 2(N - 4)$.
     2. $q = 2, a \ge 3$: $\sum_{a=3}^{\lfloor (N-1)/2 \rfloor} c(a, 2) \cdot 2 = 2 \left( \sum_{a=3}^{\lfloor N/3 \rfloor} a + \sum_{a=\lfloor N/3 \rfloor + 1}^{\lfloor (N-1)/2 \rfloor} (N - 2a) \right)$.

3. Hyperbolic Interval Aggregation for $d \ge 3$:
   - For $a \ge 3, q \ge 3$ with $a \cdot q < N$, let $d = \min(a, q) \le \sqrt{N-1}$.
   - Setting $k = \lfloor \max(a, q) / d \rfloor$, $f(a, q) = f(d, k)$ is constant over contiguous intervals of length $d$.
   - The coefficient sum over each interval is an arithmetic progression evaluated in $O(1)$ time.
   - Values of $f(d, k)$ for $3 \le d \le \sqrt{N}$ and $k \le (N-1)/d^2$ are precomputed in $O(N)$ via memoized DAG traversal over integer array buffers.
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

        # Precompute table for f(x, k) for 3 <= x <= limit_sqrt and k <= (n - 1) // (x * x)
        # We leverage f(2, b) = 2 identically for all b >= 2
        f_table: list[list[int] | None] = [None] * (limit_sqrt + 1)
        for x in range(3, limit_sqrt + 1):
            max_k = (n - 1) // (x * x)
            f_table[x] = [0] * (max_k + 1)

        def compute_f(x: int, y: int) -> int:
            if x == 1:
                return y
            if x == 2:
                return 2
            if x == y:
                return x
            k = y // x
            if k == 1:
                return x
            if k == 2:
                return 2
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

        for x in range(3, limit_sqrt + 1):
            tbl = f_table[x]
            assert tbl is not None
            max_k = len(tbl) - 1
            for k in range(2, max_k + 1):
                if k == 2:
                    tbl[k] = 2
                elif k <= x:
                    q = x // k
                    if q == 1:
                        tbl[k] = k
                    elif q == 2:
                        tbl[k] = 2
                    elif q <= k:
                        tbl[k] = compute_f(q, k)
                    else:
                        tbl[k] = compute_f(k, q)
                else:
                    q = k // x
                    if q == 1:
                        tbl[k] = x
                    elif q == 2:
                        tbl[k] = 2
                    elif q <= x:
                        tbl[k] = tbl[q] if q < len(tbl) and tbl[q] else compute_f(q, x)
                    else:
                        tbl[k] = tbl[q] if q < len(tbl) and tbl[q] else compute_f(x, q)

        # 1. Closed form for q = 1 cases: sum_{a=1}^{n-1} a * count(a, 1)
        sum_linear = lambda m: m * (m + 1) // 2
        sum_squares = lambda m: m * (m + 1) * (2 * m + 1) // 6

        sum_part1 = (half - 1) * half * (half + 1) // 3
        sum_a = sum_linear(n - 1) - sum_linear(half)
        sum_a2 = sum_squares(n - 1) - sum_squares(half)
        sum_part2 = (n - 1) * sum_a - sum_a2
        sum_q1 = sum_part1 + sum_part2

        # 2. a = 1, q in [2, n - 1]: f(1, q) = q
        sum_a1 = (n - 1) * n // 2 - 1

        # 3. Exact O(1) closed forms for d = 2 leveraging f(2, b) = 2 for all b >= 2:
        # (a) a = 2, b in [4, n - 1]:
        sum_a2_ge_4 = 2 * max(0, n - 4)

        # (b) q = 2, a in [3, (n - 1) // 2]:
        third = n // 3
        if third >= 3:
            sum_count_a = sum_linear(third) - sum_linear(2)
        else:
            sum_count_a = 0

        if half >= third + 1:
            cnt_terms = half - (third + 1) + 1
            sum_a_tail = sum_linear(half) - sum_linear(third)
            sum_count_b = n * cnt_terms - 2 * sum_a_tail
        else:
            sum_count_b = 0

        sum_q2_a_ge_3 = 2 * (sum_count_a + sum_count_b)

        sum_pairs = sum_a2_ge_4 + sum_q2_a_ge_3

        # 4. Hyperbolic intervals for d >= 3:
        for d in range(3, limit_sqrt + 1):
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
