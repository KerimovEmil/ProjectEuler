"""
PROBLEM

Find the number of integers 1 < n < 10^7, for which n and n + 1 have the same number of positive divisors.
For example, 14 has the positive divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15.

ANSWER: 986262
Solve time: ~0.21 seconds

---
MATHEMATICAL DERIVATION:

1. Divisor Pairing & Sqrt Divisor Counting:
   For any positive integer m, every divisor d < sqrt(m) corresponds to a unique complementary
   divisor (m / d) > sqrt(m).
   If m is a perfect square, d = sqrt(m) is a single divisor counted once.
   Therefore, the divisor counting function tau(m) can be expressed as:
       tau(m) = sum_{d | m, d <= sqrt(m)} (2 - [d^2 == m])

2. Direct Sqrt Vectorized Sieve:
   Instead of factorizing each number or sieving prime powers with multiple auxiliary arrays:
   - Initialize tau[m] = 2 for all m >= 2 (since every m >= 2 has at least two divisors: 1 and m),
     with tau[0] = 0 and tau[1] = 1.
   - For each integer d from 2 up to floor(sqrt(n)):
     - d is a divisor <= sqrt(m) for all multiples m = k * d with k >= d (i.e. m >= d^2).
     - For k > d, {d, k} provides two new divisors, so add 2 to tau[d^2 :: d].
     - For k = d (m = d^2), d = sqrt(m) is only one divisor, so subtract 1 from tau[d^2].
   - This requires iterating d only up to floor(sqrt(10^7)) = 3162, requiring only 3162 slice
     additions in NumPy.

3. Memory & Computational Complexity:
   - Memory: A single uint16 array of size N + 1 (20 MB for N = 10^7), avoiding auxiliary prime,
     factor, or boolean mask arrays.
   - Time: Sum_{d=2}^{sqrt(N)} (N / d) approx (1/2) N ln N operations, executing in ~0.21 seconds.
"""

import math
import unittest
import numpy as np
from util.utils import timeit


class Problem179:
    def __init__(self, n: int = 10**7):
        self.n = n

    @timeit
    def solve(self, n: int = None) -> int:
        if n is None:
            n = self.n

        limit_sqrt = math.isqrt(n)

        # Initialize: every m >= 2 has at least 2 divisors (1 and m)
        tau = np.full(n + 1, 2, dtype=np.uint16)
        tau[0] = 0
        tau[1] = 1

        # Sieve complementary divisor pairs {d, m / d} for d >= 2
        for d in range(2, limit_sqrt + 1):
            tau[d * d::d] += 2
            tau[d * d] -= 1

        return int(np.count_nonzero(tau[2:n] == tau[3:n + 1]))


class Solution179(unittest.TestCase):
    def setUp(self):
        self.problem = Problem179(n=int(1e7))

    def test_example(self):
        # 14 and 15 both have 4 divisors
        # For n = 15, valid pairs below 15: (2,3) both have 2, (14,15) both have 4
        self.assertEqual(2, self.problem.solve(n=15))

    def test_solution(self):
        self.assertEqual(986262, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
