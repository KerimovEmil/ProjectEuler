"""
PROBLEM

A natural number, N, that can be written as the sum and product of a given set of at least two natural numbers,
{a1, a2, ... , ak} is called a product-sum number: N = a1 + a2 + ... + ak = a1 × a2 × ... × ak.

For example, 6 = 1 + 2 + 3 = 1 × 2 × 3.

For a given set of size, k, we shall call the smallest N with this property a minimal product-sum number.
The minimal product-sum numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.

k=2: 4 = 2 × 2 = 2 + 2
k=3: 6 = 1 × 2 × 3 = 1 + 2 + 3
k=4: 8 = 1 × 1 × 2 × 4 = 1 + 1 + 2 + 4
k=5: 8 = 1 × 1 × 2 × 2 × 2 = 1 + 1 + 2 + 2 + 2
k=6: 12 = 1 × 1 × 1 × 1 × 2 × 6 = 1 + 1 + 1 + 1 + 2 + 6

Hence for 2≤k≤6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30; note that 8 is only counted once in
the sum.

In fact, as the complete set of minimal product-sum numbers for 2≤k≤12 is {4, 6, 8, 12, 15, 16}, the sum is 61.

What is the sum of all the minimal product-sum numbers for 2≤k≤12000?

ANSWER: 7587457
Solve time: ~ seconds
"""
from util.utils import timeit, all_possible_factorizations, primes_of_n
import unittest
# from math import prod
from primesieve import primes

# NOTE 1: the product of positive integers will always be greater than the sum, unless it is 2x2=2+2 or contains 1's.

# NOTE 2: given k, min possible integer is k, since 1+1+..+1 > 1*1*1..*1

# NOTE 3: given k, max possible integer is 2*k, since 1*1*..*1*2*k = k+2+(k-2)*1 = 2*k
# e.g. k=5, pick terms 2*5, then we get 2*5 > 2+5. Add 3 1's, and we get 1*1*1*2*5=1+1+1+2+5

# Therefore we're looking for the minimal factorization

# Note 4: given Note 1, we should always have some 1 terms (except for 2x2) and at least 2 non-one terms.


class Problem88:
    def __init__(self):
        pass

    @timeit
    def solve(self, n):
        ls_primes = list(primes(n))

        # min_factorization = [2 * n] * (n + 1)
        # min_factorization[1] = 0

        pairs = {}
        for num in range(4, 2*n + 1):
            ways = all_possible_factorizations(primes_of_n(num, ls_primes))
            for w in ways:
                if len(w) > 1:
                    k = num - sum(w) + len(w)
                    if k <= n:
                        pairs.setdefault(k, num)
        res = sum(set(pairs.values()))
        print(pairs)

        return res


class Solution88(unittest.TestCase):
    def setUp(self):
        self.problem = Problem88()

    def test_n_6_solution(self):
        self.assertEqual(30, Problem88().solve(n=6))

    def test_n_12_solution(self):
        self.assertEqual(61, Problem88().solve(n=12))

    def test_n_100_solution(self):
        self.assertEqual(2061, Problem88().solve(n=100))

    # def test_n_1200_solution(self):
    #     self.assertEqual(125128, Problem88().solve(n=1200))

    # def test_solution(self):
    #     self.assertEqual(7587457, Problem88().solve(n=12000))


if __name__ == '__main__':
    unittest.main()
