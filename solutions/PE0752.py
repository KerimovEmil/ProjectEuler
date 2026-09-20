"""
PROBLEM

When (1+sqrt(7)) is raised to an integral power, n, we always get a number of the form (a + b*sqrt(7)).
We write (1 + sqrt(7))^n = a(n) + b(n) * sqrt(7)

For a given number x we define g(x) to be the smallest positive integer n such that:
a(n) == 1 mod x
b(n) == 0 mod x
and g(x) = 0 if there is no such value of n. For example, g(3) = 0, g(5) = 12.

Further define
G(N) = sum_{x=2}^{N} g(x)

You are given G(100) = 28891 and G(1000) = 13131583

Find G(1000000)

ANSWER: 5610899769745488
Solve time: ~4.1 seconds
"""

import math
import unittest
from util.utils import timeit, tonelli_shanks


# MATHEMATICAL DERIVATION:
# Let u = 1 + sqrt(7).
# Note that N(u) = (1 + sqrt(7))(1 - sqrt(7)) = -6.
#
# 1. Non-invertible elements (gcd(x, 6) > 1):
#    If 2 | x or 3 | x, then N(u^n) = (-6)^n is divisible by 2 or 3.
#    If a(n) == 1 mod x and b(n) == 0 mod x, then N(u^n) = a(n)^2 - 7*b(n)^2 == 1 mod x.
#    Since (-6)^n = 0 mod gcd(x, 6), this has no solution for gcd(x, 6) > 1.
#    Thus, g(x) = 0 whenever gcd(x, 6) > 1.
#
# 2. Multiplicative structure via Chinese Remainder Theorem:
#    For gcd(x, 6) = 1, u is a unit in the ring (Z/xZ)[sqrt(7)].
#    For x = p1^e1 * p2^e2 * ..., g(x) = lcm(g(p1^e1), g(p2^e2), ...).
#
# 3. Prime powers:
#    For a prime p and power p^k: g(p^k) = g(p) * p^(k-1) (unless already satisfied mod p^k,
#    verified by checking mat_pow((1,1), g(p), p^k) == (1,0)).
#
# 4. Primes p >= 5:
#    - For p = 7: g(7) = 7 (since (1+sqrt(7))^7 == 1 + 7^(7/2) == 1 mod 7).
#    - If (7/p) = 1 (7 is quadratic residue mod p):
#      Let s = sqrt(7) mod p via Tonelli-Shanks. In F_p, sqrt(7) exists, so u = 1 + sqrt(7)
#      and its conjugate 1 - sqrt(7) are the two eigenvalues of the recurrence matrix mod p.
#      g(p) = lcm(ord_p(1 + s), ord_p(1 - s)), where both orders divide (p - 1).
#    - If (7/p) = -1 (7 is quadratic non-residue mod p):
#      The Frobenius automorphism of F_{p^2}/F_p maps sqrt(7) -> -sqrt(7), so u^p == 1-sqrt(7) mod p.
#      Hence u^(p+1) == (1 + sqrt(7))(1 - sqrt(7)) = -6 in F_p (a scalar).
#      The smallest d | (p + 1) such that b(d) == 0 mod p gives u^d == a_d in F_p.
#      Then g(p) = d * ord_p(a_d), where ord_p(a_d) divides (p - 1).


def mat_mul(A, B, mod):
    return (
        (A[0] * B[0] + 7 * A[1] * B[1]) % mod,
        (A[0] * B[1] + A[1] * B[0]) % mod
    )


def mat_pow(A, p, mod):
    res = (1, 0)
    base = A
    while p > 0:
        if p & 1:
            res = mat_mul(res, base, mod)
        base = mat_mul(base, base, mod)
        p >>= 1
    return res


class Problem752:
    def __init__(self, max_n: int = 1000000):
        self.max_n = max_n

    @staticmethod
    def _order_scalar(val: int, p: int, prime_factors_of_order: list) -> int:
        if val == 1:
            return 1
        if val == p - 1:
            return 2
        ord_v = p - 1
        for q in prime_factors_of_order:
            while ord_v % q == 0:
                if pow(val, ord_v // q, p) == 1:
                    ord_v //= q
                else:
                    break
        return ord_v

    @timeit
    def solve(self, n: int = None) -> int:
        if n is None:
            n = self.max_n

        # Sieve for smallest prime factor up to n + 2
        spf = list(range(n + 3))
        for i in range(2, int((n + 3) ** 0.5) + 1):
            if spf[i] == i:
                for j in range(i * i, n + 3, i):
                    if spf[j] == j:
                        spf[j] = i

        def get_prime_factors(m: int) -> list:
            res = []
            while m > 1:
                p = spf[m]
                res.append(p)
                while m % p == 0:
                    m //= p
            return res

        def get_prime_order(p: int) -> int:
            if p in (2, 3):
                return 0
            if p == 7:
                return 7

            leg = pow(7, (p - 1) // 2, p)
            if leg == 1:
                s = tonelli_shanks(7, p)
                f_p_minus_1 = get_prime_factors(p - 1)
                o1 = self._order_scalar((1 + s) % p, p, f_p_minus_1)
                o2 = self._order_scalar((1 - s) % p, p, f_p_minus_1)
                return math.lcm(o1, o2)
            else:
                d = p + 1
                for q in get_prime_factors(p + 1):
                    while d % q == 0:
                        val = mat_pow((1, 1), d // q, p)
                        if val[1] == 0:
                            d //= q
                        else:
                            break
                a_d = mat_pow((1, 1), d, p)[0]
                if a_d == 1:
                    return d
                if a_d == p - 1:
                    return d * 2

                ord_a = self._order_scalar(a_d, p, get_prime_factors(p - 1))
                return d * ord_a

        g = [0] * (n + 1)

        # 1. Compute g for primes and prime powers
        for p in range(5, n + 1):
            if spf[p] == p:
                g[p] = get_prime_order(p)
                pk = p * p
                prev = g[p]
                while pk <= n:
                    if mat_pow((1, 1), prev, pk) == (1, 0):
                        g[pk] = prev
                    else:
                        g[pk] = prev * p
                    prev = g[pk]
                    pk *= p

        # 2. Compute g for composite numbers via CRT
        for x in range(5, n + 1):
            if x % 2 == 0 or x % 3 == 0:
                continue
            p = spf[x]
            temp = x
            pk = 1
            while temp % p == 0:
                pk *= p
                temp //= p
            if temp != 1:
                g[x] = math.lcm(g[pk], g[temp])

        return sum(g)


class Solution752(unittest.TestCase):
    def setUp(self):
        self.problem = Problem752()

    def test_solution_small_1(self):
        """G(100) = 28891"""
        self.assertEqual(28891, self.problem.solve(n=100))

    def test_solution_small_2(self):
        """G(1000) = 13131583"""
        self.assertEqual(13131583, self.problem.solve(n=1000))

    def test_solution(self):
        self.assertEqual(5610899769745488, self.problem.solve())


if __name__ == '__main__':
    unittest.main()