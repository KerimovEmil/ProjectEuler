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
Solve time: ~0.035 seconds (pure Python: ~8.5 seconds)

---
MATHEMATICAL DERIVATION:

1. Condition on Average and Variance:
   For k = 4, let s = a + b + c + d.
   The condition \bar{x} = 2\sigma^2 expands to:
     4(a^2 + b^2 + c^2 + d^2) = s(s + 2)

2. Walsh-Hadamard Transform H_2:
   Transform the quadruple (a, b, c, d) using the orthogonal Walsh-Hadamard basis:
     x = (-a - b + c + d) / 2
     y = (-a + b - c + d) / 2
     z = ( a - b - c + d) / 2
   along with the sum s = a + b + c + d.
   By Parseval's identity on H_2:
     4(a^2 + b^2 + c^2 + d^2) = s^2 + 4(x^2 + y^2 + z^2)
   Substituting into 4\sum x_i^2 = s(s + 2) = s^2 + 2s gives:
     s^2 + 4(x^2 + y^2 + z^2) = s^2 + 2s  ==>  s = 2(x^2 + y^2 + z^2).
   The quadratic coupling on s cancels out completely!

3. Domain Constraints:
   The ordering 1 <= a <= b <= c <= d <= n maps to:
     x >= y >= |z|
     d = (s + x + y + z) / 2 <= n  ==>  x^2 + y^2 + z^2 + x + y + z <= 2n.
   The condition a = (s - x - y + z) / 2 >= 1 holds for all quadruples except (1, 1, 1, 3),
   which corresponds to x = 1 (where s = 6, accounted for by tot = 3).

4. Ehrhart Polynomial on the Unconstrained Interior Chamber:
   Since x >= y >= |z|, the maximum of d(x, y, z) for a fixed x occurs at y = x, z = x:
     d_max(x) = (3/2) x(x + 1)
   When x <= x_3 = floor(sqrt(2n/3 + 1/4) - 1/2), d_max(x) <= n is ALWAYS satisfied!
   In this region, the boundary condition is flat and linear, defining a dilated Weyl chamber.
   By Ehrhart's theory, the sum of terms over the entire interior cone evaluates to a degree-5 polynomial:
     \sum_{x=1}^{x_3} \left[ (x(x+1))^2 + (2x+3) \frac{x(x+1)(2x+1)}{6} \right] = \frac{x_3(x_3+1)(2x_3+1)(x_3+2)^2}{6}.
   Subtracting 9 (for x = 1) and adding the initial tot = 3 evaluates the entire interior region
   (over 60% of the domain) in O(1) time:
     tot_interior = \frac{x_3(x_3+1)(2x_3+1)(x_3+2)^2}{6} - 6.

5. Active Boundary Strip:
   For x > x_3, when y <= y_2(x) = floor((sqrt(4n - 2x(x + 1) + 1) - 1) / 2), the z-sum is still unconstrained
   and evaluates in closed form. Only for the active boundary strip y_2 < y <= min(x, y_1) do we explicitly
   compute the bound on z and sum in O(1).
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
#include <math.h>

#ifdef _WIN32
__declspec(dllexport)
#endif
int64_t solve_c_walsh(int64_t N0, int64_t M) {
    int64_t x3 = (int64_t)(sqrt(2.0 / 3.0 * N0 + 0.25) - 0.5);
    int64_t x1 = (int64_t)(sqrt(2.0 * N0 + 0.25) - 0.5);
    int64_t inv6 = 72249073;  // 6^(-1) mod 433494437
    int64_t inv3 = 144498146; // 3^(-1) mod 433494437

    int64_t tot;
    if (x3 >= 1) {
        int64_t p1 = (x3 * (x3 + 1)) % M;
        int64_t p2 = ((2 * x3 + 1) % M) * (((x3 + 2) * (x3 + 2)) % M) % M;
        int64_t full = (p1 * p2) % M;
        tot = ((full * inv6 - 6) % M + M) % M;
    } else {
        tot = 3;
    }

    __int128 boundary_tot = 0;

    #pragma omp parallel for schedule(guided) reduction(+:boundary_tot)
    for (int64_t x = x3 + 1; x <= x1; x++) {
        int64_t y2 = (int64_t)((sqrt(4.0 * N0 - 2.0 * x * (x + 1) + 1.0) - 1.0) / 2.0);
        int64_t y1 = (int64_t)((sqrt(4.0 * (2.0 * N0 - x * (x + 1)) + 1.0) - 1.0) / 2.0);

        int64_t term = (x * (y2 + 1)) % M;
        term = (term * term) % M;
        int64_t term2 = ((2 * y2 + 3) % M) * ((y2 * (y2 + 1) / 2) % M) % M;
        term2 = (term2 * ((2 * y2 + 1) % M)) % M;
        term2 = (term2 * inv3) % M;
        int64_t local_sum = (term + term2) % M;

        int64_t max_y = x < y1 ? x : y1;
        for (int64_t y = y2 + 1; y <= max_y; y++) {
            int64_t z1 = (int64_t)((sqrt(4.0 * (2.0 * N0 - x * (x + 1) - y * (y + 1)) + 1.0) - 1.0) / 2.0);
            int64_t z1_p1 = z1 + 1;
            int64_t t1 = (2 * z1_p1) % M * ((x * x + y * y) % M) % M;
            int64_t t2 = (z1 % M) * ((z1 + 1) % M) % M * ((2 * z1 + 1) % M) % M;
            t2 = (t2 * inv3) % M;
            int64_t t3 = (z1_p1 % M) * (z1_p1 % M) % M;
            local_sum = (local_sum + t1 + t2 + t3) % M;
        }

        boundary_tot += local_sum;
    }

    tot = (tot + (int64_t)(boundary_tot % M)) % M;
    return (2 * tot) % M;
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
        dll.solve_c_walsh.argtypes = [ctypes.c_int64, ctypes.c_int64]
        dll.solve_c_walsh.restype = ctypes.c_int64
        _COMPILED_C_SOLVER = dll.solve_c_walsh
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

        # Pure Python fallback using Ehrhart polynomial on interior chamber
        x3 = int(math.sqrt(2.0 / 3.0 * n + 0.25) - 0.5)
        x1 = int(math.sqrt(2.0 * n + 0.25) - 0.5)

        if x3 >= 1:
            inv6 = pow(6, -1, mod)
            tot = (x3 * (x3 + 1) % mod) * ((2 * x3 + 1) % mod) % mod * pow(x3 + 2, 2, mod) % mod
            tot = (tot * inv6 - 6) % mod
        else:
            tot = 3

        for x in range(x3 + 1, x1 + 1):
            y2 = int((math.sqrt(4.0 * n - 2.0 * x * (x + 1) + 1.0) - 1.0) / 2.0)
            y1 = int((math.sqrt(4.0 * (2.0 * n - x * (x + 1)) + 1.0) - 1.0) / 2.0)
            tot += (x * (y2 + 1)) ** 2 + (2 * y2 + 3) * (y2 * (y2 + 1) * (2 * y2 + 1) // 6)
            tot %= mod

            max_y = min(x, y1)
            for y in range(y2 + 1, max_y + 1):
                z1 = int((math.sqrt(4.0 * (2.0 * n - x * (x + 1) - y * (y + 1)) + 1.0) - 1.0) / 2.0)
                term = 2 * (z1 + 1) * (x**2 + y**2) + (z1 * (z1 + 1) * (2 * z1 + 1)) // 3 + (z1 + 1) ** 2
                tot = (tot + term) % mod

        return (2 * tot) % mod

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
