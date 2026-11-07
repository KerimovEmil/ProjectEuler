r"""
PROBLEM

A k-bounded partition of a positive integer N is a way of writing N as a sum of positive integers that do not exceed k.

A balanceable partition is a partition that can be split into two sub-multisets of equal sums.

For example, 3 + 2 + 2 + 2 + 2 + 1 is a balanceable 3-bounded partition of 12, since 3 + 2 + 1 = 2 + 2 + 2 = 6.
Conversely, 3 + 3 + 3 + 3 is a 3-bounded partition of 12 that is not balanceable.

Let f(k) be the smallest positive integer N such that all k-bounded partitions of N are balanceable.
For example, f(3) = 12 and f(6) = 120.

Find f(10^8). Give your answer modulo 1,000,000,007.

ANSWER: 83985379
Solve time: ~0.05 seconds (pure Python: ~4.5 seconds)

---
MATHEMATICAL DERIVATION:

1. Divisibility Requirement:
   For every integer d with 1 <= d <= k, consider the partition consisting entirely of parts equal to d:
     N = d + d + ... + d = (N / d) * d.
   For this partition to be balanceable, we must be able to partition these parts into two sets of equal sum N/2.
   Since each part is d, any subset sum is a multiple of d.
   Thus N/2 must be an integer multiple of d for every d in {1, 2, ..., k}.
   Consequently, lcm(1, 2, ..., k) must divide N/2, which implies:
     N >= 2 * lcm(1, 2, ..., k).

2. Sufficiency:
   It is a known combinatorial result that for N = 2 * lcm(1, 2, ..., k), every k-bounded partition
   is indeed balanceable.
   Hence f(k) = 2 * lcm(1, 2, ..., k).
   Verified against given values:
     f(3) = 2 * lcm(1, 2, 3) = 2 * 6 = 12.
     f(6) = 2 * lcm(1, 2, 3, 4, 5, 6) = 2 * 60 = 120.

3. Computation for k = 10^8 modulo 10^9 + 7:
   The prime factorization of lcm(1, 2, ..., k) is:
     lcm(1, 2, ..., k) = \prod_{p <= k} p^{\lfloor \log_p k \rfloor}.
   For primes p > sqrt(k) = 10^4, the exponent \lfloor \log_p k \rfloor is exactly 1.
   For primes p <= 10^4, the exponent is \lfloor \log_p k \rfloor.
   We sieve primes up to 10^8, compute the product of prime powers modulo 1,000,000,007,
   and multiply by 2.
"""

import ctypes
import math
import os
import shutil
import subprocess
import tempfile
import unittest

from util.utils import timeit

MOD = 1000000007

C_SOURCE = """
#include <stdint.h>
#include <stdlib.h>

#ifdef _WIN32
__declspec(dllexport)
#endif
int64_t solve_c(int64_t n, int64_t mod) {
    if (n < 2) return 0;
    int64_t max_i = (n - 1) / 2;
    uint8_t *sieve = (uint8_t *)calloc(max_i + 1, sizeof(uint8_t));
    if (!sieve) return -1;

    for (int64_t i = 1; (2 * i + 1) * (2 * i + 1) <= n; i++) {
        if (!sieve[i]) {
            int64_t p = 2 * i + 1;
            int64_t start = (p * p - 1) / 2;
            for (int64_t j = start; j <= max_i; j += p) {
                sieve[j] = 1;
            }
        }
    }

    int64_t ans = 2;
    int64_t p2 = 1;
    while (p2 * 2 <= n) p2 *= 2;
    ans = (int64_t)(((uint64_t)ans * (p2 % mod)) % mod);

    for (int64_t i = 1; i <= max_i; i++) {
        if (!sieve[i]) {
            int64_t p = 2 * i + 1;
            if (p * p <= n) {
                int64_t pw = p;
                while (pw * p <= n) pw *= p;
                ans = (int64_t)(((uint64_t)ans * (pw % mod)) % mod);
            } else {
                ans = (int64_t)(((uint64_t)ans * (p % mod)) % mod);
            }
        }
    }
    free(sieve);
    return ans;
}
"""

_COMPILED_C_SOLVER = None


def _load_c_solver():
    global _COMPILED_C_SOLVER
    if _COMPILED_C_SOLVER is not None:
        return _COMPILED_C_SOLVER
    cc = shutil.which("gcc") or shutil.which("clang")
    if not cc:
        return None
    try:
        temp_dir = tempfile.mkdtemp()
        c_path = os.path.join(temp_dir, "solver772.c")
        ext = ".dll" if os.name == "nt" else ".so"
        so_path = os.path.join(temp_dir, f"libsolver772{ext}")
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(C_SOURCE)
        cmd = [cc, "-O3", "-shared", "-fPIC", c_path, "-o", so_path]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dll = ctypes.CDLL(so_path)
        dll.solve_c.argtypes = [ctypes.c_int64, ctypes.c_int64]
        dll.solve_c.restype = ctypes.c_int64
        _COMPILED_C_SOLVER = dll.solve_c
        return _COMPILED_C_SOLVER
    except Exception:
        return None


class Problem772:
    def __init__(self, limit: int = 10**8, mod: int = MOD):
        self.limit = limit
        self.mod = mod
        self._c_solver = _load_c_solver()

    def compute_f(self, k: int, mod: int = MOD) -> int:
        if k < 2:
            return 2 if k == 1 else 0

        if self._c_solver is not None:
            ans = self._c_solver(int(k), int(mod))
            if ans >= 0:
                return ans

        # Pure Python fallback
        max_i = (k - 1) // 2
        sieve = bytearray([1]) * (max_i + 1)
        for i in range(1, int(math.isqrt(k)) // 2 + 1):
            if sieve[i]:
                p = 2 * i + 1
                start = (p * p - 1) // 2
                sieve[start :: p] = bytearray(len(sieve[start :: p]))

        ans = 2
        p2 = 1
        while p2 * 2 <= k:
            p2 *= 2
        ans = (ans * p2) % mod

        for i in range(1, max_i + 1):
            if sieve[i]:
                p = 2 * i + 1
                if p * p <= k:
                    pw = p
                    while pw * p <= k:
                        pw *= p
                    ans = (ans * pw) % mod
                else:
                    ans = (ans * p) % mod
        return ans

    @timeit
    def solve(self) -> int:
        return self.compute_f(self.limit, self.mod)


class Solution772(unittest.TestCase):
    def setUp(self):
        self.problem = Problem772()

    def test_samples(self):
        self.assertEqual(12, self.problem.compute_f(3))
        self.assertEqual(120, self.problem.compute_f(6))

    def test_solution(self):
        self.assertEqual(83985379, self.problem.solve())


if __name__ == "__main__":
    unittest.main()
