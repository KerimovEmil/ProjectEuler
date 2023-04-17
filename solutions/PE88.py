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
from util.utils import timeit
import unittest

# NOTE 1: the product of positive integers will always be greater than the sum, unless it is 2x2=2+2 or contains 1's.

# NOTE 2: given k, min possible integer is k, since 1+1+..+1 > 1*1*1..*1

# NOTE 3: given k, max possible integer is 2*k, since 1*1*..*1*2*k = k+2+(k-2)*1 = 2*k
# e.g. k=5, pick terms 2*5, then we get 2*5 > 2+5. Add 3 1's, and we get 1*1*1*2*5=1+1+1+2+5

# Therefore we're looking for the minimal factorization

# Note 4: given Note 1, we should always have some 1 terms (except for 2x2) and at least 2 non-one terms.

# k=66: 132 = 2 × 66 × 1^64 = 2 + 66 + 1*66                 -> 1+1+64 = 66
# k=100: 108 = 2^2 × 3^3 × 1^95 = 2 + 2 + 3 + 3 + 3 + 1*95  -> 2+3+95=100


def small_factor_generator(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            yield i


class Problem88:
    def __init__(self):
        pass

    @timeit
    def solve(self, n):
        """
        Get the sum of the minimum n = prod(S(k)) = sum(S(k)) where S(k) is a set of k numbers between 2 <= k <= max_k.

        Fact: n = prod(S(k)) = sum(S(k)) > k.
        Fact: n is not prime.
        """
        # from thread answer:
        # For each N, we want A(N): all (f, s) such that there are f integers >= 1 whose sum is s and product is N
        # If (f, s) is in A(N), then N is a solution to the problem for k = N+f-s.
        best = [0] * (n + 1)
        sum_decomp = {}
        for i in range(2, 2 * n + 1):  # e.g. i = 36
            sum_decomp[i] = {(1, i)}  # e.g. 36 = 1 x 36
            for k in small_factor_generator(i):  # e.g. k = [2, 3, 4, 6]
                for a, b in sum_decomp[i // k]:  # i//k -> [18, 12, 9, 6]
                    sum_decomp[i].add((a + 1, b + k))
                    # store best digit result
                    dex = i + (a + 1) - (b + k)
                    if dex <= n and best[dex] == 0:
                        best[dex] = i
        return sum(set(best[2:]))


class Solution88(unittest.TestCase):
    def setUp(self):
        self.problem = Problem88()

    def test_n_6_solution(self):
        self.assertEqual(30, self.problem.solve(n=6))

    def test_n_12_solution(self):
        self.assertEqual(61, self.problem.solve(n=12))

    def test_n_100_solution(self):
        self.assertEqual(2061, self.problem.solve(n=100))

    def test_n_1200_solution(self):
        self.assertEqual(125128, self.problem.solve(n=1200))

    def test_solution(self):
        self.assertEqual(7587457, self.problem.solve(n=12000))


if __name__ == '__main__':
    unittest.main()
