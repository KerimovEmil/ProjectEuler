"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER: 684465067343069
Solve time: ~8.0 seconds

References:
  https://arxiv.org/pdf/1107.4890.pdf
  http://www.numericana.com/answer/numbers.htm#moebius
"""
import unittest
from bisect import bisect_right
import numpy as np
from util.utils import timeit, mobius_sieve, primes_upto


class Problem193:
    def __init__(self, n=2**50):
        self.n = n
        self.ls_primes = None
        self.limit = None
        self.total = None
        self.ls_sq_primes = None
        self.num_primes = None

    @timeit
    def solve_mobius(self, debug=False):  # 49 seconds
        self.ls_primes = primes_upto((self.n ** 0.5) + 1)
        if debug:
            print("finished calculating primes")
        limit = self.n - 1
        sq_root_n = int(self.n ** 0.5) + 1
        ls_m = mobius_sieve(n=sq_root_n, ls_prime=self.ls_primes)
        if debug:
            print("finished calculating mobius values")
        return sum(ls_m[i] * (limit // (i ** 2)) for i in range(1, sq_root_n))

    @timeit
    def solve_count_p_square(self, debug=False):  # 30 seconds
        self.ls_primes = primes_upto((self.n ** 0.5) + 1)
        self.ls_sq_primes = [p * p for p in self.ls_primes]
        len_primes = len(self.ls_primes)
        if debug:
            print("finished calculating primes")
        ls = [(i, p2) for i, p2 in enumerate(self.ls_sq_primes)]
        total = self.n - 1
        limit = self.n - 1
        sig = 1
        while ls:
            sig *= -1
            new_ls = []
            for i, q in ls:
                total += (limit // q) * sig
                for j in range(i + 1, len_primes):
                    pq = self.ls_sq_primes[j] * q
                    if pq > self.n:
                        break
                    new_ls.append((j, pq))
            ls = new_ls
        return total

    @timeit
    def solve_inclusion_exclusion(self):  # ~8.0 seconds
        self.limit = self.n - 1
        self.ls_primes = primes_upto(int(self.limit ** 0.5) + 1)
        self.num_primes = len(self.ls_primes)
        p_list = [int(p) for p in self.ls_primes]
        self.ls_sq_primes = [int(p * p) for p in self.ls_primes]
        p_sq_list = self.ls_sq_primes
        limit = self.limit

        # 1-prime terms via vectorized NumPy
        p_sq = self.ls_primes.astype(np.int64) ** 2
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
                if i + 1 < self.num_primes and p_sq_list[i + 1] <= limit // new_prod:
                    dfs(i + 1, new_prod, -sign)

            # O(1) bulk count for leaf terms where floor(limit / (prod * p^2)) == 1
            count_1 = max_idx - idx_for_2
            if count_1 > 0:
                total += count_1 * sign

        for i in range(self.num_primes):
            p1_sq = p_sq_list[i]
            if i + 1 < self.num_primes and p1_sq * p_sq_list[i + 1] > limit:
                break
            dfs(i + 1, p1_sq, 1)

        self.total = total
        return self.total

    def solve(self):
        return self.solve_inclusion_exclusion()


class Solution193(unittest.TestCase):
    def setUp(self):
        self.problem = Problem193(n=int(2 ** 50))

    def test_solution(self):
        # self.assertEqual(684465067343069, self.problem.solve_mobius())
        # self.assertEqual(684465067343069, self.problem.solve_count_p_square())
        self.assertEqual(684465067343069, self.problem.solve_inclusion_exclusion())


if __name__ == '__main__':
    unittest.main()
