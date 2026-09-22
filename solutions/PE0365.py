"""
PROBLEM

The binomial coefficient (10^18 choose 10^9) is a number with more than 9 billion digits.

Let M(n,k,m) denote the binomial coefficient (n choose k) mod m.

Calculate sum of M(10^18, 10^9, p*q*r) for 1000 < p < q < r < 5000 and p, q, r prime.

ANSWER: 162619462356610313
Solve time: ~1.5 seconds

MATHEMATICAL DERIVATION:
1. By Lucas' Theorem, for a prime p,
   (n choose k) = prod (n_i choose k_i) (mod p)
   where n = sum n_i * p^i and k = sum k_i * p^i are base-p expansions.
   Since there are only 559 primes in (1000, 5000), we precompute V[p] = (10^18 choose 10^9) mod p
   for all 559 primes in ~0.05 seconds.

2. For any triplet of primes (p, q, r) with p < q < r, we wish to find X in [0, p*q*r - 1]
   satisfying:
     X = V[p] (mod p)
     X = V[q] (mod q)
     X = V[r] (mod r)

3. Using Garner's Mixed-Radix Algorithm:
   - Let y = V[p] + p * [ (V[q] - V[p]) * inv(p, q) mod q ], so 0 <= y < p*q and y = V[p] (mod p), y = V[q] (mod q).
   - Then X = y + p*q * [ (V[r] - (y mod r)) * inv(p*q, r) mod r ].
   - Since 0 <= y < p*q and the second term is < p*q*r, X is already in [0, p*q*r - 1] without full modular reduction.

4. Vectorization:
   - For all 559 primes, we precompute the modular inverse table I[i, j] = inv(p_j, p_i).
   - We precompute the 2D arrays Y[i, j] and PQ[i, j] for all pairs i < j.
   - For each prime r = primes[k] (k from 2 to 558), we evaluate the CRT sum over all pairs (i, j) with i < j < k
     using 2D vectorized NumPy matrix arithmetic:
       inv_mat = (I[k, :k, None] * I[k, None, :k]) % r
       diff = (V[k] - Y[:k, :k]) % r
       x3 = (diff * inv_mat) % r
       term = Y[:k, :k] + PQ[:k, :k] * x3
     and sum the strictly upper-triangular elements.
   This completes the ~2.9 x 10^7 CRT combinations in ~1.5 seconds.
"""

import unittest
import numpy as np
from util.utils import timeit, primes_upto, get_combination_mod_p, number_base_rep


class Problem365:
    def __init__(self, n=pow(10, 18), k=pow(10, 9), min_prime=1000, max_prime=5000):
        self.n = n
        self.k = k
        self.min_prime = min_prime
        self.max_prime = max_prime

        all_p = primes_upto(max_prime)
        self.primes = [p for p in all_p if p > min_prime]

    @timeit
    def solve(self):
        primes_list = [int(p) for p in self.primes]
        n_primes = len(primes_list)
        if n_primes < 3:
            return 0

        # Step 1: Precompute (n choose k) mod p for all primes
        v_list = [get_combination_mod_p(self.n, self.k, p) for p in primes_list]

        # Step 2: Precompute inverse matrix I[i, j] = inv(primes_list[j]) mod primes_list[i]
        inv_table = np.zeros((n_primes, n_primes), dtype=np.int64)
        for i, pi in enumerate(primes_list):
            exp = pi - 2
            inv_table[i, :] = [pow(pj, exp, pi) if pi != pj else 0 for pj in primes_list]

        # Step 3: Precompute Y[i, j] and PQ[i, j] for all i < j
        y_mat = np.zeros((n_primes, n_primes), dtype=np.int64)
        pq_mat = np.zeros((n_primes, n_primes), dtype=np.int64)
        for i in range(n_primes):
            p = primes_list[i]
            vp = v_list[i]
            for j in range(i + 1, n_primes):
                q = primes_list[j]
                vq = v_list[j]
                x2 = ((vq - vp) * inv_table[j, i]) % q
                y_mat[i, j] = vp + p * x2
                pq_mat[i, j] = p * q

        # Step 4: Vectorized summation over all triplets (i < j < k)
        total_sum = 0
        for k in range(2, n_primes):
            r = primes_list[k]
            vr = v_list[k]
            ik = inv_table[k, :k]
            inv_mat = (ik[:, None] * ik[None, :]) % r

            y_sub = y_mat[:k, :k]
            pq_sub = pq_mat[:k, :k]

            diff = (vr - y_sub) % r
            x3 = (diff * inv_mat) % r

            term = y_sub + pq_sub * x3
            total_sum += int(np.sum(np.triu(term, 1)))

        return total_sum


class Solution365(unittest.TestCase):
    def setUp(self):
        self.problem = Problem365()

    def test_solution(self):
        self.assertEqual(162619462356610313, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
