"""
PROBLEM

Inside a rope of length n, n - 1 points are placed with distance 1 from each other and from the endpoints.
Among these points, we choose m - 1 points at random and cut the rope at these points to create m segments.

Let E(n, m) be the expected length of the second-shortest segment.
For example, E(3, 2) = 2 and E(8, 3) = 16/7.
Note that if multiple segments have the same shortest length the length of the second-shortest segment is defined as the same as the shortest length.

Find E(10^7, 100).
Give your answer rounded to 5 decimal places behind the decimal point.

ANSWER: 2010.59096
Solve time: ~0.08 seconds

---
MATHEMATICAL DERIVATION:

1. Tail Probability Formulation:
   Choosing m - 1 cut points out of n - 1 points is equivalent to choosing a composition of n into m positive
   integers X_1 + ... + X_m = n with X_i >= 1. The total number of compositions is comb(n - 1, m - 1).
   Let X_(1) <= X_(2) <= ... <= X_(m) be the sorted segment lengths.
   By the tail sum formula for expectation of non-negative integer random variables:
   E[X_(2)] = sum_{k=1}^inf P(X_(2) >= k).

2. Combinatorial Counting via Hockey-Stick Identity:
   The event X_(2) >= k occurs if and only if at most one segment has length < k:
   P(X_(2) >= k) = P(N_{< k} = 0) + P(N_{< k} = 1).

   - N_{< k} = 0: All m segments have length >= k.
     Setting Y_i = X_i - (k - 1) >= 1 gives sum Y_i = n - m(k - 1).
     Number of ways: comb(n - m(k - 1) - 1, m - 1).

   - N_{< k} = 1: Exactly one segment j has length L in [1, k - 1], while the remaining m - 1 segments
     have length >= k.
     For a fixed L, sum_{i != j} (X_i - (k - 1)) = (n - L) - (m - 1)(k - 1).
     Summing over L = 1, ..., k - 1 and multiplying by m choices for j:
     W_1 = m * sum_{L=1}^{k-1} comb(n - L - (m - 1)(k - 1) - 1, m - 2).
     By the hockey-stick identity sum_{t=A}^B comb(t, m - 2) = comb(B + 1, m - 1) - comb(A, m - 1), this telescopes:
     W_1 = m * [ comb(n - (m - 1)(k - 1) - 1, m - 1) - comb(n - m(k - 1) - 1, m - 1) ].

   Summing W_0 + W_1:
   W_0 + W_1 = m * comb(n - (m - 1)(k - 1) - 1, m - 1) - (m - 1) * comb(n - m(k - 1) - 1, m - 1).

3. Numerical Evaluation:
   Dividing by comb(n - 1, m - 1), we obtain:
   P(X_(2) >= k) = m * R(n - (m - 1)(k - 1) - 1) - (m - 1) * R(n - m(k - 1) - 1),
   where R(N) = comb(N, m - 1) / comb(n - 1, m - 1) = prod_{j=0}^{m-2} (1 - delta / (n - 1 - j))
   with delta = (n - 1) - N.
   Evaluating log(R(N)) via np.log1p(-delta / (n - 1 - j)) avoids catastrophic numerical underflow and
   cancellation, executing the vectorized summation in under 0.1 seconds.
"""

import math
import unittest
import numpy as np
from util.utils import timeit


class Problem398:
    def __init__(self):
        pass

    def expected_second_shortest(self, n: int, m: int) -> float:
        if m == 1:
            return float(n)

        def compute_s(step: int) -> float:
            k_max = (n - m) // step + 1
            # We can vectorize over k
            k = np.arange(1, k_max + 1, dtype=np.float64)
            delta = step * (k - 1.0)
            j = np.arange(m - 1, dtype=np.float64)
            denom = (n - 1.0) - j

            ratio = delta[:, None] / denom[None, :]
            valid = (ratio < 1.0)
            ratio_clipped = np.where(valid, ratio, 0.0)
            log_terms = np.where(valid, np.log1p(-ratio_clipped), -np.inf)
            log_ratio = np.sum(log_terms, axis=1)

            # Filter terms that underflow float precision
            mask = log_ratio > -60.0
            return float(np.sum(np.exp(log_ratio[mask])))

        s1 = compute_s(m - 1)
        s2 = compute_s(m)
        return m * s1 - (m - 1) * s2

    @timeit
    def solve(self) -> str:
        ans = self.expected_second_shortest(10**7, 100)
        return f"{ans:.5f}"


class Solution398(unittest.TestCase):
    def setUp(self):
        self.problem = Problem398()

    def test_sample(self):
        self.assertAlmostEqual(2.0, self.problem.expected_second_shortest(3, 2), places=5)
        self.assertAlmostEqual(16.0 / 7.0, self.problem.expected_second_shortest(8, 3), places=5)

    def test_solution(self):
        self.assertEqual("2010.59096", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
