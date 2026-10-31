"""
PROBLEM

Two players are playing a game. There are k piles of counters. The sizes of the piles are between 2 and n.
At each turn a player chooses a pile of size s and replaces it with two piles of maximum size s - 1 each,
both sizes being a divisor of s and greater than 1.
The player unable to make a move loses.

Let f(n, k) be the number of winning positions for the first player, assuming perfect play, when the game
is played with k piles each having between 2 and n counters.

For example, f(10, 5) = 40085.

Find f(10^7, 10^{12}) mod 987654321.

ANSWER: 328104836
Solve time: ~1.5 seconds

---
MATHEMATICAL DERIVATION:

1. Game Theory and Sprague-Grundy Theorem:
   The game is an impartial game played under normal play convention.
   By the Sprague-Grundy theorem, each single pile of size s has an independent Grundy value (nim-value) g(s):
     g(s) = mex { g(a) ^ g(b) : 1 < a < s, 1 < b < s, a | s, b | s }.
   Since a and b can be chosen independently from the proper divisors of s strictly greater than 1:
     M(s) = { u ^ v : u, v in V(s) }, where V(s) = { g(d) : d | s, 1 < d < s }.
   Then g(s) = mex(M(s)).
   For prime p, V(p) = {} ==> g(p) = 0.

2. Invariance with respect to Omega(s):
   We show by induction on Omega(s) (the total number of prime factors with multiplicity) that g(s) depends
   solely on Omega(s):
   - For Omega(s) = 1 (primes), g(s) = 0.
   - For any integer s with Omega(s) = m, any divisor d | s with 1 < d < s satisfies 1 <= Omega(d) <= m - 1.
   - Furthermore, because prime factors can be removed one at a time, for EVERY j in {1, ..., m - 1}, there
     exists at least one proper divisor d | s with Omega(d) = j.
   - By induction, if g(d) = G(Omega(d)) for all Omega(d) < m, then:
       V(s) = { G(1), G(2), ..., G(m - 1) },
     which depends exclusively on m.
   - Hence, g(s) = G(m) is identical for all integers s with Omega(s) = m.
   For n = 10^7, the maximum number of prime factors is floor(log2(10^7)) = 23.
   Evaluating G(m) for m = 1..23 yields max G(m) = G(23) = 42 < 64.

3. Counting Omega(s) up to n = 10^7:
   Using a prime sieve up to n, we tally Omega(s) for 2 <= s <= n by adding 1 at multiples of p^k for each prime p.
   In NumPy, this runs in ~1.4 seconds. We map the Omega counts to counts of each Grundy value v in [0, 63].

4. Walsh-Hadamard Transform (FWHT) for k Piles:
   A configuration (s_1, ..., s_k) is a losing position for the first player if and only if:
     g(s_1) ^ ... ^ g(s_k) = 0.
   The number of such sequences is the coefficient of x^0 in the k-th XOR-convolution power of the distribution
   polynomial P(x) = sum_{v=0}^{63} c_v x^v.
   Because M = 987654321 is odd, gcd(64, M) = 1, so the Fast Walsh-Hadamard Transform (FWHT) of size 64 is
   fully invertible modulo M.
   We transform P modulo M, raise each pointwise entry to power k mod M, inverse-transform, and subtract the
   number of losing positions from (n - 1)^k mod M to obtain f(n, k) mod M.
"""

import unittest
import numpy as np
from util.utils import timeit


class Problem550:
    def __init__(self, n: int = 10_000_000, k: int = 1_000_000_000_000, mod: int = 987654321):
        self.n = n
        self.k = k
        self.mod = mod

    @staticmethod
    def compute_grundy_by_omega(max_omega: int = 30) -> list[int]:
        """Compute Grundy values G(m) for Omega = 1..max_omega."""
        G = [0] * (max_omega + 1)
        V = set()
        for om in range(1, max_omega + 1):
            moves = set()
            V_list = list(V)
            for i in range(len(V_list)):
                for j in range(i, len(V_list)):
                    moves.add(V_list[i] ^ V_list[j])
            mex = 0
            while mex in moves:
                mex += 1
            G[om] = mex
            V.add(mex)
        return G

    @staticmethod
    def fwht_mod(a: list[int], mod: int) -> list[int]:
        """In-place Fast Walsh-Hadamard Transform modulo mod."""
        a = list(a)
        h = 1
        sz = len(a)
        while h < sz:
            for i in range(0, sz, h * 2):
                for j in range(i, i + h):
                    x = a[j]
                    y = a[j + h]
                    a[j] = (x + y) % mod
                    a[j + h] = (x - y) % mod
            h *= 2
        return a

    @classmethod
    def ifwht_mod(cls, a: list[int], mod: int) -> list[int]:
        """Inverse Fast Walsh-Hadamard Transform modulo mod."""
        sz = len(a)
        inv_sz = pow(sz, -1, mod)
        a = cls.fwht_mod(a, mod)
        return [(x * inv_sz) % mod for x in a]

    def compute_f(self, n: int, k: int, mod: int) -> int:
        """Compute f(n, k) mod mod."""
        # Find maximum omega for n
        max_omega = int(np.log2(n)) + 1
        G = self.compute_grundy_by_omega(max(max_omega, 5))

        # Sieve primes up to n
        is_prime = np.ones(n + 1, dtype=bool)
        is_prime[0:2] = False
        for p in range(2, int(n**0.5) + 1):
            if is_prime[p]:
                is_prime[p * p : n + 1 : p] = False

        primes = np.nonzero(is_prime)[0]

        # Sieve Omega(s) for 2 <= s <= n
        omega = np.zeros(n + 1, dtype=np.int8)
        for p in primes:
            pk = int(p)
            while pk <= n:
                omega[pk::pk] += 1
                pk *= int(p)

        omega_counts = np.bincount(omega[2:])

        # Distribution of Grundy values
        # Since max Grundy value for Omega <= 23 is 42, length 64 is sufficient
        L = 64
        poly = [0] * L
        for om, count in enumerate(omega_counts):
            if om > 0 and count > 0:
                g_val = G[om]
                poly[g_val] = (poly[g_val] + int(count)) % mod

        # FWHT to compute k-th XOR-convolution power
        A = self.fwht_mod(poly, mod)
        A_k = [pow(x, k, mod) for x in A]
        res = self.ifwht_mod(A_k, mod)

        losing = res[0]
        total = pow(n - 1, k, mod)
        winning = (total - losing) % mod
        return winning

    @timeit
    def solve(self) -> int:
        return self.compute_f(self.n, self.k, self.mod)


class Solution550(unittest.TestCase):
    def setUp(self):
        self.problem = Problem550()

    def test_sample(self):
        self.assertEqual(40085, self.problem.compute_f(10, 5, 987654321))

    def test_solution(self):
        self.assertEqual(328104836, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
