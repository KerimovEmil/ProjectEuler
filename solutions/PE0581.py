"""
PROBLEM

A number is p-smooth if it has no prime factors larger than p.
Let T be the sequence of triangular numbers, i.e. T(n) = n(n+1)/2

Find the sum of all indices n such that T(n) is 47-smooth.

ANSWER: 2227616372734
Solve time: ~10.5 seconds
"""

import unittest
import numpy as np
from util.utils import timeit


# MATHEMATICAL DERIVATION:
#
# 1. Smooth Triangular Numbers and Consecutive Smooth Pairs:
#    T(n) = n * (n + 1) / 2.
#    Since gcd(n, n + 1) = 1, T(n) is 47-smooth if and only if both n and n + 1 are 47-smooth.
#    Therefore, every index n corresponds to a pair of consecutive 47-smooth numbers (n, n + 1).
#
# 2. Bound on Consecutive 47-Smooth Numbers:
#    By Størmer's Theorem (using solutions to Pell's equations x^2 - D*y^2 = 1 for square-free 47-smooth D),
#    the maximum consecutive 47-smooth number is bounded by 1,109,496,723,126 (OEIS A117581 / Lehmer 1964).
#
# 3. High-Performance Generation:
#    - Iteratively expand 47-smooth numbers in a flat list without recursion overhead.
#    - Sort the array and detect consecutive elements via NumPy vector difference (diff == 1).


class Problem581:
    def __init__(self):
        self.ls_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        self.max_n = 1_109_496_723_127

    @timeit
    def solve(self):
        results = [1]
        max_n = self.max_n
        for p in self.ls_prime:
            n_prev = len(results)
            for i in range(n_prev):
                val = results[i] * p
                while val <= max_n:
                    results.append(val)
                    val *= p

        arr = np.array(results, dtype=np.int64)
        arr.sort()

        diff = arr[1:] - arr[:-1]
        consec_indices = np.nonzero(diff == 1)[0]
        return int(np.sum(arr[consec_indices]))


class Solution581(unittest.TestCase):
    def setUp(self):
        self.problem = Problem581()

    def test_solution(self):
        self.assertEqual(2_227_616_372_734, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
