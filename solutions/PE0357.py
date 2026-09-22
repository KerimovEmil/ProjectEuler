"""
PROBLEM

Consider the divisors of 30: 1, 2, 3, 5, 6, 10, 15, 30.
It can be seen that for every divisor d of 30, d+30/d is prime.

Find the sum of all positive integers n not exceeding 100,000,000
such that for every divisor d of n, d+n/d is prime.

ANSWER: 1739023853137
Solve time: ~4.4 seconds
"""

import unittest
import numpy as np
from util.utils import timeit


# Since 1 is always a divisor of n, then
# 1 + n/1 = 1 + n = prime

# n must be even
# since if n is odd then every divisor d must be odd then
# d + n/30 = odd + odd = even != prime if the prime > 2. Which holds for n > 2.

# n is square free
# since if n = p_1 * p_2^2 then choose d = p_2
# p_2 + p_1*p_2 = p_2 * (1 + p_1) != prime.

# combining the last two findings we have, n%4 can only be 0 or 2 since n needs to be odd,
# however since n is squarefree, n%4 can only be equal to 2

# combining this with the fact that n + 1 must be a prime, it results in us only needing
# to loop over primes such that p%4 == 3

# Fast Candidate Filtering and Factor-Tree Divisor Generation:
# - A bytearray prime sieve up to 10^8 allows O(1) primality tests.
# - Filter candidate n = p - 1 for primes p = 3 (mod 4) such that 2 + n // 2 is also prime.
# - Instead of checking ~10,000 trial divisors for each candidate, factorize n into its prime factors
#   to generate only the actual divisors (typically <= 16 divisors per square-free number).
# - Early exit whenever any divisor d produces a composite d + n // d.


class Problem357:
    def __init__(self, max_int=100_000_000, debug=False):
        self.max_int = max_int
        self.debug = debug

    @timeit
    def solve(self):  # noqa: C901
        max_int = self.max_int
        # Bytearray prime sieve
        is_p = bytearray([1]) * (max_int + 2)
        is_p[0] = is_p[1] = 0
        for i in range(2, int((max_int + 1)**0.5) + 1):
            if is_p[i]:
                is_p[i * i:max_int + 2:i] = bytearray(len(range(i * i, max_int + 2, i)))

        # Fast NumPy filtering for initial candidate n
        is_p_np = np.frombuffer(is_p, dtype=np.uint8)
        p_arr = np.nonzero(is_p_np[3::4])[0] * 4 + 3
        n_arr = p_arr - 1
        candidates = n_arr[is_p_np[2 + n_arr // 2] == 1]

        small_primes = [p for p in range(2, 10001) if is_p[p]]
        ans = 1  # for n = 1 (divisors: 1 -> 1+1=2 prime)

        for n in candidates:
            n = int(n)
            # Quick modular filters on small prime factors
            if n % 3 == 0 and not is_p[3 + n // 3]:
                continue
            if n % 5 == 0 and not is_p[5 + n // 5]:
                continue
            if n % 7 == 0 and not is_p[7 + n // 7]:
                continue
            if n % 11 == 0 and not is_p[11 + n // 11]:
                continue

            # Factorize square-free n and test divisors on the fly
            temp = n
            divs = [1]
            valid = True
            for p in small_primes:
                if p * p > temp:
                    break
                if temp % p == 0:
                    temp //= p
                    if temp % p == 0:  # Not square-free
                        valid = False
                        break
                    if not is_p[p + n // p]:
                        valid = False
                        break
                    new_divs = []
                    for d in divs:
                        nd = d * p
                        new_divs.append(nd)
                        if nd > 2 and not is_p[nd + n // nd]:
                            valid = False
                            break
                    if not valid:
                        break
                    divs.extend(new_divs)

            if not valid:
                continue

            if temp > 1:
                if not is_p[temp + n // temp]:
                    continue
                for d in divs:
                    nd = d * temp
                    if nd > 2 and not is_p[nd + n // nd]:
                        valid = False
                        break
                if not valid:
                    continue

            ans += n

        return ans


class Solution357(unittest.TestCase):
    def setUp(self):
        self.problem = Problem357(max_int=int(1e8), debug=False)

    def test_solution(self):
        self.assertEqual(1739023853137, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
