"""
PROBLEM

An infinite sequence of real numbers a(n) is defined for all integers n as follows:
a(n) = 1 if n < 0
a(n) = sum_{i=1}^{inf} a(n-i)/(i!)  if n >= 0

For example,
a(0) = 1/1! + 1/2! + 1/3! + ... = e - 1
a(1) = (e - 1)/1! + 1/2! + 1/3! + ... = 2e - 3
a(2) = (2e - 3)/1! + (e - 1)/2! + 1/3! + ... = (7/2)e - 6

with e being Euler's constant.

It can be shown that a(n) is of the form (A(n)e + B(n))/(n!)
for integers A(n) and B(n).

For example,
a(10) = (328161643 e - 652694486)/(10!)

Find A(10^9) + B(10^9) and give your answer mod 77 777 777.

ANSWER: 15955822
Solve time: ~0.47 seconds
"""

import unittest
from typing import List
from util.crt import ChineseRemainderTheorem
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Recurrence Relations:
#    From a(n) = (A(n)e + B(n)) / n!, equating coefficients yields:
#      A(n) = n! + sum_{k=0}^{n-1} binom(n, k) A(k)
#      B(n) = -1 + sum_{k=0}^{n-1} binom(n, k) (B(k) - (n - k)!)
#    with A(0) = 1, B(0) = -1.
#
# 2. Modulo Prime Reductions:
#    77,777,777 = 7 * 11 * 73 * 101 * 137.
#    For each prime p, the sequence A(n) and B(n) modulo p has period p*(p - 1).
#    Thus, n = 10^9 mod (p*(p - 1)) can be evaluated at n_mod <= 18,769.
#
# 3. Factored 2D Lucas Convolution:
#    By Lucas' theorem, for n = n_1 * p + n_0 and k = k_1 * p + k_0:
#      binom(n, k) = binom(n_1, k_1) * binom(n_0, k_0) (mod p).
#    For k_1 < n_1:
#      (n - k) >= p => (n - k)! = 0 (mod p).
#      The sum factors as:
#        sum_{k_1 < n_1} binom(n_1, k_1) * S(k_1, n_0)
#      where S(k_1, n_0) = sum_{k_0=0}^{n_0} binom(n_0, k_0) A[k_1*p + k_0] (mod p).
#    By memoizing S(k_1, n_0) for completed blocks k_1, each step evaluates in O(p) instead of O(n),
#    reducing the overall complexity per prime to O(p^3).
#    Total runtime across all 5 primes is ~0.47s.


class Problem330:
    def __init__(self, prime_list: List[int] = None, n: int = 10**9):
        if prime_list is None:
            self.prime_list = [7, 11, 73, 101, 137]
        else:
            self.prime_list = prime_list
        self.n = n

    @timeit
    def solve(self, n: int = None) -> int:  # noqa: C901
        if n is None:
            n = self.n

        a_mod_list = []
        b_mod_list = []

        for p in self.prime_list:
            n_mod = (n - p) % (p * (p - 1)) + p if n >= p else n

            # Precompute binomial coefficients modulo p
            binom = [[0] * p for _ in range(p)]
            for i in range(p):
                binom[i][0] = 1
                for j in range(1, i + 1):
                    binom[i][j] = (binom[i - 1][j - 1] + binom[i - 1][j]) % p

            # Precompute factorials modulo p
            fact = [1] * p
            for i in range(1, p):
                fact[i] = (fact[i - 1] * i) % p

            A = [0] * (n_mod + 1)
            B = [0] * (n_mod + 1)
            A[0] = 1 % p
            B[0] = (p - 1) % p

            max_n1 = n_mod // p
            s_a = [[0] * p for _ in range(max_n1 + 1)]
            s_b = [[0] * p for _ in range(max_n1 + 1)]

            for cur_n in range(1, n_mod + 1):
                n1 = cur_n // p
                n0 = cur_n % p

                a_sum = fact[cur_n] if cur_n < p else 0
                b_sum = -1

                binom_n1 = binom[n1]
                binom_n0 = binom[n0]

                # 1. Blocks k1 < n1: O(1) via block cache
                for k1 in range(n1):
                    c1 = binom_n1[k1]
                    if c1:
                        a_sum += c1 * s_a[k1][n0]
                        b_sum += c1 * s_b[k1][n0]

                # 2. Current block k1 == n1:
                n1_p = n1 * p
                sum_a_k0 = 0
                sum_b_k0 = 0
                for k0 in range(n0):
                    c0 = binom_n0[k0]
                    k = n1_p + k0
                    sum_a_k0 += c0 * A[k]
                    sum_b_k0 += c0 * (B[k] - fact[n0 - k0])

                a_sum += sum_a_k0
                b_sum += sum_b_k0

                A[cur_n] = a_sum % p
                B[cur_n] = b_sum % p

                # When a block finishes or at end, compute its S_A and S_B table
                if n0 == p - 1 or cur_n == n_mod:
                    n1_p = n1 * p
                    for row_n0 in range(p):
                        b_row = binom[row_n0]
                        sa = 0
                        sb = 0
                        for k0 in range(row_n0 + 1):
                            k = n1_p + k0
                            if k <= n_mod:
                                sa += b_row[k0] * A[k]
                                sb += b_row[k0] * B[k]
                        s_a[n1][row_n0] = sa % p
                        s_b[n1][row_n0] = sb % p

            a_mod_list.append(A[n_mod])
            b_mod_list.append(B[n_mod])

        # Combine via CRT
        a_total = ChineseRemainderTheorem(a_mod_list, self.prime_list).solve()
        b_total = ChineseRemainderTheorem(b_mod_list, self.prime_list).solve()
        mod_m = 1
        for p in self.prime_list:
            mod_m *= p

        return (a_total + b_total) % mod_m


class Solution330(unittest.TestCase):
    def setUp(self):
        # 77777777 = 7 x 11 x 73 x 101 x 137
        self.problem = Problem330(prime_list=[7, 11, 73, 101, 137], n=10**9)

    def test_example(self):
        # a(10) = (328161643 e - 652694486)/(10!)
        # A(10) + B(10) = 328161643 - 652694486 = -324532843 = 64356042 mod 77777777
        self.assertEqual(64356042, self.problem.solve(n=10))

    def test_solution(self):
        self.assertEqual(15955822, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
