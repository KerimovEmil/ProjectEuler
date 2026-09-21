"""
PROBLEM

For a positive number n, define C(n) as the number of the integers x, for which 1 < x < n and x^3 ≡ 1 mod n.

When n = 91, there are 8 possible values for x, so C(91) = 8.
We are given that C(91) = 8, C(280) = 8, C(4740) = 8, C(14210) = 8, C(89260) = 8.

Find the sum of all n <= 10^11 for which C(n) = 242.

ANSWER: 8495585919506151122
Solve time: ~4.0 seconds
"""

import bisect
import math
import unittest
from util.utils import timeit, is_prime_simple


# MATHEMATICAL DERIVATION:
#
# 1. Problem Characterization:
#    We seek the sum of all integers n <= L = 10^11 such that the number of non-trivial
#    roots of x^3 = 1 (mod n) is 242.
#    Since x = 1 is always a root, the total number of solutions in [1, n] is:
#      R(n) = C(n) + 1 = 243 = 3^5.
#
# 2. Multiplicative Structure of R(n):
#    By the Chinese Remainder Theorem, if n = prod p_i^{a_i}, then R(n) = prod R(p_i^{a_i}).
#    For prime powers p^a:
#      - If p = 1 (mod 3):
#          The multiplicative group (Z / p^a Z)* is cyclic of order phi(p^a) = p^{a-1}(p - 1).
#          Since 3 | (p - 1), gcd(3, phi(p^a)) = 3.
#          Thus, R(p^a) = 3 for any a >= 1 when p = 1 (mod 3).
#      - If p = 3:
#          For p = 3 (a = 1): (Z / 3Z)* has order 2 (not divisible by 3) => R(3) = 1.
#          For p = 3 (a >= 2): (Z / 3^a Z)* has order 2 * 3^{a-1} (divisible by 3) => R(3^a) = 3.
#      - If p = 2 (mod 3) or p = 2:
#          gcd(3, phi(p^a)) = 1 => R(p^a) = 1 for all a >= 1.
#
# 3. Necessary and Sufficient Conditions for R(n) = 3^5 = 243:
#    Let S_1 = {p prime : p = 1 (mod 3)} = {7, 13, 19, 31, 37, 43, 61, ...}.
#    There are two mutually exclusive ways R(n) can equal 3^5:
#      - Case A: n is divisible by exactly 5 distinct primes from S_1, and 9 does not divide n.
#                (n may or may not be divisible by 3^1).
#      - Case B: n is divisible by exactly 4 distinct primes from S_1, and 3^a divides n with a >= 2.
#
# 4. Kernel Decomposition and S_2-Smooth Multipliers:
#    Any valid n can be uniquely factored as n = m * b, where:
#      - m (the "kernel") is composed solely of prime factors from S_1 and powers of 3.
#      - b is coprime to all primes in S_1 and coprime to 3 (prime factors from S_2 = {p : p = 2 (mod 3)} U {2}).
#    The minimum product of 4 primes from S_1 combined with 3^2 is 9 * 7 * 13 * 19 = 15,561.
#    Thus the maximum prime in S_1 for L = 10^11 is at most L / 15,561 ~ 6.42 * 10^6.
#    The maximum cofactor b is at most L / (9 * 7 * 13 * 19 * 31) = L / 482,391 < 208,000.
#    We precompute the prefix sum table:
#      sum_b[X] = sum_{b <= X, b is S_2-smooth} b.
#
# 5. Fast Tree Search with Hyperbolic Interval Summation:
#    In Case A, we pick 4 distinct primes p_1 < p_2 < p_3 < p_4.
#    For the 5th prime p_5:
#      - For small p_5 <= sqrt(L / prod), we recurse directly to handle higher powers p_5^k and cofactors.
#      - For p_5 > sqrt(L / prod), p_5 must have exponent 1.
#        The term floor(L / (prod * p_5)) = k takes small integer values k <= sqrt(L / prod).
#        For each fixed k, p_5 falls in the interval ( floor(L / (prod * (k+1))), floor(L / (prod * k)) ].
#        Within this interval, sum_b[floor(L / (prod * p_5))] = sum_b[k] is constant.
#        The sum over all primes p_5 in this range is obtained in O(1) via prefix sums of S_1 primes.
#    Similarly in Case B, for 3 distinct primes and 3^a (a >= 2), the 4th prime is summed via interval queries.
#
# 6. Complexity:
#    - Sieve primes up to ~6.42 * 10^6 takes ~0.2s.
#    - Precomputing sum_b table takes <0.1s.
#    - Search with hyperbolic interval summation executes in ~3.8s.
#    - Total execution time is ~4.0s.


class Problem272:
    def __init__(self, limit: int = 10**11):
        self.limit = limit

    @timeit
    def solve(self, limit: int = None) -> int:
        if limit is None:
            limit = self.limit

        # 1. Sieve primes up to max possible prime in S1
        # In Case B, 9 * 7 * 13 * 19 = 15,561 is the minimum base for the 4th prime.
        min_prod = 9 * 7 * 13 * 19
        max_p = limit // min_prod + 100 if limit >= min_prod else 100

        is_prime = bytearray([1]) * (max_p + 1)
        is_prime[0] = is_prime[1] = 0
        for p in range(2, int(math.isqrt(max_p)) + 1):
            if is_prime[p]:
                is_prime[p * p::p] = bytearray(len(is_prime[p * p::p]))

        # Collect S1 = {p prime : p = 1 (mod 3)} and prefix sums
        s1 = [p for p in range(7, max_p + 1) if p % 3 == 1 and is_prime[p]]
        prefix_s1_sum = [0] * (len(s1) + 1)
        for i, p in enumerate(s1):
            prefix_s1_sum[i + 1] = prefix_s1_sum[i] + p

        # 2. Precompute S2-smooth numbers b (factors only primes = 2 mod 3 and 2)
        min_kernel = 9 * 7 * 13 * 19 * 31  # 482,391
        max_b = limit // min_kernel + 100 if limit >= min_kernel else 100

        valid_b = bytearray([1]) * (max_b + 1)
        valid_b[0] = 0
        for i in range(3, max_b + 1, 3):
            valid_b[i] = 0
        for p in s1:
            if p > max_b:
                break
            valid_b[p::p] = bytearray(len(valid_b[p::p]))

        sum_b = [0] * (max_b + 1)
        for i in range(1, max_b + 1):
            sum_b[i] = sum_b[i - 1] + (i if valid_b[i] else 0)

        total_ans = 0

        def add_kernel(m: int, mult_by_3: bool = False):
            nonlocal total_ans
            if m <= limit:
                total_ans += m * sum_b[limit // m]
            if mult_by_3 and m * 3 <= limit:
                total_ans += (m * 3) * sum_b[limit // (m * 3)]

        # Hyperbolic interval processing for the 5th prime in Case A
        def process_last_prime_a(prod: int, start_idx: int):
            nonlocal total_ans
            limit_p5 = limit // prod
            if start_idx >= len(s1) or s1[start_idx] > limit_p5:
                return

            split_p5 = math.isqrt(limit_p5)
            i = start_idx
            while i < len(s1) and s1[i] <= split_p5:
                p = s1[i]
                p_pow = p
                while prod * p_pow <= limit:
                    add_kernel(prod * p_pow, mult_by_3=True)
                    p_pow *= p
                i += 1

            p5_min = s1[start_idx] if start_idx >= i else s1[i]
            max_k = limit_p5 // p5_min
            if max_k == 0:
                return

            for k in range(1, max_k + 1):
                sb = sum_b[k]
                if sb == 0:
                    continue
                high_p5 = limit_p5 // k
                low_p5 = max(p5_min, (limit_p5 // (k + 1)) + 1)
                if low_p5 <= high_p5:
                    idx_low = bisect.bisect_left(s1, low_p5)
                    idx_high = bisect.bisect_right(s1, high_p5)
                    if idx_low < idx_high:
                        s_primes = prefix_s1_sum[idx_high] - prefix_s1_sum[idx_low]
                        total_ans += prod * sb * s_primes

            limit_p5_3 = limit // (3 * prod)
            if limit_p5_3 >= p5_min:
                max_k3 = limit_p5_3 // p5_min
                for k in range(1, max_k3 + 1):
                    sb = sum_b[k]
                    if sb == 0:
                        continue
                    high_p5 = limit_p5_3 // k
                    low_p5 = max(p5_min, (limit_p5_3 // (k + 1)) + 1)
                    if low_p5 <= high_p5:
                        idx_low = bisect.bisect_left(s1, low_p5)
                        idx_high = bisect.bisect_right(s1, high_p5)
                        if idx_low < idx_high:
                            s_primes = prefix_s1_sum[idx_high] - prefix_s1_sum[idx_low]
                            total_ans += (3 * prod) * sb * s_primes

        # Hyperbolic interval processing for the 4th prime in Case B
        def process_last_prime_b(prod: int, start_idx: int):
            nonlocal total_ans
            limit_p4 = limit // prod
            if start_idx >= len(s1) or s1[start_idx] > limit_p4:
                return

            split_p4 = math.isqrt(limit_p4)
            i = start_idx
            while i < len(s1) and s1[i] <= split_p4:
                p = s1[i]
                p_pow = p
                while prod * p_pow <= limit:
                    add_kernel(prod * p_pow, mult_by_3=False)
                    p_pow *= p
                i += 1

            p4_min = s1[start_idx] if start_idx >= i else s1[i]
            max_k = limit_p4 // p4_min
            if max_k == 0:
                return

            for k in range(1, max_k + 1):
                sb = sum_b[k]
                if sb == 0:
                    continue
                high_p4 = limit_p4 // k
                low_p4 = max(p4_min, (limit_p4 // (k + 1)) + 1)
                if low_p4 <= high_p4:
                    idx_low = bisect.bisect_left(s1, low_p4)
                    idx_high = bisect.bisect_right(s1, high_p4)
                    if idx_low < idx_high:
                        s_primes = prefix_s1_sum[idx_high] - prefix_s1_sum[idx_low]
                        total_ans += prod * sb * s_primes

        # Search Case A: Exactly 5 distinct primes from S1, 9 does not divide n
        def search_a(idx: int, count: int, prod: int):
            if count == 4:
                process_last_prime_a(prod, idx)
                return
            rem = 5 - count
            for i in range(idx, len(s1)):
                p = s1[i]
                if prod * (p ** rem) > limit:
                    break
                p_pow = p
                while prod * p_pow <= limit:
                    search_a(i + 1, count + 1, prod * p_pow)
                    p_pow *= p

        # Search Case B: Exactly 4 distinct primes from S1, and 3^a | n with a >= 2
        def search_b(idx: int, count: int, prod: int):
            if count == 3:
                process_last_prime_b(prod, idx)
                return
            rem = 4 - count
            for i in range(idx, len(s1)):
                p = s1[i]
                if prod * (p ** rem) > limit:
                    break
                p_pow = p
                while prod * p_pow <= limit:
                    search_b(i + 1, count + 1, prod * p_pow)
                    p_pow *= p

        search_a(0, 0, 1)

        p3 = 9
        while p3 <= limit:
            search_b(0, 0, p3)
            p3 *= 3

        return total_ans


class Solution272(unittest.TestCase):
    def setUp(self):
        self.problem = Problem272()

    def test_primality_util(self):
        # Verify first primes in S1 using is_prime_simple
        for p in [7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97]:
            self.assertTrue(is_prime_simple(p))
            self.assertEqual(1, p % 3)

    def test_small_limits(self):
        # Minimal number with C(n) = 242 is 9 * 7 * 13 * 19 * 31 = 482,391
        self.assertEqual(482391, self.problem.solve(limit=482391))

    def test_solution(self):
        self.assertEqual(8495585919506151122, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
