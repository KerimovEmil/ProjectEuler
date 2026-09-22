"""
PROBLEM

The number of divisors of 120 is 16.
In fact 120 is the smallest number having 16 divisors.

Find the smallest number with 2^500500 divisors.
Give your answer modulo 500500507.

ANSWER: 35407281
Solve time: ~0.35 seconds

---
MATHEMATICAL DERIVATION:

Let N = prod p_i^{a_i}. The number of divisors of N is d(N) = prod (a_i + 1).
We require d(N) = 2^K with K = 500500.
Since the divisor count is a power of 2, each factor (a_i + 1) must be a power of 2:
a_i + 1 = 2^{k_i} ==> a_i = 2^{k_i} - 1.
In binary, a_i = 1 + 2 + 4 + ... + 2^{k_i - 1}.
Each increment of k_i doubles the number of divisors and multiplies N by p_i^{2^j} for some j >= 0.
To minimize N, we greedily select the smallest K values from the set of prime powers {p^{2^j} : p prime, j >= 0}.
We can maintain these candidate factors using a min-heap or by merging the prime stream with small powers p^{2^j}.
"""

import heapq
import unittest
from util.utils import primes_upto, timeit


class Problem500:
    def __init__(self):
        # 500500 = 2^2 × 5^3 × 7 × 11 × 13
        # divisors(p1^{k1} x p2^{k2} x p3^{k3} x ... x pn^{kn}) = (k1+1) x (k2+1) x (k3+1) x ... x (kn+1)
        # divisors(p1*p2*p3*...*pn) = (1+1)^n = 2^n
        # d(2*3*5*7) = d(210) = (1+1)*(1+1)*(1+1)*(1+1) = 2^4 = 16
        # d(2^3*3*5) = d(120) = (1+3)*(1+1)*(1+1) = 2^4
        # 2^31 * 3^15 * 5^15 * 7^15 * 11^7 * 13^7 * 17^7 * 19^7 * 23^7 * 31^7 * 37^7 * 41^7 * 43^7 * 47^7 * 53^3 * ...
        # * 7370029
        pass

    @timeit
    def solve(self, k=500500, mod=500500507):
        # The k-th prime for k=500500 is 7370029
        limit = 7400000 if k >= 500500 else 100
        primes = list(primes_upto(limit))

        h = primes[:k]
        heapq.heapify(h)

        ans = 1
        for _ in range(k):
            val = heapq.heappop(h)
            ans = (ans * (val % mod)) % mod
            heapq.heappush(h, val * val)

        return ans


class Solution500(unittest.TestCase):
    def setUp(self):
        self.problem = Problem500()

    def test_small(self):
        # Smallest number with 2^4 = 16 divisors is 120
        self.assertEqual(120, self.problem.solve(k=4, mod=10**9))

    def test_solution(self):
        self.assertEqual(35407281, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
