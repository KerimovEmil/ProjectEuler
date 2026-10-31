"""
PROBLEM

Consider the numbers 15, 16 and 18:
  15 = 3 * 5 and 3 + 5 = 8.
  16 = 2 * 2 * 2 * 2 and 2 + 2 + 2 + 2 = 8.
  18 = 2 * 3 * 3 and 2 + 3 + 3 = 8.

15, 16 and 18 are the only numbers that have 8 as sum of the prime factors (counted with multiplicity).

We define S(k) to be the sum of all numbers n where the sum of the prime factors (with multiplicity)
of n is k.

Hence S(8) = 15 + 16 + 18 = 49.

Other examples: S(1) = 0, S(2) = 2, S(3) = 3, S(5) = 5 + 6 = 11.

The Fibonacci sequence is F_1 = 1, F_2 = 1, F_3 = 2, F_4 = 3, F_5 = 5, ....

Find the last nine digits of sum_{k=2}^{24} S(F_k).

ANSWER: 634212216
Solve time: ~60 seconds

---
MATHEMATICAL DERIVATION:

1. Generating Function:
   Every integer n >= 2 has a unique prime factorization n = prod p_i^(a_i).
   The sum of prime factors counted with multiplicity is sum a_i * p_i = k.
   The sum S(k) of all such integers n is the coefficient of x^k in the Euler product:
     G(x) = prod_{p prime} (1 + p*x^p + p^2*x^(2p) + p^3*x^(3p) + ...)
          = prod_{p prime} 1 / (1 - p*x^p).

2. Unbounded Knapsack DP:
   Expanding the product factor by factor for each prime p <= F_24:
   Let dp[i] be the coefficient of x^i in the partial product up to prime p.
   For each prime p, the transition for i from p to F_24 is:
     dp[i] = (dp[i] + p * dp[i - p]) mod 10^9,
   with base case dp[0] = 1 and dp[i] = 0 for i > 0.

3. Target Evaluation:
   The maximum Fibonacci index required is F_24 = 46368.
   Sieving all primes up to 46368 and performing the DP modulo 10^9 gives S(k) = dp[k].
   We then sum dp[F_k] for k = 2, ..., 24 modulo 10^9.
"""

from typing import List
import unittest
from util.utils import timeit

MOD = 10**9


class Problem618:
    def __init__(self, max_fib_index: int = 24):
        self.max_fib_index = max_fib_index

    @staticmethod
    def get_fibonacci(n: int) -> List[int]:
        fib = [0, 1]
        for _ in range(2, n + 1):
            fib.append(fib[-1] + fib[-2])
        return fib

    @staticmethod
    def sieve_primes(limit: int) -> List[int]:
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False
        return [i for i, prime in enumerate(is_prime) if prime]

    def compute_S(self, max_k: int) -> List[int]:
        primes = self.sieve_primes(max_k)
        dp = [0] * (max_k + 1)
        dp[0] = 1

        for p in primes:
            for i in range(p, max_k + 1):
                dp[i] = (dp[i] + p * dp[i - p]) % MOD

        return dp

    @timeit
    def solve(self) -> int:
        fib = self.get_fibonacci(self.max_fib_index)
        max_k = fib[self.max_fib_index]
        dp = self.compute_S(max_k)
        return sum(dp[fib[k]] for k in range(2, self.max_fib_index + 1)) % MOD


class Solution618(unittest.TestCase):
    def setUp(self):
        self.problem = Problem618()

    def test_sample(self):
        dp = self.problem.compute_S(8)
        self.assertEqual(0, dp[1])
        self.assertEqual(2, dp[2])
        self.assertEqual(3, dp[3])
        self.assertEqual(11, dp[5])
        self.assertEqual(49, dp[8])

    def test_solution(self):
        self.assertEqual(634212216, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
