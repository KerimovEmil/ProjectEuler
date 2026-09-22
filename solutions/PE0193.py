"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER: 684465067343069
Solve time: ~8.0 seconds
"""

import unittest
from bisect import bisect_right
import numpy as np
from util.utils import timeit, primes_upto


# MATHEMATICAL DERIVATION:
#
# 1. Square-free Counting via Inclusion-Exclusion (Möbius Inversion):
#    The count of square-free integers strictly below N is:
#      Q(N - 1) = sum_{k=1}^{floor(sqrt(N - 1))} mu(k) * floor((N - 1) / k^2)
#
# 2. Branch-and-Bound DFS with O(1) Binary Search Bulk Counting:
#    - For 1 prime: sum_{p <= sqrt(N-1)} floor((N - 1) / p^2) is computed directly via NumPy vectorization.
#    - For square-free products of >= 2 primes (p_1 < p_2 < ...), we traverse the tree of prime square products.
#    - Terminal Leaf Optimization: When floor((N - 1) / (prod * p^2)) == 1, no further prime can branch.
#      All primes in the interval (sqrt((N - 1)/(2 * prod)), sqrt((N - 1)/prod)] each contribute exactly
#      1 * sign to the total. We count this entire block in O(1) time using bisect_right, eliminating
#      millions of leaf function calls.


class Problem193:
    def __init__(self, n=2**50):
        self.n = n

    @timeit
    def solve(self):
        limit = self.n - 1
        sq_n = int(limit**0.5)

        primes = primes_upto(sq_n + 1)
        num_primes = len(primes)
        p_list = [int(p) for p in primes]
        p_sq_list = [int(p * p) for p in primes]

        # 1-prime terms via vectorized NumPy
        p_sq = primes.astype(np.int64)**2
        total = limit - int(np.sum(limit // p_sq))

        def dfs(idx, prod, sign):
            nonlocal total
            max_p2 = limit // prod
            if max_p2 < p_sq_list[idx]:
                return
            max_p = int(max_p2**0.5)
            max_idx = bisect_right(p_list, max_p, idx)

            max_p2_for_2 = limit // (2 * prod)
            if max_p2_for_2 >= p_sq_list[idx]:
                max_p_for_2 = int(max_p2_for_2**0.5)
                idx_for_2 = bisect_right(p_list, max_p_for_2, idx, max_idx)
            else:
                idx_for_2 = idx

            # Loop for terms where floor(limit / (prod * p^2)) >= 2 (may branch further)
            for i in range(idx, idx_for_2):
                p2 = p_sq_list[i]
                new_prod = prod * p2
                val = limit // new_prod
                total += val * sign
                if i + 1 < num_primes and p_sq_list[i + 1] <= limit // new_prod:
                    dfs(i + 1, new_prod, -sign)

            # O(1) bulk count for leaf terms where floor(limit / (prod * p^2)) == 1
            count_1 = max_idx - idx_for_2
            if count_1 > 0:
                total += count_1 * sign

        for i in range(num_primes):
            p1_sq = p_sq_list[i]
            if i + 1 < num_primes and p1_sq * p_sq_list[i + 1] > limit:
                break
            dfs(i + 1, p1_sq, 1)

        return total


class Solution193(unittest.TestCase):
    def setUp(self):
        self.problem = Problem193(n=int(2 ** 50))

    def test_solution(self):
        self.assertEqual(684465067343069, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
