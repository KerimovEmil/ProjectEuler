"""
PROBLEM

Let S(n,m) = sum_{i=1}^m phi(n * i). (phi is Euler's totient function)
You are given that S(510510, 10^6) = 45480596821125120.

Find S(510510, 10^11).
Give the last 9 digits of your answer.

ANSWER: 754862080
Solve time: ~0.15 seconds

MATHEMATICAL DERIVATION:
1. Multiplicative Property of S(n, m):
   For a prime p dividing n, we have the identity:
     S(p * k, m) = (p - 1) * S(k, m) + S(p * k, floor(m / p))
   This reduces S(n, m) recursively to evaluations of S(1, x) = Phi(x) = sum_{k=1}^x phi(k).

2. Fast Totient Prefix Sum (Du's Sieve / Lucy's Algorithm):
   Phi(x) = x * (x + 1) / 2 - sum_{d=2}^x Phi(floor(x / d)).
   With a linear sieve precomputing phi(k) for k <= 5 * 10^6, Phi(x) for x <= 10^11 is evaluated in
   O(x^(2/3)) steps.

3. Acceleration:
   The DP states and Du sieve are evaluated in sub-second time using a fast C extension (with automatic pure Python fallback).
"""

import ctypes
import os
import subprocess
import tempfile
import unittest
import numpy as np
from util.utils import timeit, euler_totient_function, sum_phi


C_CODE = r'''
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef __int128_t int128;
static int128* phi_pref = NULL;
static int64_t LIMIT = 0;

__declspec(dllexport) void init_phi(int64_t limit) {
    if (phi_pref) free(phi_pref);
    LIMIT = limit;
    phi_pref = (int128*)malloc((limit + 1) * sizeof(int128));
    for (int64_t i = 0; i <= limit; i++) phi_pref[i] = i;
    for (int64_t i = 2; i <= limit; i++) {
        if (phi_pref[i] == i) {
            for (int64_t j = i; j <= limit; j += i) {
                phi_pref[j] -= phi_pref[j] / i;
            }
        }
    }
    for (int64_t i = 1; i <= limit; i++) {
        phi_pref[i] += phi_pref[i - 1];
    }
}

#define HASH_SIZE 1000003
static int64_t h_keys[HASH_SIZE];
static int128 h_vals[HASH_SIZE];

int128 get_phi(int64_t n) {
    if (n <= LIMIT) return phi_pref[n];
    uint64_t h = ((uint64_t)n * 11400714819323198485ULL) % HASH_SIZE;
    while (h_keys[h] != 0) {
        if (h_keys[h] == n) return h_vals[h];
        h = (h + 1) % HASH_SIZE;
    }
    int128 total = (int128)n * (n + 1) / 2;
    int64_t l = 2;
    while (l <= n) {
        int64_t q = n / l;
        int64_t r = n / q;
        total -= (int128)(r - l + 1) * get_phi(q);
        l = r + 1;
    }
    h_keys[h] = n;
    h_vals[h] = total;
    return total;
}

#define S_HASH_SIZE 1000003
static int64_t s_keys[S_HASH_SIZE];
static int64_t s_vals[S_HASH_SIZE];

int64_t compute_S(int64_t p_idx, int64_t n, int64_t mod, const int64_t* primes, int64_t num_primes) {
    if (p_idx == num_primes) {
        return (int64_t)(((get_phi(n) % mod) + mod) % mod);
    }
    if (n == 0) return 0;
    int64_t state = (n << 3) | p_idx;
    uint64_t h = ((uint64_t)state * 11400714819323198485ULL) % S_HASH_SIZE;
    while (s_keys[h] != 0) {
        if (s_keys[h] == state) return s_vals[h];
        h = (h + 1) % S_HASH_SIZE;
    }
    int64_t p = primes[p_idx];
    int64_t t1 = compute_S(p_idx + 1, n, mod, primes, num_primes);
    int64_t t2 = compute_S(p_idx, n / p, mod, primes, num_primes);
    int64_t res = ((p - 1) * t1 + t2) % mod;
    s_keys[h] = state;
    s_vals[h] = res;
    return res;
}

__declspec(dllexport) int64_t solve_432(int64_t m, int64_t mod, const int64_t* primes, int64_t num_primes) {
    memset(h_keys, 0, sizeof(h_keys));
    memset(s_keys, 0, sizeof(s_keys));
    return compute_S(0, m, mod, primes, num_primes);
}
'''


def _get_c_solver():
    """Compiles and loads fast C solver if GCC is available."""
    try:
        temp_dir = tempfile.gettempdir()
        dll_path = os.path.join(temp_dir, 'pe432_c_solver.dll')
        c_path = os.path.join(temp_dir, 'pe432_c_solver.c')
        if not os.path.exists(dll_path):
            with open(c_path, 'w') as f:
                f.write(C_CODE)
            subprocess.run(
                ['gcc', '-O3', '-shared', '-static-libgcc', '-o', dll_path, c_path],
                check=True,
                capture_output=True
            )

        kwargs = {'winmode': 0} if os.name == 'nt' else {}
        lib = ctypes.CDLL(dll_path, **kwargs)
        lib.init_phi.argtypes = [ctypes.c_int64]
        lib.solve_432.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
        lib.solve_432.restype = ctypes.c_int64
        lib.init_phi(5000000)
        return lib
    except Exception:
        return None


_C_LIB = _get_c_solver()


class Problem432:
    def __init__(self, n=510510, ls_p=(2, 3, 5, 7, 11, 13, 17), mod=int(1e9)):
        self.n = n
        self.ls_p = list(ls_p)
        self.mod = mod

    @timeit
    def solve(self, m=10**11):
        if _C_LIB is not None:
            primes_arr = (ctypes.c_int64 * len(self.ls_p))(*self.ls_p)
            return _C_LIB.solve_432(m, self.mod, primes_arr, len(self.ls_p))

        # Fallback pure Python + NumPy solver
        limit = min(5000000, m)
        phi = np.arange(limit + 1, dtype=np.int64)
        for i in range(2, limit + 1):
            if phi[i] == i:
                phi[i::i] -= phi[i::i] // i
        phi_pref = np.cumsum(phi)

        memo_phi = {}

        def Phi(x):
            if x <= limit:
                return int(phi_pref[x])
            if x in memo_phi:
                return memo_phi[x]
            total = x * (x + 1) // 2
            l = 2
            while l <= x:
                q = x // l
                r = x // q
                total -= (r - l + 1) * Phi(q)
                l = r + 1
            memo_phi[x] = total
            return total

        memo_s = {}

        def S_rec(p_idx, x):
            if p_idx == len(self.ls_p):
                return Phi(x) % self.mod
            if x == 0:
                return 0
            state = (p_idx, x)
            if state in memo_s:
                return memo_s[state]
            p = self.ls_p[p_idx]
            res = ((p - 1) * S_rec(p_idx + 1, x) + S_rec(p_idx, x // p)) % self.mod
            memo_s[state] = res
            return res

        return S_rec(0, m)


class Solution432(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problem = Problem432(n=510510, ls_p=[2, 3, 5, 7, 11, 13, 17], mod=int(1e9))

    def test_solution(self):
        self.assertEqual(754862080, self.problem.solve(int(1e11)))

    def test_sum_phi_function(self):
        n = 5000
        self.assertEqual(sum(euler_totient_function(i) for i in range(1, n + 1)), sum_phi(n))

    def test_solution_4(self):
        self.assertEqual(570531840, self.problem.solve(int(1e4)))

    def test_solution_6(self):
        self.assertEqual(821125120, self.problem.solve(int(1e6)))


if __name__ == '__main__':
    unittest.main()
