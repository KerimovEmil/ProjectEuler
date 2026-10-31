"""
PROBLEM

In the context of formal languages, any finite sequence of letters of a given alphabet Sigma
is called a word over Sigma. We call a word incomplete if it does not contain every letter of Sigma.

For example, using the alphabet Sigma = {a, b, c}, 'ab', 'abab' and '' (the empty word) are
incomplete words over Sigma, while 'abac' is a complete word over Sigma.

Given an alphabet Sigma of alpha letters, we define I(alpha, n) to be the number of incomplete words
over Sigma with a length not exceeding n.
For example, I(3, 0) = 1, I(3, 2) = 13 and I(3, 4) = 79.

Find I(10^7, 10^12). Give your answer modulo 1 000 000 007.

ANSWER: 219493139
Solve time: ~0.85 seconds

---
MATHEMATICAL DERIVATION:

1. Formal Statement & Principle of Inclusion-Exclusion (PIE):
   Let Sigma be an alphabet with |Sigma| = alpha.
   A word w of length L is incomplete if there exists at least one letter x in Sigma that does not appear in w.
   By the Principle of Inclusion-Exclusion:
     Number of words of length L avoiding at least one letter is:
       sum_{k=1}^alpha (-1)^(k-1) * binom(alpha, k) * (alpha - k)^L.

2. Summing Over Lengths 0 <= L <= n:
   Summing over all lengths 0 <= L <= n:
     I(alpha, n) = sum_{k=1}^alpha (-1)^(k-1) * binom(alpha, k) * S(alpha - k, n),
   where S(m, n) = sum_{L=0}^n m^L.
   Evaluating S(m, n):
   - For m = 0: S(0, n) = 0^0 + 0^1 + ... = 1 (accounting for the empty word).
   - For m = 1: S(1, n) = n + 1.
   - For m >= 2: S(m, n) = (m^(n+1) - 1) / (m - 1).

3. Index Substitution:
   Let m = alpha - k. As k ranges from 1 to alpha, m ranges from alpha - 1 down to 0:
     I(alpha, n) = sum_{m=0}^{alpha - 1} (-1)^(alpha - m - 1) * binom(alpha, m) * S(m, n) mod M,
   where M = 10^9 + 7.

4. Modular Arithmetic & Fast Sieve:
   - Since M is prime, by Fermat's Little Theorem:
       m^(n+1) = m^((n+1) mod (M - 1)) mod M.
   - For alpha = 10^7, m^(n+1) mod M is completely multiplicative in m, so we compute all powers
     up to alpha in O(alpha) time via an Euler linear sieve.
   - Factorials and inverse factorials up to alpha are precomputed in O(alpha) time.
   - Inverses of (m - 1) for 2 <= m <= alpha are computed in O(alpha) using linear recurrence:
       inv[i] = -(M // i) * inv[M % i] mod M.
   - The entire calculation runs in O(alpha) time and O(alpha) space (~0.85 seconds via C extension).
"""

import ctypes
import os
import shutil
import subprocess
import tempfile
import unittest
from util.utils import timeit

MOD = 1_000_000_007

C_SOURCE = """
#include <stdlib.h>
#include <stdint.h>

static inline long long power(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = (__int128)res * base % mod;
        base = (__int128)base * base % mod;
        exp /= 2;
    }
    return res;
}

static inline long long modInverse(long long n, long long m) {
    return power(n, m - 2, m);
}

#ifdef _WIN32
__declspec(dllexport)
#endif
long long solve_c(int alpha, long long n, long long MOD) {
    long long E = (n + 1) % (MOD - 1);
    
    int *primes = (int *)malloc((alpha + 1) * sizeof(int));
    int *min_prime = (int *)calloc((alpha + 1), sizeof(int));
    int *pow_E = (int *)malloc((alpha + 1) * sizeof(int));
    int *fact = (int *)malloc((alpha + 1) * sizeof(int));
    int *inv_fact = (int *)malloc((alpha + 1) * sizeof(int));
    int *inv_m = (int *)malloc((alpha + 1) * sizeof(int));
    
    if (!primes || !min_prime || !pow_E || !fact || !inv_fact || !inv_m) {
        if (primes) free(primes);
        if (min_prime) free(min_prime);
        if (pow_E) free(pow_E);
        if (fact) free(fact);
        if (inv_fact) free(inv_fact);
        if (inv_m) free(inv_m);
        return 0;
    }
    
    int num_primes = 0;
    pow_E[0] = 0;
    pow_E[1] = 1;
    
    for (int i = 2; i <= alpha; i++) {
        if (!min_prime[i]) {
            min_prime[i] = i;
            primes[num_primes++] = i;
            pow_E[i] = (int)power(i, E, MOD);
        }
        for (int j = 0; j < num_primes; j++) {
            int p = primes[j];
            if (p > min_prime[i] || (long long)i * p > alpha) break;
            min_prime[i * p] = p;
            pow_E[i * p] = (int)((long long)pow_E[i] * pow_E[p] % MOD);
        }
    }
    
    fact[0] = 1;
    for (int i = 1; i <= alpha; i++) fact[i] = (int)((long long)fact[i - 1] * i % MOD);
    inv_fact[alpha] = (int)modInverse(fact[alpha], MOD);
    for (int i = alpha - 1; i >= 0; i--) inv_fact[i] = (int)((long long)inv_fact[i + 1] * (i + 1) % MOD);
    
    inv_m[1] = 1;
    for (int i = 2; i <= alpha; i++) inv_m[i] = (int)((long long)(MOD - MOD / i) * inv_m[MOD % i] % MOD);
    
    long long total = 0;
    for (int m = 0; m < alpha; m++) {
        long long Sm = 0;
        if (m == 0) Sm = 1;
        else if (m == 1) Sm = (n + 1) % MOD;
        else {
            long long num = (pow_E[m] - 1 + MOD) % MOD;
            Sm = (long long)num * inv_m[m - 1] % MOD;
        }
        long long binom = (long long)fact[alpha] * inv_fact[m] % MOD * inv_fact[alpha - m] % MOD;
        long long term = binom * Sm % MOD;
        if ((alpha - m - 1) % 2 == 1) total = (total - term + MOD) % MOD;
        else total = (total + term) % MOD;
    }
    
    free(primes);
    free(min_prime);
    free(pow_E);
    free(fact);
    free(inv_fact);
    free(inv_m);
    
    return total;
}
"""


def _load_c_solver():
    cc = shutil.which('gcc') or shutil.which('clang')
    if not cc:
        return None
    try:
        temp_dir = tempfile.mkdtemp()
        c_path = os.path.join(temp_dir, 'solver.c')
        ext = '.dll' if os.name == 'nt' else '.so'
        so_path = os.path.join(temp_dir, f'libsolver{ext}')
        with open(c_path, 'w', encoding='utf-8') as f:
            f.write(C_SOURCE)
        cmd = [cc, '-O3', '-shared', '-static', '-fPIC', c_path, '-o', so_path]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dll = ctypes.CDLL(so_path)
        dll.solve_c.argtypes = [ctypes.c_int, ctypes.c_longlong, ctypes.c_longlong]
        dll.solve_c.restype = ctypes.c_longlong
        return dll.solve_c
    except Exception:
        return None


class Problem657:
    def __init__(self, alpha: int = 10_000_000, n: int = 1_000_000_000_000, mod: int = MOD):
        self.alpha = alpha
        self.n = n
        self.mod = mod
        self._c_solver = _load_c_solver()

    def compute_I(self, alpha: int, n: int) -> int:
        if self._c_solver:
            return int(self._c_solver(alpha, n, self.mod))

        # Pure Python fallback for smaller inputs
        mod = self.mod
        fact = [1] * (alpha + 1)
        for i in range(1, alpha + 1):
            fact[i] = fact[i - 1] * i % mod
        inv_fact = [1] * (alpha + 1)
        inv_fact[alpha] = pow(fact[alpha], mod - 2, mod)
        for i in range(alpha - 1, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

        total = 0
        for m in range(alpha):
            if m == 0:
                Sm = 1
            elif m == 1:
                Sm = (n + 1) % mod
            else:
                num = (pow(m, n + 1, mod) - 1) % mod
                Sm = num * pow(m - 1, mod - 2, mod) % mod
            binom = fact[alpha] * inv_fact[m] % mod * inv_fact[alpha - m] % mod
            term = binom * Sm % mod
            if (alpha - m - 1) % 2 == 1:
                total = (total - term + mod) % mod
            else:
                total = (total + term) % mod
        return total

    @timeit
    def solve(self) -> int:
        return self.compute_I(self.alpha, self.n)


class Solution657(unittest.TestCase):
    def setUp(self):
        self.problem = Problem657()

    def test_sample(self):
        self.assertEqual(1, self.problem.compute_I(3, 0))
        self.assertEqual(13, self.problem.compute_I(3, 2))
        self.assertEqual(79, self.problem.compute_I(3, 4))

    def test_solution(self):
        self.assertEqual(219493139, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
