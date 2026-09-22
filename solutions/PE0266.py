"""
PROBLEM

The divisors of 12 are: 1,2,3,4,6 and 12.
The largest divisor of 12 that does not exceed the square root of 12 is 3.
We shall call the largest divisor of an integer n that does not exceed the square root of n the pseudo square
root (PSR) of n.
It can be seen that PSR(3102)=47.

Let p be the product of the primes below 190.
Find PSR(p) mod 10^16.

ANSWER: 1096883702440585
Solve time: ~4.4 seconds

Example:
  prime_prod = 2*3*5*7*11 = 2310
  sqrt(2310) = 48.06... < 49
  48 < sqrt(2310) < 49
  divisors of 2310: 1 | 2 | 3 | 5 | 6 | 7 | 10 | 11 | 14 | 15 | 21 | 22 | 30 | 33 | 35 | 42
  | 55 | 66 | 70 | 77 | 105 | 110 | 154 | 165 | 210 | 231 | 330 | 385 | 462 | 770 | 1155 | 2310 (32 divisors)
  therefore the PSR(2310) = 42 = 2*3*7

MATHEMATICAL DERIVATION:
1. Logarithmic Subset Sum (Knapsack):
   Let P = prod_{i=1}^{m} p_i be the product of all primes below 190 (m = 42 primes).
   Every divisor d of P is square-free and formed by a subset S subseteq {1, ..., m}:
     d = prod_{i in S} p_i
   We want to maximize d <= sqrt(P), which is equivalent to maximizing:
     sum_{i in S} ln(p_i) <= 1/2 * sum_{i=1}^{m} ln(p_i).

2. Meet-in-the-Middle with Two-Pointer Linear Scan:
   With m = 42 primes, iterating over all 2^42 subsets is infeasible.
   We split the primes into two halves of 21 primes each:
   - Left half (21 primes): generate all 2^21 ~ 2.1 * 10^6 subsets (log_sum, product) and sort ascending by log_sum.
   - Right half (21 primes): generate all 2^21 subsets and sort descending by log_sum.
   - Use a linear two-pointer scan over the sorted lists to find the pair (L, R) maximizing
     (L.log_sum + R.log_sum) <= target_log in O(2^21) time.

3. Final Result:
   Compute (L.product * R.product) mod 10^16. Total runtime is ~4.4s.
"""

import math
import unittest
from util.utils import timeit, primes_upto


class Problem266:
    def __init__(self, prime_max: int = 190, digits: int = 16, debug: bool = False):
        self.prime_max = prime_max
        self.digits = digits
        self.debug = debug
        self.ls_primes = [int(p) for p in primes_upto(self.prime_max)]
        self.num_total_primes = len(self.ls_primes)

    @timeit
    def solve(self) -> int:  # noqa: C901
        primes = self.ls_primes
        target_log = sum(math.log(p) for p in primes) / 2.0
        mid = len(primes) // 2

        left_primes = primes[:mid]
        right_primes = primes[mid:]

        # 1. Generate left half
        left_subsets = [(0.0, 1)]
        for p in left_primes:
            lp = math.log(p)
            new_subsets = []
            for l_sum, l_prod in left_subsets:
                if l_sum + lp <= target_log:
                    new_subsets.append((l_sum + lp, l_prod * p))
            left_subsets.extend(new_subsets)
        left_subsets.sort(key=lambda x: x[0])

        # 2. Generate right half
        right_subsets = [(0.0, 1)]
        for p in right_primes:
            lp = math.log(p)
            new_subsets = []
            for r_sum, r_prod in right_subsets:
                if r_sum + lp <= target_log:
                    new_subsets.append((r_sum + lp, r_prod * p))
            right_subsets.extend(new_subsets)
        right_subsets.sort(key=lambda x: x[0], reverse=True)

        # 3. Two-pointer scan
        best_log = 0.0
        best_prod = 1
        l_idx = 0
        n_left = len(left_subsets)

        for r_sum, r_prod in right_subsets:
            while l_idx < n_left and r_sum + left_subsets[l_idx][0] <= target_log:
                l_idx += 1
            if l_idx > 0:
                total_l = r_sum + left_subsets[l_idx - 1][0]
                if total_l > best_log:
                    best_log = total_l
                    best_prod = r_prod * left_subsets[l_idx - 1][1]

        return best_prod % (10 ** self.digits)


class Solution266(unittest.TestCase):
    def setUp(self):
        self.problem = Problem266()

    def test_example(self):
        # PSR of 2310 = 2 * 3 * 5 * 7 * 11 is 42
        self.assertEqual(42, Problem266(prime_max=12, digits=16).solve())

    def test_solution(self):
        self.assertEqual(1096883702440585, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
