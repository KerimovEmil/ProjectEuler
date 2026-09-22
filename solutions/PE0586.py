"""
PROBLEM

The number 209 can be expressed as a^2 + 3ab + b^2 in two distinct ways:
209 = 8^2 + 3*8*5 + 5^2
209 = 13^2 + 3*13*1 + 1^2

Let f(n, r) be the number of integers k not exceeding n that can be expressed as
k = a^2 + 3ab + b^2, with a > b > 0 integers, in exactly r different ways.

You are given that f(10^5, 4) = 237 and f(10^8, 6) = 59517.

Find f(10^15, 40).

ANSWER: 82490213
Solve time: ~5.5 seconds

---
MATHEMATICAL DERIVATION:

1. Arithmetic in the Ring of Integers of Q(sqrt(5)):
   The quadratic form Q(a, b) = a^2 + 3ab + b^2 has discriminant D = 5.
   In the ring of integers Z[phi] where phi = (1 + sqrt(5))/2:
   Norm N(x + y phi) = x^2 + xy - y^2 = Q(x - y, y) for x = a + b, y = b.
   Primes decompose as follows:
   - p = 5: ramified (5 = (sqrt(5))^2).
   - p = 1, 4 mod 5: split into conjugate primes pi, bar{pi} with norm p.
   - q = 2, 3 mod 5: inert with norm q^2.

2. Representation Count R(k):
   Let k = 5^{e_5} prod_{p_i = 1,4 mod 5} p_i^{a_i} prod_{q_j = 2,3 mod 5} q_j^{b_j}.
   If any b_j is odd, R(k) = 0.
   If all b_j are even, let D = prod_{p_i} (a_i + 1):
   - If D is even: R(k) = D / 2.
   - If D is odd: R(k) = (D - 1) / 2.

3. Sieve and Counting:
   To find all k <= N with R(k) = r, k must factor as M * Y where:
   - M is the core composed of split primes p = 1, 4 mod 5 whose exponent pattern matches
     either D = 2r (at least one odd exponent) or D = 2r + 1 (all even exponents).
   - Y has no prime factors congruent to 1, 4 mod 5, and all inert prime factors have even powers.
     Equivalently, Y = W^2 or 5 W^2 where W has no split prime factors.
   Precomputing the prefix sums of such W <= sqrt(N) enables O(1) evaluation of count_Y(X).
   For large patterns such as (4, 1, 1, 1, 1), interval grouping over split prime counting
   pi_split(x) accelerates the search to ~5.5s for N = 10^15.
"""

import bisect
from collections import Counter
import math
import unittest
import numpy as np
from util.utils import timeit


def g(a: int, b: int) -> int:
    return a**2 + 3 * a * b + b**2


def g2(z: int, b: int) -> int:
    return z**2 - 5 * b**2


def get_divisors(n: int):
    res = []
    for d in range(2, n + 1):
        if n % d == 0:
            res.append(d)
    return res


def get_partitions(rem_d: int, min_d: int):
    if rem_d == 1:
        return [()]
    parts = []
    for d in get_divisors(rem_d):
        if d >= min_d:
            for sub in get_partitions(rem_d // d, d):
                parts.append((d,) + sub)
    return parts


class Problem586:
    def __init__(self):
        # 4k + 5b^2 = z^2
        # z > 5b > 0
        pass

    @staticmethod
    def direct_form(n: int, r: int) -> int:
        """Count integers k <= n expressible in exactly r ways directly."""
        dc = {}
        max_a_int = int(((5 + 4 * n)**0.5 - 3) / 2)

        for a in range(1, max_a_int + 1):
            max_b_real = ((5 * a * a + 4 * n)**0.5 - 3 * a) / 2
            max_b_int = min(int(max_b_real), a - 1)
            for b in range(1, max_b_int + 1):
                t = g(a, b)
                dc[t] = dc.get(t, 0) + 1

        return sum(1 for v in dc.values() if v == r)

    @staticmethod
    def adjusted_form(n: int, r: int) -> int:
        """Count integers k <= n via 4k = z^2 - 5b^2."""
        dc = {}
        max_z_int = int((5 + 4 * n) ** 0.5)

        for z in range(6, max_z_int + 1):
            max_b_int = z // 5 - 1
            for b in range(1, max_b_int + 1):
                t = g2(z, b)
                if t % 4 == 0 and t > 0:
                    k = t // 4
                    if k <= n:
                        dc[k] = dc.get(k, 0) + 1

        return sum(1 for v in dc.values() if v == r)

    def _setup_sieve(self, max_n):
        w_limit = int(math.isqrt(max_n)) + 1
        prime_limit = min(max(w_limit, max_n // 209 + 1, 1000), 32000000)

        is_prime = np.ones(prime_limit, dtype=bool)
        is_prime[:2] = False
        for i in range(2, int(math.isqrt(prime_limit)) + 1):
            if is_prime[i]:
                is_prime[i * i::i] = False

        split_mask = is_prime & ((np.arange(prime_limit) % 5 == 1) | (np.arange(prime_limit) % 5 == 4))
        split_primes_arr = np.where(split_mask)[0]
        split_primes = [int(p) for p in split_primes_arr]

        valid = np.ones(w_limit, dtype=np.uint8)
        valid[0] = 0
        for p in split_primes:
            if p < w_limit:
                valid[p::p] = 0

        pref = np.cumsum(valid)
        return split_primes, pref

    def _get_target_patterns(self, r):
        target_cases = []
        d_even = 2 * r
        for p in get_partitions(d_even, 2):
            exps = tuple(d - 1 for d in p)
            if any(e % 2 != 0 for e in exps):
                target_cases.append(exps)

        d_odd = 2 * r + 1
        for p in get_partitions(d_odd, 2):
            exps = tuple(d - 1 for d in p)
            if all(e % 2 == 0 for e in exps):
                target_cases.append(exps)
        return target_cases

    def _count_y(self, x, pref):
        if x <= 0:
            return 0
        w = math.isqrt(x)
        ans = int(pref[w])
        w5 = math.isqrt(x // 5)
        ans += int(pref[w5])
        return ans

    def _sum_last_prime_intervals(self, base_prod, p_min, max_n, used, split_primes, pref):
        max_last_p = max_n // base_prod
        if max_last_p < p_min:
            return 0

        cur_high = max_last_p
        x_val = 1
        subtotal = 0
        while cur_high >= p_min:
            next_high = max_n // (base_prod * (x_val + 1))
            low = max(p_min - 1, next_high)
            high = cur_high
            if high > low:
                c = bisect.bisect_right(split_primes, high) - bisect.bisect_right(split_primes, low)
                for u in used:
                    if low < u <= high:
                        c -= 1
                if c > 0:
                    subtotal += c * self._count_y(x_val, pref)
            cur_high = low
            x_val += 1
        return subtotal

    def _search_pattern(self, exp_idx, used, cur_m, d_exps, counts, max_n, split_primes, pref):
        if exp_idx == len(d_exps):
            return self._count_y(max_n // cur_m, pref)

        e = d_exps[exp_idx]
        k = counts[e]
        total = 0

        def choose_primes(rem_k, min_p_idx, cur_prod, chosen):
            nonlocal total
            if rem_k == 0:
                total += self._search_pattern(
                    exp_idx + 1, used | set(chosen), cur_m * cur_prod,
                    d_exps, counts, max_n, split_primes, pref
                )
                return

            if rem_k == 1 and exp_idx == len(d_exps) - 1 and e == 1:
                base_prod = cur_m * cur_prod
                if min_p_idx < len(split_primes):
                    p_min = split_primes[min_p_idx]
                    used_all = used | set(chosen)
                    total += self._sum_last_prime_intervals(
                        base_prod, p_min, max_n, used_all, split_primes, pref
                    )
                return

            for idx in range(min_p_idx, len(split_primes)):
                p = split_primes[idx]
                if p in used:
                    continue
                if cur_m * cur_prod * (p**(e * rem_k)) > max_n:
                    break
                choose_primes(rem_k - 1, idx + 1, cur_prod * (p**e), chosen + [p])

        choose_primes(k, 0, 1, [])
        return total

    def fast_form(self, max_n: int, r: int) -> int:
        split_primes, pref = self._setup_sieve(max_n)
        target_cases = self._get_target_patterns(r)
        total = 0

        for pattern in target_cases:
            counts = Counter(pattern)
            distinct_exps = sorted(counts.keys(), reverse=True)
            total += self._search_pattern(
                0, set(), 1, distinct_exps, counts, max_n, split_primes, pref
            )

        return total

    @timeit
    def solve(self, n=10**15, r=40):
        if n <= 1000:
            return self.direct_form(n, r)
        return self.fast_form(n, r)


class Solution586(unittest.TestCase):
    def setUp(self):
        self.problem = Problem586()

    def test_no_solution(self):
        self.assertEqual(0, self.problem.solve(n=208, r=2))

    def test_first_solution(self):
        self.assertEqual(1, self.problem.solve(n=209, r=2))

    def test_small_solution(self):
        self.assertEqual(237, self.problem.solve(n=int(1e5), r=4))

    def test_1e6_solution(self):
        self.assertEqual(6, self.problem.solve(n=int(1e6), r=5))

    def test_5e6_solution(self):
        self.assertEqual(50, self.problem.solve(n=int(5e6), r=5))

    def test_final_solution(self):
        self.assertEqual(82490213, self.problem.solve(n=10**15, r=40))


if __name__ == '__main__':
    unittest.main()
