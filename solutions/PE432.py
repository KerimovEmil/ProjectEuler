"""
PROBLEM

Let S(n,m) = ∑φ(n × i) for 1 ≤ i ≤ m. (φ is Euler's totient function)
You are given that S(510510,10^6)= 45480596821125120.

Find S(510510,10^11).
Give the last 9 digits of your answer.

ANSWER:
754862080
Solve time 618 seconds ~ 10 mins + 20 seconds
"""

import unittest
from util.utils import timeit, euler_totient_function, sum_phi

# 510510 = 2×3×5×7×11×13×17
# n = 510510
# phi(n) = 92160


# Solution idea:
# comment from user Guego on https://projecteuler.net/thread=432
# It is easy to compute S(1,n) recursively using the relation S(1,n) = n(n+1)/2 − ∑d≥2 S(1,n/d).
# Then, I just noticed that S(p*k,n)=(p−1)*S(k,n)+S(p*k,n/p) if p is a prime number.
# S(1,n) = sum of euler totient function, could be implemented even more efficiently, see util function


class Problem432:
    def __init__(self, n, ls_p, mod):
        self.n = n
        self.ls_p = ls_p
        self.mod = mod

    @timeit
    def solve(self, m):

        def S(L, n):
            if len(L) == 0:
                return sum_phi(n)
            else:
                if n == 0:
                    return 0
                else:
                    return (L[0] - 1) * S(L[1:], n) + S(L, n // L[0])

        return S(self.ls_p, m) % self.mod


class Solution432(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problem = Problem432(n=510510, ls_p=[2, 3, 5, 7, 11, 13, 17], mod=int(1e9))

    def test_solution(self):
        self.assertEqual(754862080, self.problem.solve(int(1e11)))

    def test_sum_phi_function(self):
        n = 5000
        self.assertEqual(sum(euler_totient_function(i) for i in range(1, n+1)), sum_phi(n))

    def test_solution_4(self):
        self.assertEqual(570531840, self.problem.solve(int(1e4)))

    def test_solution_6(self):
        self.assertEqual(821125120, self.problem.solve(int(1e6)))


if __name__ == '__main__':
    unittest.main()
