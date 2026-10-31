"""
PROBLEM

Let r be the real root of the equation x^3 = x^2 + 1.

Every positive integer can be written as the sum of distinct increasing powers of r.

If we require the number of terms to be finite and the difference between any two exponents
to be three or more, then the representation is unique.

For example, 3 = r^(-10) + r^(-5) + r^(-1) + r^2 and 10 = r^(-10) + r^(-7) + r^6.

Interestingly, the relation holds for the complex roots of the equation.

Let w(n) be the number of terms in this unique representation of n.
Thus w(3) = 4 and w(10) = 3.

More formally, for all positive integers n, we have:
  n = sum_{k=-infinity}^infinity b_k r^k
under the conditions that:
  b_k is 0 or 1 for all k;
  b_k + b_{k+1} + b_{k+2} <= 1 for all k;
  w(n) = sum_{k=-infinity}^infinity b_k is finite.

Let S(m) = sum_{j=1}^m w(j^2).

You are given S(10) = 61 and S(1000) = 19403.

Find S(5 000 000).

ANSWER: 226754889
Solve time: ~8.5 seconds

---
MATHEMATICAL DERIVATION:

1. Base-r Arithmetic and Carry Propagation:
   The base r satisfies r^3 = r^2 + 1.
   Multiplying or dividing this characteristic equation yields five fundamental identities:
     (1) r^x + r^(x+2) = r^(x+3)
     (2) r^x + r^(x-2) = r^(x+1)
     (3) r^x + r^(x-1) = r^(x+1) + r^(x-4)
     (4) r^x + r^(x+1) = r^(x+2) + r^(x-3)
     (5) 2 * r^x = r^(x+1) + r^(x-2) + r^(x-7)

   Any integer addition of a term r^x can be reduced to canonical form (where no two powers
   are within distance 2 of each other) by recursively resolving collisions using identities
   (1) through (5). When no neighbor within distance 2 exists, we simply set b_x = 1.

2. Incremental Evaluation over Squares:
   Rather than computing w(j^2) independently for each j from scratch, we observe that:
     j^2 = (j - 1)^2 + (2j - 1).
   Furthermore, the odd difference increments by 2 each step:
     (2j - 1) = (2(j - 1) - 1) + 2.

   We maintain two canonical base-r representations:
     f: representing the odd increment (2j - 1)
     g: representing the square j^2 = (j - 1)^2 + f

   In step j:
     - For j = 1, f = 0 + 1 = 1 (r^0).
     - For j > 1, f is updated by adding 2 = 1 + 1 (adding r^0 twice).
     - Each active power r^t present in f is then added into g using the carry DFS.
     - The number of non-zero terms in g is w(j^2), which is accumulated into S(m).

3. Performance & Acceleration:
   For m = 5,000,000, the maximum exponent reached is floor(ln(2.5 * 10^13) / ln(r)) = 80,
   and minimum exponent is around -168.
   An array of size 600 centered at exponent 0 (offset 300) suffices.
   The carry-propagation DFS on this compact array runs in ~8.5 seconds via on-the-fly C
   compilation (using ctypes), with an automatic fallback to pure Python if no C compiler
   is present.
"""

import ctypes
import os
import shutil
import subprocess
import tempfile
from typing import List, Tuple
import unittest
from util.utils import timeit


C_SOURCE = """
#include <stdint.h>

#define B 300
static int f[B * 2], g[B * 2];

static void dfs(int *arr, int x) {
    if (arr[x + 2]) {
        --arr[x + 2];
        dfs(arr, x + 3);
    } else if (arr[x - 2]) {
        --arr[x - 2];
        dfs(arr, x + 1);
    } else if (arr[x - 1]) {
        --arr[x - 1];
        dfs(arr, x + 1);
        dfs(arr, x - 4);
    } else if (arr[x + 1]) {
        --arr[x + 1];
        dfs(arr, x + 2);
        dfs(arr, x - 3);
    } else if (arr[x]) {
        --arr[x];
        dfs(arr, x + 1);
        dfs(arr, x - 2);
        dfs(arr, x - 7);
    } else {
        ++arr[x];
    }
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int64_t solve_c(int limit) {
    for (int i = 0; i < B * 2; ++i) { f[i] = 0; g[i] = 0; }
    int64_t ans = 0;
    for (int i = 1; i <= limit; ++i) {
        dfs(f, B);
        if (i != 1) dfs(f, B);
        for (int t = 0; t < B * 2; ++t) {
            if (f[t]) dfs(g, t);
        }
        for (int t = 0; t < B * 2; ++t) {
            if (g[t]) ++ans;
        }
    }
    return ans;
}
"""


def _load_c_solver():
    """Compile and load the C implementation via ctypes, or return None if unavailable."""
    compiler = shutil.which('gcc') or shutil.which('clang')
    if not compiler:
        return None
    try:
        cache_dir = os.path.join(tempfile.gettempdir(), 'pe558_cache')
        os.makedirs(cache_dir, exist_ok=True)
        ext = 'dll' if os.name == 'nt' else 'so'
        lib_path = os.path.join(cache_dir, f'solve_558.{ext}')
        c_path = os.path.join(cache_dir, 'solve_558.c')

        if not os.path.exists(lib_path):
            with open(c_path, 'w', encoding='utf-8') as f:
                f.write(C_SOURCE)
            subprocess.run([compiler, '-O3', '-shared', '-fPIC', c_path, '-o', lib_path],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        lib = ctypes.CDLL(lib_path)
        lib.solve_c.argtypes = [ctypes.c_int]
        lib.solve_c.restype = ctypes.c_int64
        return lib.solve_c
    except Exception:
        return None


class Problem558:
    def __init__(self, m: int = 5_000_000):
        self.m = m
        self._c_solver = _load_c_solver()

    @staticmethod
    def w_and_terms(n: int, base_offset: int = 300) -> Tuple[int, List[int]]:
        """Return the count w(n) and sorted list of exponents in canonical representation of n."""
        arr = [0] * (base_offset * 2)

        def add_power(x: int):
            st = [x]
            while st:
                curr = st.pop()
                if arr[curr + 2]:
                    arr[curr + 2] -= 1
                    st.append(curr + 3)
                elif arr[curr - 2]:
                    arr[curr - 2] -= 1
                    st.append(curr + 1)
                elif arr[curr - 1]:
                    arr[curr - 1] -= 1
                    st.append(curr - 4)
                    st.append(curr + 1)
                elif arr[curr + 1]:
                    arr[curr + 1] -= 1
                    st.append(curr - 3)
                    st.append(curr + 2)
                elif arr[curr]:
                    arr[curr] -= 1
                    st.append(curr - 7)
                    st.append(curr - 2)
                    st.append(curr + 1)
                else:
                    arr[curr] += 1

        for _ in range(n):
            add_power(base_offset)

        exponents = [i - base_offset for i in range(len(arr)) if arr[i]]
        return len(exponents), exponents

    def _solve_py(self, limit: int) -> int:
        """Pure Python solver for S(m) using incremental carry propagation."""
        base_offset = 300
        size = base_offset * 2
        f = [0] * size
        g = [0] * size

        def add_term(arr: List[int], x: int):
            st = [x]
            while st:
                curr = st.pop()
                if arr[curr + 2]:
                    arr[curr + 2] -= 1
                    st.append(curr + 3)
                elif arr[curr - 2]:
                    arr[curr - 2] -= 1
                    st.append(curr + 1)
                elif arr[curr - 1]:
                    arr[curr - 1] -= 1
                    st.append(curr - 4)
                    st.append(curr + 1)
                elif arr[curr + 1]:
                    arr[curr + 1] -= 1
                    st.append(curr - 3)
                    st.append(curr + 2)
                elif arr[curr]:
                    arr[curr] -= 1
                    st.append(curr - 7)
                    st.append(curr - 2)
                    st.append(curr + 1)
                else:
                    arr[curr] += 1

        total = 0
        for i in range(1, limit + 1):
            add_term(f, base_offset)
            if i != 1:
                add_term(f, base_offset)

            for t in range(size):
                if f[t]:
                    add_term(g, t)

            for t in range(size):
                if g[t]:
                    total += 1

        return total

    def compute_s(self, limit: int) -> int:
        """Compute S(limit) using C-accelerator if available, else pure Python."""
        if self._c_solver is not None:
            return int(self._c_solver(limit))
        return self._solve_py(limit)

    @timeit
    def solve(self) -> int:
        return self.compute_s(self.m)


class Solution558(unittest.TestCase):
    def setUp(self):
        self.problem = Problem558()

    def test_samples(self):
        w_3, terms_3 = Problem558.w_and_terms(3)
        self.assertEqual(4, w_3)
        self.assertEqual([-10, -5, -1, 2], terms_3)

        w_10, terms_10 = Problem558.w_and_terms(10)
        self.assertEqual(3, w_10)
        self.assertEqual([-10, -7, 6], terms_10)

        self.assertEqual(61, self.problem.compute_s(10))
        self.assertEqual(19403, self.problem.compute_s(1000))

    def test_solution(self):
        self.assertEqual(226754889, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
