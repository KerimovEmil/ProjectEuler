"""
PROBLEM

The radical of n, rad(n), is the product of the distinct prime factors of n. For example, 504 = 23 × 32 × 7, so
rad(504) = 2 × 3 × 7 = 42.

Let E(k) be the kth element in the sorted n column; for example, E(4) = 8 and E(6) = 9.
If rad(n) is sorted for 1 ≤ n ≤ 100000, find E(10000).

ANSWER:
21417
Solve time ~2 seconds
"""


from util.utils import timeit, primes_of_n
import unittest
import functools
import operator


class Problem124:
    def __init__(self, max_n, order):
        self.max_n = max_n
        self.order = order

    @timeit
    def solve(self):
        if self.order == 1:
            return 1

        def prod(k):
            return functools.reduce(lambda a, b: a * b, k)

        ls_full = {i: prod(primes_of_n(i)) for i in range(2, self.max_n+1)}

        sorted_x = sorted(ls_full.items(), key=operator.itemgetter(1))

        return sorted_x[self.order - 2][0]


class Solution124(unittest.TestCase):
    def test_solution_small(self):
        self.assertEqual(8, Problem124(max_n=10, order=4).solve())
        self.assertEqual(9, Problem124(max_n=10, order=6).solve())
        self.assertEqual(10, Problem124(max_n=10, order=10).solve())

    def test_solution(self):
        self.assertEqual(21417, Problem124(max_n=100000, order=10000).solve())


if __name__ == '__main__':
    unittest.main()

