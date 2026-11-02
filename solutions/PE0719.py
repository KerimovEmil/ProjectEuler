"""
PROBLEM

We define an S-number to be a natural number, n, that is a perfect square and its square root can be
obtained by splitting the decimal representation of n into 2 or more numbers then adding the numbers.

For example, 81 is an S-number because sqrt(81) = 8 + 1.
6724 is an S-number: sqrt(6724) = 6 + 72 + 4.
8281 is an S-number: sqrt(8281) = 8 + 2 + 81 = 82 + 8 + 1.
9801 is an S-number: sqrt(9801) = 98 + 0 + 1.

Further we define T(N) to be the sum of all S numbers n <= N. You are given T(10^4) = 41333.

Find T(10^12).

ANSWER: 128088830547982
Solve time: ~0.10 seconds

---
MATHEMATICAL DERIVATION:

1. Search Space Reduction:
   Since n <= N = 10^12 is a perfect square, we can iterate over its square root s = sqrt(n).
   For N = 10^12, 2 <= s <= 10^6. Thus n = s^2 and s has at most 6 digits.

2. Modulo 9 Filter:
   Let d_1, d_2, ..., d_k be a valid split of the decimal representation of n.
   Because any decimal partition of an integer preserves its sum modulo 9:
     n = sum_{i=1}^k d_i mod 9.
   Since the partition sums to s, we have:
     n = s mod 9.
   Substituting n = s^2:
     s^2 = s mod 9  ==>  s(s - 1) = 0 mod 9.
   Since gcd(s, s - 1) = 1, 9 must divide either s or s - 1:
     s = 0 mod 9  or  s = 1 mod 9.
   This single modular constraint eliminates 7/9 (~77.8%) of all candidates, leaving only ~222,222
   values of s to test up to 10^6.

3. Recursive Suffix Splitting with Branch-and-Bound:
   For each candidate s:
   - To ensure at least 2 parts, the first split cannot take the entire number.
   - Subproblems check if `rem` can be split into parts summing to `target`:
       if num < target: return False
       if num == target: return True
       for suffix of length 1, 2, ...:
         if suffix <= target and can_split(num // 10^k, target - suffix):
           return True
   - Pruning `suffix <= target` and `num >= target` stops branches almost immediately.

4. Performance:
   Evaluating T(10^12) takes ~0.10 seconds via compiled C routine with pure Python fallback.
"""

import ctypes
import math
import os
import shutil
import subprocess
import tempfile
import unittest
from util.utils import timeit

C_SOURCE = """
#include <stdint.h>
#include <stdbool.h>

static inline bool can_split(uint64_t num, uint64_t target) {
    if (num < target) return false;
    if (num == target) return true;

    uint64_t mod = 10;
    while (mod <= num) {
        uint64_t part = num % mod;
        if (part <= target) {
            if (can_split(num / mod, target - part)) return true;
        }
        mod *= 10;
    }
    return false;
}

static inline bool check_s(uint64_t s) {
    uint64_t num = s * s;
    uint64_t mod = 10;
    while (mod <= num) {
        uint64_t part = num % mod;
        if (part <= s) {
            if (can_split(num / mod, s - part)) return true;
        }
        mod *= 10;
    }
    return false;
}

#ifdef _WIN32
__declspec(dllexport)
#endif
uint64_t solve_c(uint64_t limit_s) {
    uint64_t total = 0;
    for (uint64_t s = 2; s <= limit_s; s++) {
        uint64_t rem = s % 9;
        if (rem != 0 && rem != 1) continue;
        if (check_s(s)) {
            total += s * s;
        }
    }
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
        dll.solve_c.argtypes = [ctypes.c_uint64]
        dll.solve_c.restype = ctypes.c_uint64
        return dll.solve_c
    except Exception:
        return None


class Problem719:
    def __init__(self, limit: int = 10**12):
        self.limit = limit
        self.limit_s = math.isqrt(limit)
        self._c_solver = _load_c_solver()

    @staticmethod
    def _can_split(num: int, target: int) -> bool:
        if num < target:
            return False
        if num == target:
            return True
        mod = 10
        while mod <= num:
            part = num % mod
            if part <= target:
                if Problem719._can_split(num // mod, target - part):
                    return True
            mod *= 10
        return False

    @staticmethod
    def is_s_number(s: int) -> bool:
        num = s * s
        mod = 10
        while mod <= num:
            part = num % mod
            if part <= s:
                if Problem719._can_split(num // mod, s - part):
                    return True
            mod *= 10
        return False

    def compute_T(self, limit: int) -> int:
        limit_s = math.isqrt(limit)
        if self._c_solver:
            return int(self._c_solver(limit_s))

        # Pure Python fallback
        total = 0
        for s in range(2, limit_s + 1):
            rem = s % 9
            if rem != 0 and rem != 1:
                continue
            if self.is_s_number(s):
                total += s * s
        return total

    @timeit
    def solve(self) -> int:
        return self.compute_T(self.limit)


class Solution719(unittest.TestCase):
    def setUp(self):
        self.problem = Problem719()

    def test_sample(self):
        self.assertTrue(self.problem.is_s_number(9))      # 81
        self.assertTrue(self.problem.is_s_number(82))     # 6724
        self.assertTrue(self.problem.is_s_number(91))     # 8281
        self.assertTrue(self.problem.is_s_number(99))     # 9801
        self.assertEqual(41333, self.problem.compute_T(10**4))

    def test_solution(self):
        self.assertEqual(128088830547982, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
