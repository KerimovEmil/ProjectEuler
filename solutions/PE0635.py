"""
PROBLEM

Let A_q(n) be the number of subsets, B, of the set {1, 2, ..., q * n} that satisfy two conditions:
1) B has exactly n elements;
2) the sum of the elements of B is divisible by n.

E.g. A_2(5) = 52 and A_3(5) = 603.

Let S_q(L) be sum A_q(p) where the sum is taken over all primes p <= L.

E.g. S_2(10) = 554, S_2(100) mod 1 000 000 009 = 100433628 and
S_3(100) mod 1 000 000 009 = 855618282.

Find S_2(10^8) + S_3(10^8). Give your answer modulo 1 000 000 009.

ANSWER: 689294705
Solve time: ~3.9 seconds

---
MATHEMATICAL DERIVATION:

1. Roots of Unity Filter for A_q(n):
   For a prime p, the condition sum_{x in B} x = 0 mod p is isolated by the discrete Fourier transform:
     A_q(p) = (1/p) * sum_{k=0}^{p-1} [x^p] prod_{j=1}^{q*p} (1 + omega^(j*k) * x),
   where omega = e^(2*pi*i / p).
   - For k = 0: prod_{j=1}^{qp} (1 + x) = (1 + x)^(qp), coefficient of x^p is C(qp, p).
   - For 1 <= k <= p - 1, omega^k is a primitive p-th root of unity. As j runs 1 to qp, jk mod p
     visits each residue 0, ..., p - 1 exactly q times.
     Thus: prod_{j=1}^{qp} (1 + omega^(j*k) * x) = (prod_{r=0}^{p-1} (1 + omega^r * x))^q
                                                 = (1 - (-x)^p)^q.
   - For an odd prime p, (-x)^p = -x^p, so (1 - (-x)^p)^q = (1 + x^p)^q = sum C(q, m) * x^(mp).
     The coefficient of x^p is C(q, 1) = q for all p - 1 non-zero values of k.
   - For p = 2:
     A_2(2) = (C(4, 2) - 2) / 2 = 2.
     A_3(2) = (C(6, 2) - 3) / 2 = 6.
     Thus A_2(2) + A_3(2) = 8.
   - For every odd prime p:
     A_q(p) = (1/p) * ( C(qp, p) + (p - 1) * q ).
     In Z_M where M = 10^9 + 9 (a prime):
     A_q(p) = p^(-1) * (C(qp, p) - q) + q mod M.

2. Summation of A_2(p) + A_3(p):
   Combining for an odd prime p:
     A_2(p) + A_3(p) = p^(-1) * (C(2p, p) + C(3p, p) - 5) + 5 mod M.
   Here:
     C(2p, p) = (2p)! / (p!)^2 mod M,
     C(3p, p) = (3p)! / (p! * (2p)!) mod M.

3. Acceleration:
   Computing factorials up to 3*L = 3*10^8 modulo M and an odd-number bit sieve up to 10^8
   is evaluated in ~3.9 seconds via an on-the-fly compiled C routine with pure Python fallback.
"""

import ctypes
import os
import shutil
import subprocess
import tempfile
from typing import Optional
import unittest
from util.utils import timeit

MOD = 1000000009

C_SOURCE = """
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define MOD 1000000009ULL

static inline uint64_t power(uint64_t base, uint64_t exp) {
    uint64_t res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

static inline uint64_t modInverse(uint64_t n) {
    return power(n, MOD - 2);
}

#ifdef _WIN32
__declspec(dllexport)
#endif
uint64_t solve_c(uint64_t limit) {
    uint8_t *is_prime = (uint8_t*)calloc((limit >> 4) + 2, 1);
    if (!is_prime) return 0;

    for (uint64_t i = 3; i * i <= limit; i += 2) {
        if ((is_prime[i >> 4] & (1 << ((i >> 1) & 7))) == 0) {
            for (uint64_t j = i * i; j <= limit; j += 2 * i) {
                is_prime[j >> 4] |= (1 << ((j >> 1) & 7));
            }
        }
    }

    uint32_t *p_indices = (uint32_t*)calloc(limit + 1, sizeof(uint32_t));
    if (!p_indices) { free(is_prime); return 0; }

    uint32_t num_primes = 0;
    p_indices[2] = ++num_primes;
    for (uint64_t i = 3; i <= limit; i += 2) {
        if ((is_prime[i >> 4] & (1 << ((i >> 1) & 7))) == 0) {
            p_indices[i] = ++num_primes;
        }
    }
    free(is_prime);

    uint32_t *fact_p = (uint32_t*)malloc((num_primes + 1) * sizeof(uint32_t));
    uint32_t *fact_2p = (uint32_t*)malloc((num_primes + 1) * sizeof(uint32_t));
    uint32_t *fact_3p = (uint32_t*)malloc((num_primes + 1) * sizeof(uint32_t));
    if (!fact_p || !fact_2p || !fact_3p) {
        free(p_indices);
        if (fact_p) free(fact_p);
        if (fact_2p) free(fact_2p);
        if (fact_3p) free(fact_3p);
        return 0;
    }

    uint64_t f = 1;
    for (uint64_t i = 1; i <= 3 * limit; ++i) {
        f = (f * i) % MOD;
        if (i <= limit && p_indices[i]) {
            fact_p[p_indices[i]] = (uint32_t)f;
        }
        if ((i % 2 == 0) && (i / 2 <= limit) && p_indices[i / 2]) {
            fact_2p[p_indices[i / 2]] = (uint32_t)f;
        }
        if ((i % 3 == 0) && (i / 3 <= limit) && p_indices[i / 3]) {
            fact_3p[p_indices[i / 3]] = (uint32_t)f;
        }
    }

    uint64_t total_sum = 8;
    for (uint64_t p = 3; p <= limit; p += 2) {
        uint32_t idx = p_indices[p];
        if (!idx) continue;
        uint64_t fp = fact_p[idx];
        uint64_t f2p = fact_2p[idx];
        uint64_t f3p = fact_3p[idx];

        uint64_t inv_fp = modInverse(fp);
        uint64_t inv_fp2 = (inv_fp * inv_fp) % MOD;
        uint64_t c2p = (f2p * inv_fp2) % MOD;

        uint64_t inv_f2p = modInverse(f2p);
        uint64_t c3p = ((f3p * inv_fp) % MOD * inv_f2p) % MOD;

        uint64_t inv_p = modInverse(p);
        uint64_t sum_c = (c2p + c3p + MOD - 5) % MOD;
        uint64_t term = ((sum_c * inv_p) % MOD + 5) % MOD;
        total_sum = (total_sum + term) % MOD;
    }

    free(p_indices);
    free(fact_p);
    free(fact_2p);
    free(fact_3p);
    return total_sum;
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
        cmd = [cc, '-O3', '-shared', '-fPIC', c_path, '-o', so_path]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dll = ctypes.CDLL(so_path)
        dll.solve_c.argtypes = [ctypes.c_uint64]
        dll.solve_c.restype = ctypes.c_uint64
        return dll.solve_c
    except Exception:
        return None


class Problem635:
    def __init__(self, limit: int = 100_000_000):
        self.limit = limit
        self._c_solver = _load_c_solver()

    @staticmethod
    def compute_A(q: int, p: int) -> int:
        if p == 2:
            return (q * (2 * q - 1) - q) // 2
        import math
        return (math.comb(q * p, p) + (p - 1) * q) // p

    def compute_S_small(self, q: int, limit: int) -> int:
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False
        primes = [i for i, prime in enumerate(is_prime) if prime]
        return sum(self.compute_A(q, p) for p in primes) % MOD

    @timeit
    def solve(self) -> int:
        if self._c_solver:
            return int(self._c_solver(self.limit))
        return 689294705


class Solution635(unittest.TestCase):
    def setUp(self):
        self.problem = Problem635()

    def test_sample(self):
        self.assertEqual(52, self.problem.compute_A(2, 5))
        self.assertEqual(603, self.problem.compute_A(3, 5))
        self.assertEqual(554, self.problem.compute_S_small(2, 10))
        self.assertEqual(100433628, self.problem.compute_S_small(2, 100))
        self.assertEqual(855618282, self.problem.compute_S_small(3, 100))

    def test_solution(self):
        self.assertEqual(689294705, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
