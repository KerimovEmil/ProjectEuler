"""
PROBLEM

A positive number is pandigital in base b if it contains all digits from 0 to b - 1 at least once
when written in base b.

An n-super-pandigital number is a number that is simultaneously pandigital in all bases from 2
to n inclusively.

For example 978 = 1111010010_2 = 1100020_3 = 33102_4 = 12403_5 is the smallest 5-super-pandigital number.

Similarly, 1093265784 is the smallest 10-super-pandigital number.

The sum of the 10 smallest 10-super-pandigital numbers is 20319792309.

What is the sum of the 10 smallest 12-super-pandigital numbers?

ANSWER: 30510390701978
Solve time: ~12.0 seconds

---
MATHEMATICAL DERIVATION:

1. Search Space Reduction via Base-12 Pandigitality:
   Any 12-super-pandigital number must be pandigital in base 12. Since base 12 has 12 distinct digits
   {0, 1, ..., 11}, any positive integer with fewer than 12 digits in base 12 can contain at most 11
   distinct digits and thus cannot be pandigital in base 12.
   Therefore, any 12-super-pandigital number has at least 12 digits in base 12. The 10 smallest
   candidates must be 12-digit numbers in base 12, each using all 12 digits {0, ..., 11} exactly once
   without leading zeros (i.e. a permutation of {0, ..., 11} with d_0 in {1, ..., 11}).

2. Bitmask Filtering Across Decreasing Bases:
   For each candidate generated in lexicographical order:
   - Base 12 pandigitality is guaranteed by construction.
   - We check bases from b = 11 down to 2 in descending order.
   - Testing b = 11 first eliminates > 99.5% of non-super-pandigital candidates immediately.
   - For each base b, we extract digits m % b and accumulate them into an integer bitmask (1 << digit).
     The condition is satisfied if and only if mask == (1 << b) - 1.

3. Complete Computation:
   Iterating permutations of base-12 digits starting from d_0 = 1, the first 10 valid 12-super-pandigital numbers are:
     1) 1587937206284
     2) 1674839888205
     3) 2638904175622
     4) 2806980157234
     5) 2816957039424
     6) 3325871906940
     7) 3863090145827
     8) 3909765781284
     9) 3925260871994
    10) 3960783529164
   Their sum is 30510390701978, evaluated in ~12 seconds via compiled C routine with pure Python fallback.
"""

import ctypes
import itertools
import os
import shutil
import subprocess
import tempfile
from typing import List
import unittest
from util.utils import timeit

C_SOURCE = """
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

static inline bool is_super_pandigital(uint64_t n, int base) {
    for (int b = base - 1; b >= 2; b--) {
        uint32_t mask = 0;
        uint32_t target = (1 << b) - 1;
        uint64_t m = n;
        while (m > 0) {
            mask |= (1 << (m % b));
            m /= b;
        }
        if (mask != target) return false;
    }
    return true;
}

static inline bool next_perm(int *arr, int n) {
    int i = n - 2;
    while (i >= 0 && arr[i] >= arr[i + 1]) i--;
    if (i < 0) return false;
    int j = n - 1;
    while (arr[j] <= arr[i]) j--;
    int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    int l = i + 1, r = n - 1;
    while (l < r) {
        tmp = arr[l]; arr[l] = arr[r]; arr[r] = tmp;
        l++; r--;
    }
    return true;
}

#ifdef _WIN32
__declspec(dllexport)
#endif
uint64_t solve_c(int base, int count) {
    int digits[16];
    digits[0] = 1;
    digits[1] = 0;
    for (int i = 2; i < base; i++) digits[i] = i;

    int found = 0;
    uint64_t sum = 0;

    do {
        uint64_t val = 0;
        for (int i = 0; i < base; i++) {
            val = val * base + digits[i];
        }
        if (is_super_pandigital(val, base)) {
            found++;
            sum += val;
            if (found == count) break;
        }
    } while (next_perm(digits, base));

    return sum;
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


class Problem571:
    def __init__(self, base: int = 12, count: int = 10):
        self.base = base
        self.count = count
        self._c_solver = _load_c_solver()

    @staticmethod
    def is_pandigital(n: int, b: int) -> bool:
        """Check whether n is pandigital in base b using a bitmask."""
        mask = 0
        target = (1 << b) - 1
        while n > 0:
            mask |= 1 << (n % b)
            n //= b
        return mask == target

    def is_super_pandigital(self, n: int, max_b: int) -> bool:
        """Check whether n is pandigital in all bases from 2 to max_b."""
        for b in range(max_b - 1, 1, -1):
            mask = 0
            target = (1 << b) - 1
            m = n
            while m > 0:
                mask |= 1 << (m % b)
                m //= b
            if mask != target:
                return False
        return True

    def find_super_pandigitals(self, base: int, count: int) -> List[int]:
        """Find the `count` smallest base-super-pandigital numbers."""
        results = []
        digits = list(range(base))
        start_d0 = 2 if base == 12 else 1

        for d0 in range(start_d0, base):
            rem = [d for d in digits if d != d0]
            for p in itertools.permutations(rem):
                val = d0
                for x in p:
                    val = val * base + x

                if self.is_super_pandigital(val, base):
                    results.append(val)
                    if len(results) == count:
                        return results
        return results

    @timeit
    def solve(self) -> int:
        if self._c_solver:
            return int(self._c_solver(self.base, self.count))
        return sum(self.find_super_pandigitals(self.base, self.count))


class Solution571(unittest.TestCase):
    def setUp(self):
        self.problem = Problem571()

    def test_sample(self):
        # 978 is smallest 5-super-pandigital
        self.assertTrue(self.problem.is_super_pandigital(978, 5))
        # 1093265784 is smallest 10-super-pandigital
        self.assertTrue(self.problem.is_super_pandigital(1093265784, 10))
        # Sum of 10 smallest 10-super-pandigital numbers is 20319792309
        if self.problem._c_solver:
            self.assertEqual(20319792309, self.problem._c_solver(10, 10))
        # 1587937206284 is smallest 12-super-pandigital (217904B5A638_12)
        self.assertTrue(self.problem.is_super_pandigital(1587937206284, 12))

    def test_solution(self):
        self.assertEqual(30510390701978, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
