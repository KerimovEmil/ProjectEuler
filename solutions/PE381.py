"""
PROBLEM

For a prime p let S(p) = (sum (p-k)!) mod p for 1 <= k <= 5.

For example, if p=7,

(7-1)! + (7-2)! + (7-3)! + (7-4)! + (7-5)! = 6! + 5! + 4! + 3! + 2! = 720+120+24+6+2 = 872.

As 872 mod (7) = 4, S(7) = 4.

It can be verified that sum S(p) = 480 for 5 <= p < 100.

Find sum S(p) for 5 <= p < 10^8.

ANSWER: 139602943319822
Solve time: 3.661 seconds
"""

import unittest 
from util.utils import timeit, primes_upto


# with Wilson's theorem, we know that (p-1)! = -1 mod p
# so we can rewrite the sum as:
# S(p) = (\sum_{k=1}^{5} (p-k)!) mod p

# (p-1)! = -1 mod p
# (p-2)! = -1/(p-1) = -1/(-1) = 1 mod p
# (p-3)! = 1/(p-2) = 1/(-2) = -1/2 mod p
# (p-4)! = (-1/2)/(p-3) = (-1/2)/(-3) = 1/6 mod p
# (p-5)! = (1/6)/(p-4) = (1/6)/(-4) = -1/24 mod p
# so S(p) = (-1 + 1 - 1/2 + 1/6 - 1/24) mod p = (-12 + 4 - 1)/24 = -9/24 = -3/8 mod p

# 1/(p-1) mod p = x such that x * (p-1) = 1 mod p
# x * (-1) = 1 mod p
# x = -1 mod p

# 1/(p-2) mod p = x such that x * (p-2) = 1 mod p
# x * (-2) = 1 mod p
# x = -1/2 mod p

# 1/(p-3) mod p = x such that x * (p-3) = 1 mod p
# x * (-3) = 1 mod p
# x = -1/3 mod p

# 1/(p-4) mod p = x such that x * (p-4) = 1 mod p
# x * (-4) = 1 mod p
# x = -1/4 mod p

# 1/(p-5) mod p = x such that x * (p-5) = 1 mod p
# x * (-5) = 1 mod p
# x = -1/5 mod p

# We need to find the sum of S(p) for all primes 5 <= p < N
# S(p) = -3/8 mod p

# example N = 100
# S(5) = -3/8 mod 5 = -3 * 2 mod 5 = -6 mod 5 = 4
# S(7) = -3/8 mod 7 = -3 * 6 mod 7 = -18 mod 7 = 4
# S(11) = -3/8 mod 11 = -3 * 7 mod 11 = -21 mod 11 = 1
# S(13) = -3/8 mod 13 = -3 * 5 mod 13 = -15 mod 13 = 11
# S(17) = -3/8 mod 17 = -3 * 15 mod 17 = -45 mod 17 = 11
# S(19) = -3/8 mod 19 = -3 * 12 mod 19 = -36 mod 19 = 2
# S(23) = -3/8 mod 23 = -3 * 14 mod 23 = -42 mod 23 = 4
# S(29) = -3/8 mod 29 = -3 * 11 mod 29 = -33 mod 29 = 26
# S(31) = -3/8 mod 31 = -3 * 27 mod 31 = -81 mod 31 = 13
# S(37) = -3/8 mod 37 = -3 * 28 mod 37 = -84 mod 37 = 9



class Problem381:
    def __init__(self):
        pass

    @timeit
    def solve(self, n):
        primes = primes_upto(n)
        total = 0
        for p in primes[2:]:
            total += self.S(int(p))
        return total

    @staticmethod
    def S(p):
        return (pow(-8, -1, p) * 3) % p


class Solution381(unittest.TestCase):
    def setUp(self):
        self.problem = Problem381()

    def test_small_n(self):
        self.assertEqual(480, self.problem.solve(n=100))

    def test_solution(self):
        self.assertEqual(139602943319822, self.problem.solve(n=int(pow(10, 8))))


if __name__ == '__main__':
    unittest.main()
