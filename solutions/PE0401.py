"""
PROBLEM

The divisors of 6 are 1,2,3 and 6.
The sum of the squares of these numbers is 1+4+9+36=50.

Let sigma2(n) represent the sum of the squares of the divisors of n. Thus sigma2(6)=50.

Let SIGMA2 represent the summatory function of sigma2, that is SIGMA2(n)=sum_{i=1}^n sigma2(i).
The first 6 values of SIGMA2 are: 1,6,16,37,63 and 113.
Find SIGMA2(10^15) modulo 10^9.

ANSWER: 281632621
Solve time: ~5 seconds

MATHEMATICAL DERIVATION:
1. The sum of divisor squares over all integers up to N can be rewritten by swapping summation order:
   SIGMA2(N) = sum_{k=1}^N sigma_2(k) = sum_{d=1}^N d^2 * floor(N / d).

2. We use the standard hyperbolic / square-root block division at D = floor(sqrt(N)):
   - For d <= D: Each d appears floor(N / d) times.
     Contribution: sum_{d=1}^D d^2 * floor(N / d) (mod 10^9).
   - For d > D: The quotient q = floor(N / d) satisfies 1 <= q <= floor(N / (D + 1)).
     The range of divisors d that produce quotient q is:
       low = max(D, floor(N / (q + 1)))
       high = floor(N / q)
     The contribution for this quotient is q * sum_{d=low+1}^{high} d^2.

3. The sum of squares S(x) = sum_{k=1}^x k^2 = x * (x + 1) * (2x + 1) / 6.
   To compute S(x) mod 10^9 without 64-bit overflow during intermediate multiplication,
   we observe that among {x, x+1, 2x+1}, exactly one is divisible by 2 and one by 3.
   We divide out 2 and 3 before performing modular multiplication mod 10^9.

4. Using chunked NumPy vectorization over the sqrt(N) ~ 3.16 x 10^7 elements,
   the calculation executes in ~5 seconds.
"""

import unittest
import numpy as np
from util.utils import timeit


def sum_sq_mod(x, mod):
    """Computes x*(x+1)*(2x+1)//6 mod `mod` for a NumPy array of int64 without overflow."""
    rem6 = x % 6
    a = np.where(rem6 == 0, x // 6, np.where((rem6 == 2) | (rem6 == 4), x // 2, np.where(rem6 == 3, x // 3, x))) % mod
    b = np.where(rem6 == 5, (x + 1) // 6, np.where((rem6 == 1) | (rem6 == 3), (x + 1) // 2, np.where(rem6 == 2, (x + 1) // 3, x + 1))) % mod
    c = np.where((rem6 == 1) | (rem6 == 4), (2 * x + 1) // 3, 2 * x + 1) % mod
    return ((a * b % mod) * c) % mod


class Problem401:
    def __init__(self, max_int=int(1e15), mod=int(1e9)):
        self.max_int = max_int
        self.mod = mod

    @timeit
    def solve(self):
        n = self.max_int
        mod = self.mod
        sqr_n = int(n ** 0.5)

        chunk_size = 5000000
        ans = 0

        for start in range(1, sqr_n + 1, chunk_size):
            end = min(sqr_n + 1, start + chunk_size)
            i = np.arange(start, end, dtype=np.int64)

            # Part 1: d <= sqrt(n)
            q = n // i
            i_mod = i % mod
            term1 = ((i_mod * i_mod % mod) * (q % mod)) % mod

            # Part 2: quotients q = i corresponding to d > sqrt(n)
            high = q
            low = np.maximum(sqr_n, n // (i + 1))
            valid = high > low

            sh = sum_sq_mod(high, mod)
            sl = sum_sq_mod(low, mod)
            diff = np.where(valid, (sh - sl) % mod, 0)
            term2 = (i_mod * diff) % mod

            ans = (ans + int(np.sum(term1)) + int(np.sum(term2))) % mod

        return ans


class Solution401(unittest.TestCase):
    def setUp(self):
        self.problem = Problem401(max_int=int(1e15), mod=int(1e9))

    def test_solution(self):
        self.assertEqual(281632621, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
