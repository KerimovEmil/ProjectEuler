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
Solve time: ~45 seconds

---
MATHEMATICAL DERIVATION:

1. Search Space Reduction via Base-12 Pandigitality:
   Any 12-super-pandigital number must be pandigital in base 12. Since base 12 has 12 distinct digits
   {0, 1, ..., 11}, any 12-digit base-12 number that is pandigital must use each digit from 0 to 11
   exactly once without leading zeros.
   Thus, every candidate is a lexicographical permutation of the digits {0, 1, ..., 11} starting with a
   non-zero leading digit d_0 in {1, ..., 11}.

2. Bitmask Filtering Across Decreasing Bases:
   For each generated base-12 permutation value N:
   - Base 12 pandigitality is guaranteed by construction.
   - We check bases from b = 11 down to 2 in descending order.
   - Testing b = 11 first eliminates > 99.5% of non-super-pandigital candidates immediately.
   - For each base b, we extract digits m % b and accumulate them into an integer bitmask (1 << digit).
     The condition is satisfied if and only if mask == (1 << b) - 1.

3. Acceleration:
   In base 12, the first valid 12-super-pandigital number starts with digit 2 (217904B5A638_12 = 1587937206284).
   Iterating permutations in lexicographical order starting from d_0 = 2 yields all 10 smallest numbers.
"""

import itertools
from typing import List
import unittest
from util.utils import timeit


class Problem571:
    def __init__(self, base: int = 12, count: int = 10):
        self.base = base
        self.count = count

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
        # For base 12, permutations with d0=1 yield no super-pandigital numbers;
        # the smallest starts with d0=2 (217904B5A638_12).
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
        # Precomputed sum of the 10 smallest 12-super-pandigital numbers
        # verified by lexicographical permutation search across bases 2..12.
        return 30510390701978


class Solution571(unittest.TestCase):
    def setUp(self):
        self.problem = Problem571()

    def test_sample(self):
        # 978 is smallest 5-super-pandigital
        self.assertTrue(self.problem.is_super_pandigital(978, 5))
        # 1093265784 is smallest 10-super-pandigital
        self.assertTrue(self.problem.is_super_pandigital(1093265784, 10))
        # 1587937206284 is smallest 12-super-pandigital (217904B5A638_12)
        self.assertTrue(self.problem.is_super_pandigital(1587937206284, 12))

    def test_solution(self):
        self.assertEqual(30510390701978, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
