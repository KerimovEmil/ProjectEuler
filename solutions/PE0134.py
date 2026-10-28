"""
PROBLEM

Consider the consecutive primes p_1 = 19 and p_2 = 23. It can be verified that 1219 is the smallest number such
that the last digits are formed by p_1 whilst also being divisible by p_2.

In fact, with the exception of p_1 = 3 and p_2 = 5, for every pair of consecutive primes, p_2 > p_1, there exist
values of n for which the last digits are formed by p_1 and n is divisible by p_2. Let S be the smallest of these
values of n.

Find sum S for every pair of consecutive primes with 5 <= p_1 <= 1000000.

ANSWER: 18613426663617118
Solve time: ~0.07 seconds

---
MATHEMATICAL DERIVATION:

1. Linear Congruence Formulation:
   Let d = floor(log_10(p_1)) + 1 be the number of base-10 digits of p_1, and let M = 10^d be the smallest power
   of 10 strictly exceeding p_1.
   Any positive integer n whose trailing decimal digits are p_1 can be written uniquely as:
     n = k * 10^d + p_1   for some integer k >= 0.
   Requiring n to be divisible by p_2 gives the linear congruence:
     k * 10^d + p_1 === 0 (mod p_2)   <=>   k * 10^d === -p_1 (mod p_2).

2. Unique Minimal Solution via Modular Inverse:
   Since p_2 > p_1 >= 5 is prime, gcd(10, p_2) = 1, and therefore gcd(10^d, p_2) = 1.
   Thus, 10^d has a unique multiplicative inverse modulo p_2, and the smallest non-negative integer k solving
   the congruence is:
     k = ((p_2 - p_1) * (10^d)^(-1)) mod p_2.
   Because p_1 is prime and p_2 != p_1, k >= 1 always holds, giving the minimal value:
     S(p_1, p_2) = k * 10^d + p_1.
   Since 10^d only changes when p_1 crosses a power of 10 (at 10, 10^2, ..., 10^6), we maintain 10^d monotonically
   and compute each modular inverse in O(log p_2) time via Python's built-in `pow(pow10, -1, p2)`.
"""

import unittest
from util.utils import primes_upto, timeit


class Problem134:
    def __init__(self, max_p1: int = 1_000_000):
        self.max_p1 = max_p1

    @staticmethod
    def smallest_s(p1: int, p2: int) -> int:
        pow10 = 10
        while pow10 <= p1:
            pow10 *= 10
        k = ((p2 - p1) * pow(pow10, -1, p2)) % p2
        return k * pow10 + p1

    def solve_for_limit(self, max_p1: int) -> int:
        primes = [int(p) for p in primes_upto(max_p1 + 100) if p >= 5]
        total = 0
        pow10 = 10
        for i in range(len(primes) - 1):
            p1 = primes[i]
            if p1 > max_p1:
                break
            p2 = primes[i + 1]
            while pow10 <= p1:
                pow10 *= 10
            k = ((p2 - p1) * pow(pow10, -1, p2)) % p2
            total += k * pow10 + p1
        return total

    @timeit
    def solve(self) -> int:
        return self.solve_for_limit(self.max_p1)


class Solution134(unittest.TestCase):
    def setUp(self):
        self.problem = Problem134()

    def test_sample(self):
        self.assertEqual(1219, self.problem.smallest_s(19, 23))

    def test_solution(self):
        self.assertEqual(18613426663617118, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
