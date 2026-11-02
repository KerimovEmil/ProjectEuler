r"""
PROBLEM

Denote the average of k numbers x_1, ..., x_k by \bar{x} = (1/k) \sum_i x_i.
Their variance is defined as (1/k) \sum_i (x_i - \bar{x})^2.

Let S(n) be the sum of all quadruples of integers (a, b, c, d) satisfying 1 <= a <= b <= c <= d <= n
such that their average is exactly twice their variance.

For n = 5, there are 5 such quadruples, namely:
  (1, 1, 1, 3), (1, 1, 3, 3), (1, 2, 3, 4), (1, 3, 4, 4), (2, 2, 3, 5).

Hence S(5) = 48. You are also given S(10^3) = 37048340.

Find S(10^8). Give your answer modulo 433494437.

ANSWER: 404890862
Solve time: ~1.8 seconds

---
MATHEMATICAL DERIVATION:

1. Algebraic Condition on Average and Variance:
   For k = 4, let s = a + b + c + d.
   Average: \bar{x} = s / 4.
   Variance: \sigma^2 = (1/4) \sum x_i^2 - (s/4)^2.
   The condition \bar{x} = 2\sigma^2 expands to:
     s/4 = 2 * ((1/4) \sum x_i^2 - s^2/16)
     2s = 4 \sum x_i^2 - s^2
     4 \sum x_i^2 = s(s + 2).
   Since 4 | s(s + 2), s must be even: s = 2m.
   Then 4 \sum x_i^2 = 2m(2m + 2) = 4m(m + 1), which implies:
     \sum_{i=1}^4 x_i^2 = m(m + 1).

2. Centered Coordinates and Transformation:
   Case 1 (m even, m = 2k):
     The mean \mu = k is an integer. Let y_i = x_i - k.
     Then \sum y_i = 0 and \sum y_i^2 = 2k, so k = (1/2) \sum y_i^2 is uniquely determined!
     With y_1 <= y_2 <= y_3 <= y_4, define:
       u = y_3 + y_4 = -(y_1 + y_2) > 0,
       d_1 = y_2 - y_1 >= 0,   d_2 = y_4 - y_3 >= 0,
       with d_1 \equiv d_2 \equiv u (mod 2).
     Then:
       \sum y_i^2 = u^2 + (d_1^2 + d_2^2) / 2,   y_4 = (u + d_2) / 2.
     The constraint d = k + y_4 <= n translates to:
       2u^2 + 2u + d_1^2 + d_2^2 + 2d_2 <= 4n.
     The ordering condition y_2 <= y_3 simplifies to d_1 + d_2 <= 2u.
     The quadruple sum is s = 4k = 2 \sum y_i^2 = 2u^2 + d_1^2 + d_2^2.

   Case 2 (m odd, m = 2k + 1):
     The mean \mu = k + 0.5 is a half-integer.
     Let z_i = 2x_i - (2k + 1) be odd integers with \sum z_i = 0.
     Then \sum z_i^2 = 8k + 4 = 4m.
     Let u = z_3 + z_4 = 2U, d_1 = z_2 - z_1 = 2D_1, d_2 = z_4 - z_3 = 2D_2.
     Since z_i are odd, D_1 \not\equiv U (mod 2) and D_2 \not\equiv U (mod 2).
     The constraint d <= n becomes:
       2U^2 + 2U + D_1^2 + D_2^2 + 2D_2 <= 4n.
     The ordering condition becomes D_1 + D_2 <= 2U.
     The quadruple sum is s = 2m = 2U^2 + D_1^2 + D_2^2.

3. Closed-Form Summation over d_1 / D_1:
   For fixed u and d_2, d_1 ranges from rem to max_d_1 in steps of 2, where:
     max_d_1 = min(2u - d_2, floor(sqrt(4n - (2u^2 + 2u + d_2^2 + 2d_2)))).
   Setting J = (max_d_1 - rem) // 2 and cnt = J + 1, the inner sum \sum (2u^2 + d_2^2 + d_1^2)
   evaluates in O(1) via Faulhaber's formulas for \sum j and \sum j^2.

4. Boundary Violators (a < 1):
   a >= 1 holds for all quadruples except exactly three across both cases:
     - Case 1: y = (-1, 0, 0, 1) -> sum = 4
     - Case 2: z = (-3, 1, 1, 1) -> sum = 6
     - Case 2: z = (-1, -1, 1, 1) -> sum = 2
   Subtracting 4 + 6 + 2 = 12 yields the exact value of S(n).
"""

import ctypes
import math
import os
import shutil
import subprocess
import tempfile
import unittest
from util.utils import timeit

MOD = 433494437

C_SOURCE = """
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

static inline int64_t isqrt_i64(int64_t n) {
    if (n <= 0) return 0;
    int64_t x = (int64_t)sqrt((double)n);
    while ((x + 1) * (x + 1) <= n) x++;
    while (x * x > n) x--;
    return x;
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int64_t solve_c_omp(int64_t n, int64_t mod) {
    int64_t four_n = 4 * n;
    int64_t max_u = isqrt_i64(2 * n) + 2;
    __int128 total1 = 0;
    __int128 total2 = 0;

    // Case 1: rem = u % 2
    #pragma omp parallel for schedule(guided) reduction(+:total1)
    for (int64_t u = 1; u <= max_u; u++) {
        int64_t rem = u % 2;
        int64_t u2 = u * u;
        int64_t two_u2_plus_2u = 2 * u2 + 2 * u;
        if (two_u2_plus_2u > four_n) continue;

        int64_t cur_bound = isqrt_i64(four_n - two_u2_plus_2u);

        for (int64_t d2 = rem; d2 <= 2 * u; d2 += 2) {
            int64_t lhs_part = two_u2_plus_2u + d2 * d2 + 2 * d2;
            int64_t rem_val = four_n - lhs_part;
            if (rem_val < 0) break;

            while (cur_bound * cur_bound > rem_val) {
                cur_bound--;
            }

            int64_t max_d1 = 2 * u - d2;
            if (cur_bound < max_d1) max_d1 = cur_bound;
            if (max_d1 < rem) continue;

            int64_t J = (max_d1 - rem) / 2;
            int64_t cnt = J + 1;

            __int128 sum_j = (__int128)J * (J + 1) / 2;
            __int128 sum_j2 = (__int128)J * (J + 1) * (2 * J + 1) / 6;
            __int128 sum_d1_sq = (__int128)cnt * (rem * rem) + 4 * rem * sum_j + 4 * sum_j2;

            __int128 term = (__int128)cnt * (2 * u2 + d2 * d2) + sum_d1_sq;
            total1 += term;
        }
    }

    // Case 2: rem = 1 - (U % 2)
    #pragma omp parallel for schedule(guided) reduction(+:total2)
    for (int64_t U = 1; U <= max_u; U++) {
        int64_t rem = 1 - (U % 2);
        int64_t U2 = U * U;
        int64_t two_U2_plus_2U = 2 * U2 + 2 * U;
        if (two_U2_plus_2U > four_n) continue;

        int64_t cur_bound = isqrt_i64(four_n - two_U2_plus_2U);

        for (int64_t D2 = rem; D2 <= 2 * U; D2 += 2) {
            int64_t lhs_part = two_U2_plus_2U + D2 * D2 + 2 * D2;
            int64_t rem_val = four_n - lhs_part;
            if (rem_val < 0) break;

            while (cur_bound * cur_bound > rem_val) {
                cur_bound--;
            }

            int64_t max_D1 = 2 * U - D2;
            if (cur_bound < max_D1) max_D1 = cur_bound;
            if (max_D1 < rem) continue;

            int64_t J = (max_D1 - rem) / 2;
            int64_t cnt = J + 1;

            __int128 sum_j = (__int128)J * (J + 1) / 2;
            __int128 sum_j2 = (__int128)J * (J + 1) * (2 * J + 1) / 6;
            __int128 sum_D1_sq = (__int128)cnt * (rem * rem) + 4 * rem * sum_j + 4 * sum_j2;

            __int128 term = (__int128)cnt * (2 * U2 + D2 * D2) + sum_D1_sq;
            total2 += term;
        }
    }

    __int128 total = total1 + total2 - 12;
    int64_t ans = (int64_t)(total % mod);
    if (ans < 0) ans += mod;
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
        c_path = os.path.join(temp_dir, "solver791.c")
        ext = ".dll" if os.name == "nt" else ".so"
        so_path = os.path.join(temp_dir, f"libsolver791{ext}")
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(C_SOURCE)
        try:
            cmd = [cc, "-O3", "-fopenmp", "-shared", "-static", "-fPIC", c_path, "-o", so_path]
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            cmd = [cc, "-O3", "-shared", "-static", "-fPIC", c_path, "-o", so_path]
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dll = ctypes.CDLL(so_path)
        dll.solve_c_omp.argtypes = [ctypes.c_int64, ctypes.c_int64]
        dll.solve_c_omp.restype = ctypes.c_int64
        _COMPILED_C_SOLVER = dll.solve_c_omp
        return _COMPILED_C_SOLVER
    except Exception:
        return None


class Problem791:
    def __init__(self, limit: int = 10**8, mod: int = MOD):
        self.limit = limit
        self.mod = mod
        self._c_solver = _load_c_solver()

    def compute_S(self, n: int, mod: int = MOD) -> int:
        if self._c_solver is not None:
            ans = self._c_solver(int(n), int(mod))
            if ans >= 0:
                return ans

        # Pure Python fallback
        four_n = 4 * n
        max_u = int(math.isqrt(2 * n)) + 2
        total = 0

        # Case 1: rem = u % 2
        for u in range(1, max_u):
            rem = u % 2
            u2 = u * u
            two_u2_plus_2u = 2 * u2 + 2 * u
            if two_u2_plus_2u > four_n:
                break
            for d2 in range(rem, 2 * u + 1, 2):
                lhs_part = two_u2_plus_2u + d2 * d2 + 2 * d2
                if lhs_part > four_n:
                    break
                max_d1_by_bound = int(math.isqrt(four_n - lhs_part))
                max_d1 = min(2 * u - d2, max_d1_by_bound)
                if max_d1 < rem:
                    continue
                J = (max_d1 - rem) // 2
                cnt = J + 1
                sum_j = J * (J + 1) // 2
                sum_j2 = J * (J + 1) * (2 * J + 1) // 6
                sum_d1_sq = cnt * (rem * rem) + 4 * rem * sum_j + 4 * sum_j2
                term = cnt * (2 * u2 + d2 * d2) + sum_d1_sq
                total += term

        # Case 2: rem = 1 - (U % 2)
        for U in range(1, max_u):
            rem = 1 - (U % 2)
            U2 = U * U
            two_U2_plus_2U = 2 * U2 + 2 * U
            if two_U2_plus_2U > four_n:
                break
            for D2 in range(rem, 2 * U + 1, 2):
                lhs_part = two_U2_plus_2U + D2 * D2 + 2 * D2
                if lhs_part > four_n:
                    break
                max_D1_by_bound = int(math.isqrt(four_n - lhs_part))
                max_D1 = min(2 * U - D2, max_D1_by_bound)
                if max_D1 < rem:
                    continue
                J = (max_D1 - rem) // 2
                cnt = J + 1
                sum_j = J * (J + 1) // 2
                sum_j2 = J * (J + 1) * (2 * J + 1) // 6
                sum_D1_sq = cnt * (rem * rem) + 4 * rem * sum_j + 4 * sum_j2
                term = cnt * (2 * U2 + D2 * D2) + sum_D1_sq
                total += term

        total -= 12
        return total % mod

    @timeit
    def solve(self) -> int:
        return self.compute_S(self.limit, self.mod)


class Solution791(unittest.TestCase):
    def setUp(self):
        self.problem = Problem791()

    def test_sample(self):
        self.assertEqual(48, self.problem.compute_S(5, MOD))
        self.assertEqual(37048340, self.problem.compute_S(1000, MOD))

    def test_solution(self):
        self.assertEqual(404890862, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
