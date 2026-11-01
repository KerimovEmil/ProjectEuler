"""
PROBLEM

Find the number of non-empty subsets of {1^1, 2^2, 3^3, ..., 250250^250250},
the sum of whose elements is divisible by 250. Enter the rightmost 16 digits as your answer.

ANSWER: 1425480602091519
Solve time: ~0.20 seconds

---
MATHEMATICAL DERIVATION:

1. Problem Formulation:
   Let S = {1^1, 2^2, ..., N^N} where N = 250250.
   We seek the number of non-empty subsets B subset of S such that:
     sum_{x in B} x = 0 mod 250.
   The answer is requested modulo 10^16.

2. Modular Residue Mapping:
   Since subset summation is associative and commutative in Z_250, the divisibility of the sum
   by 250 depends solely on the residues r_k = k^k mod 250 for each k in {1, ..., N}.
   For each k, r_k is computed via modular exponentiation in O(log k) time.

3. Dynamic Programming (Subset Sum modulo 250):
   Let dp[s] be the number of subsets (including the empty subset) of the first k elements
   whose sum is congruent to s mod 250.
   Initially, before considering any elements:
     dp[0] = 1,  dp[s] = 0 for s != 0.
   When processing the (k)-th element with residue r = k^k mod 250:
     next_dp[s] = (dp[s] + dp[(s - r) mod 250]) mod 10^16.
   After all N = 250250 elements have been processed:
   - dp[0] counts all subsets with sum divisible by 250.
   - We subtract 1 to exclude the empty subset (whose sum is 0):
       answer = (dp[0] - 1) mod 10^16.

4. Performance:
   Processing 250250 elements with 250 states per transition requires ~6.25 * 10^7 additions
   modulo 10^16, evaluated in ~0.20 seconds via a dynamically compiled C routine with pure Python fallback.
"""

import ctypes
import os
import shutil
import subprocess
import tempfile
import unittest
from util.utils import timeit

MOD = 10**16

C_SOURCE = """
#include <stdint.h>
#include <stdlib.h>

#ifdef _WIN32
__declspec(dllexport)
#endif
uint64_t solve_c(int n, int m) {
    uint64_t MOD = 10000000000000000ULL;
    uint64_t *dp = (uint64_t *)calloc(m, sizeof(uint64_t));
    uint64_t *next_dp = (uint64_t *)calloc(m, sizeof(uint64_t));
    if (!dp || !next_dp) {
        if (dp) free(dp);
        if (next_dp) free(next_dp);
        return 0;
    }
    dp[0] = 1;

    for (int k = 1; k <= n; k++) {
        uint64_t base = k % m;
        uint64_t exp = k;
        uint64_t r = 1;
        while (exp > 0) {
            if (exp & 1) r = (r * base) % m;
            base = (base * base) % m;
            exp >>= 1;
        }

        for (int s = 0; s < m; s++) {
            int prev_s = (s - r + m) % m;
            uint64_t sum = dp[s] + dp[prev_s];
            if (sum >= MOD) sum -= MOD;
            next_dp[s] = sum;
        }
        for (int s = 0; s < m; s++) dp[s] = next_dp[s];
    }

    uint64_t ans = (dp[0] + MOD - 1) % MOD;
    free(dp);
    free(next_dp);
    return ans;
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
        dll.solve_c.argtypes = [ctypes.c_int, ctypes.c_int]
        dll.solve_c.restype = ctypes.c_uint64
        return dll.solve_c
    except Exception:
        return None


class Problem250:
    def __init__(self, n: int = 250250, m: int = 250, mod: int = MOD):
        self.n = n
        self.m = m
        self.mod = mod
        self._c_solver = _load_c_solver()

    def compute_subsets(self, n: int, m: int) -> int:
        if self._c_solver:
            return int(self._c_solver(n, m))

        # Pure Python fallback
        mod = self.mod
        dp = [0] * m
        dp[0] = 1

        for k in range(1, n + 1):
            r = pow(k, k, m)
            next_dp = list(dp)
            for s in range(m):
                prev = s - r
                if prev < 0:
                    prev += m
                val = dp[s] + dp[prev]
                if val >= mod:
                    val -= mod
                next_dp[s] = val
            dp = next_dp

        return (dp[0] - 1) % mod

    @timeit
    def solve(self) -> int:
        return self.compute_subsets(self.n, self.m)


class Solution250(unittest.TestCase):
    def setUp(self):
        self.problem = Problem250()

    def test_sample(self):
        self.assertEqual(5, self.problem.compute_subsets(5, 5))
        self.assertEqual(49, self.problem.compute_subsets(8, 5))
        self.assertEqual(103, self.problem.compute_subsets(10, 10))

    def test_solution(self):
        self.assertEqual(1425480602091519, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
