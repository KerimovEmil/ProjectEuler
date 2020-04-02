"""
PROBLEM

Let S(n,m) = ∑φ(n × i) for 1 ≤ i ≤ m. (φ is Euler's totient function)
You are given that S(510510,10^6)= 45480596821125120.

Find S(510510,10^11).
Give the last 9 digits of your answer.

ANSWER:
754862080
Solve time too_long seconds
"""

import unittest
from util.utils import timeit, euler_totient_function, len_faray_seq
from math import gcd

# 510510 = 2×3×5×7×11×13×17
# n = 510510
# phi(n) = 92160


@timeit
def g(m):
    """For any m,n>0, let d=gcd(m,n), then Phi(m*n) = Phi(m) * Phi(n) * d/Phi(d)"""
    n = 510510
    ans = 0
    phi_n = euler_totient_function(n)

    for i in range(1, m+1):
        d = gcd(i, n)
        ans += euler_totient_function(i) * d / euler_totient_function(d)
    return ans*phi_n


def factor(n):
    """returns the largest factor of n"""
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return factor(n // i)
    return n

# def factor_2(n):
#     """returns the largest factor of n"""
#     for i in range(int(n ** 0.5) + 1, 2, -1):
#         if n % i == 0:
#             return i
#     return None



def S(n, m):
    # print(n, m)
    if m == 0 or n == 0:
        return 0
    if m == 1:
        return euler_totient_function(n)
    if n == 1:
        return len_faray_seq(m) - 1

    p = factor(n)
    q = n // p
    r = (p - 1) * S(q, m)
    return r + S(n, m // p)


class Problem432:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self, m):
        return S(self.n, m)


class Solution432(unittest.TestCase):
    def setUp(self):
        self.problem = Problem432(n=510510)

    def test_solution(self):
        self.assertEqual(754862080, self.problem.solve(int(1e11)) % int(1e9))

    def test_solution_4(self):
        self.assertEqual(4548570531840, self.problem.solve(int(1e4)))

    def test_solution_6(self):
        self.assertEqual(45480596821125120, self.problem.solve(int(1e6)))


if __name__ == '__main__':
    unittest.main()

