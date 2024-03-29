"""
Let F5(n) be the number of strings s such that:
- s consists only of '0's and '1's,
- s has length at most n, and
- s contains a palindromic substring of length at least 5.

For example, F5(4) = 0, F5(5) = 8, F5(6) = 42 and F5(11) = 3844.

Let D(L) be the number of integers n such that 5 ≤ n ≤ L and F5(n) is divisible by 87654321.

For example, D(10^7) = 0 and D(5·10^9) = 51.

Find D(10^18).

ANSWER: 11408450515
Solve time: 1.5 seconds
"""

from util.utils import timeit, lcm
from util.crt import ChineseRemainderTheoremSets
import unittest


def f5(n):
    """Analytical solution"""
    p = [1, 1, 1, 1, 0, -2]
    k = n // 6
    t = 2**n - 16*n + 56 - 4*k + p[n % 6]
    if n == 5:
        t -= 2
    return 2*t


# Let D(L) be the number of integers n such that 5 ≤ n ≤ L and F5(n) is divisible by 87654321 = 3^2 × 1997 × 4877
# Figure out when F5(n) is divisible by 9, and 1997, and 4877

# analytical solution for F5(n) for n>5 is: (ignoring multiplication of 2 since 87654321 is not divisible by 2)
# 2^n - 16*n + 56 - 4*(n // 6) + p[n % 6]
# p = [1, 1, 1, 1, 0, -2]

# n split into 6 cases for analytic solution. Therefore n=6k + x. 2^n = 2^{6k} * 2^x

# Key facts
# 2^6 == 1 mod 9
# 2^1996 == 1 mod 1997
# 2^4876 == 1 mod 4877

# mod x -> 2^(6v) == 1 mod x -> given an x, easy to find smallest v
# mod 9    -> 6      = 6*1    = 6*v
# mod 1997 -> 1996*3 = 6*998  = 6*v
# mod 4877 -> 4876*3 = 6*2438 = 6*v

# Therefore the class of equivalence will be based on
# mod 9    -> 6*9         = 54
# mod 1997 -> 6*998*1997  = 11958036
# mod 4877 -> 6*2438*4877 = 71340756

# specifically
# Divisible by 9    -> n = 54t + {14, 24, 41, 43, 51, 52} for all t
# Divisible by 1997 -> n = 11958036t + {...} for all t
# Divisible by 4877 -> n = 71340756t + {...} for all t

# p = [1, 1, 1, 1, 0, -2]
# f(n) = 2**n - 16*n + 56 - 4*(n//6) + p[n % 6]
# n == a mod 6 -> n = 6k + a
# f(n) = 2**6k * 2**a - 16*(6k+a) + 56 - 4k + p[a] mod x
# k == b mod v -> k = rv + b
# f(n) = 2**a * 2**6rv * 2**6b - 16*(6k+a) + 56 - 4k + p[a] mod x = 0
# f(n) = 2**a * (2**6v)**(r) * 2**6b - 16*(6k+a) + 56 - 4k + p[a] mod x = 0
# f(n) = 2**a * 2**6b - 16*(6k+a) + 56 - 4k + p[a] mod x = 0
# f(n) = 2**(6b + a) - 16*(6b + a) - 16*6rv + 56 - 4(rv + b) + p[a] mod x = 0
# f(n) = 2**(6b + a) - 100(rv+b) - 16a  + 56 + p[a] mod x = 0
# f(n) = 2**(6b + a) - 100k - 16a  + 56 + p[a] mod x = 0
# 0<=a<6, 0<=b<v

# keep track of the following expression for n
# n = 6vr + 6b + a
# since this implied that F5(n) == 0 mod x

# example with x = 9 -> v = 1
# v=1 -> b=0 -> k=r, n = 6k + a
# f(n) = 2^a - 100r + 16a + 56 + p[a] mod 9 = 0
# 0<=a<6
# p = [1, 1, 1, 1, 0, -2]
# if a == 0 -> f(n) = 1 - 100r + 56 + 1 mod 9 = 0 -> r == 4 mod 9  -> n = 9*6t + 4*6 + 0 = 54t + 24
# if a == 1 -> f(n) = 2 - 100r + 16 + 56 + 1 mod 9 = 0 -> r == 7 mod 9  -> n = 9*6t + 7*6 + 1 = 54t + 43
# if a == 2 -> f(n) = 4 - 100r + 16*2 + 56 + 1 mod 9 = 0 -> r == 2 mod 9  -> n = 9*6t + 2*6 + 2 = 54t + 14
# if a == 3 -> f(n) = 8 - 100r + 16*3 + 56 + 1 mod 9 = 0 -> r == 8 mod 9  -> n = 9*6t + 8*6 + 3 = 54t + 51
# if a == 4 -> f(n) = 16 - 100r + 16*4 + 56 + 0 mod 9 = 0 -> r == 8 mod 9  -> n = 9*6t + 8*6 + 4 = 54t + 52
# if a == 5 -> f(n) = 32 - 100r + 16*5 + 56 - 2 mod 9 = 0 -> r == 6 mod 9  -> n = 9*6t + 6*6 + 5 = 54t + 41

# this logic is coded up efficiently in get_mod_equations method below

# using the numbers we kept track of, we have the following divisibility rules
# (for a in 0 to 5)
# Relations for divisibility by 9  (for all T1)
# n = dc_9[a] + 6*9*T1
# Relations for divisibility by 1997 (for all T2)
# n = dc_1997[a] + 6*998*1997*T2
# Relations for divisibility by 4877 (for all T3)
# n = dc_4877[a] + 6*2438*4877*T3

# when combining all of these modular equations together using the Chinese Remainder Theorem (allowing for co-primes),
# we get that the final modular equation will have a period of lcm(6*9, 6*998*1997,  6*2438*4877)
# period = 639821496386412 ~= 6e15
# this implies that for finding all values less than 1e18 which are divisible by 87654321 we only need to search within
# d = 1e18 mod 6e15


class Problem486:
    def __init__(self, debug_mode=False):
        # 87654321 = 9*1997*4877
        dc_9 = self.get_mod_equations(9)
        dc_1997 = self.get_mod_equations(1997)
        dc_4877 = self.get_mod_equations(4877)

        # Create final mod equation
        m1 = 6 * 1 * 9
        m2 = 6 * 998 * 1997
        m3 = 6 * 2438 * 4877
        self.period = lcm(lcm(m1, m2), m3)  # 639821496386412

        self.set_period = set()

        for a in range(6):
            s1 = dc_9[a]
            s2 = dc_1997[a]
            s3 = dc_4877[a]

            obj = ChineseRemainderTheoremSets([s1, s2, s3], n_list=[m1, m2, m3])
            sol_set = obj()
            self.set_period = self.set_period.union(sol_set)
            if debug_mode:
                print(f'created solution set for a={a}')

    @staticmethod
    def get_mod_equations(x):
        """
        f(n) = 2**(6b + a) - 100k + 16a  + 56 + p[a] mod x = 0
        0<=a<6, 0<=b<v
        n == a mod 6 -> n = 6k + a
        k == b mod v -> k = rv + b

        Examples:
            When x=9 is provided that should result in the following dictionary :
             {0: {24}, 1: {43}, 2: {14}, 3: {51}, 4: {52}, 5: {41}}
            Which should be interpreted as
            n = 54t + {14, 24, 41, 43, 51, 52}, for all t has f5(t) divisible by 9

            note that 54 = 9*6*v (since v is 1 for x=9)
        """
        if x == 9:
            v = 1  # 2^(6*1) == 1 mod 9
            inv_100 = 1  # 100*1 == 1 mod 9
            inv_v = 1  # 1*1 == 1 mod 9
        elif x == 1997:
            v = 998  # 2^(6*998) == 1 mod 1997
            inv_100 = 1338  # 100*1338 == 1 mod 1997
            inv_v = 1995  # 998*1995 == 1 mod 1997
        elif x == 4877:
            v = 2438  # 2^(6*2438) == 1 mod 4877
            inv_100 = 4243  # 100*4243 == 1 mod 4877
            inv_v = 4875  # 2438*4875 == 1 mod 4877
        elif x == 87654321:
            v = 1216562  # 2^(6*1216562) == 1 mod 87654321  # pow(2,6*1216562, 87654321)
            inv_100 = 16654321  # 100*16654321 == 1 mod 87654321
            inv_v = 80527988  # 1216562*80527988 == 1 mod 87654321
        else:
            raise NotImplementedError
        p = [1, 1, 1, 1, 0, -2]
        dc_sol = {}
        for a in range(6):
            dc_sol[a] = set()
            for b in range(v):
                # using:
                # f(n) = 2**(6b + a) - 100*(rv+b) - 16a  + 56 + p[a] == 0 mod x
                # re-arranging to solve for r, we get
                # r*100*v = 2**(6b + a) - 100b - 16a  + 56 + p[a] mod x
                # r = (2**(6b + a) - 100b - 16a  + 56 + p[a]) * inv_100 * inv_v  mod x
                rhs = 2 ** (6 * b + a) - 100 * b - 16 * a + 56 + p[a]
                r = (rhs * inv_100 * inv_v) % x
                # storing n = 6vr + 6b + a
                # since this implies that F5(n) == 0 mod x
                dc_sol[a].add(6*v*r + 6*b + a)
        return dc_sol

    @timeit
    def solve(self, d):
        """
        Return the number of integers n such that 5<=n<=d and F_5(n) is divisible by 87654321
        """
        num_sol = 0
        if d > self.period:
            multiple = (d // self.period)
            num_sol += multiple * len(self.set_period)
            d -= self.period * multiple

        num_sol += sum(x <= d for x in self.set_period)
        return num_sol


class Solution486(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problem = Problem486()

    def test_first_solution(self):
        self.assertEqual(1, self.problem.solve(d=95440424))
    #
    # def test_first_10_solution(self):
    #     self.assertEqual(10, self.problem.solve(d=879562681))
    #
    # def test_given_sample_solution(self):
    #     self.assertEqual(51, self.problem.solve(d=5*int(1e9)))  # takes around 0.7 seconds
    #
    # def test_first_100_solution(self):
    #     self.assertEqual(100, self.problem.solve(d=9524776956))  # takes around 1 seconds
    #
    # def test_first_200_solution(self):
    #     self.assertEqual(200, self.problem.solve(d=18010838498))  # takes around 0.5 seconds
    #
    # def test_first_300_solution(self):
    #     self.assertEqual(300, self.problem.solve(d=26168704503))  # takes around 0.6 seconds
    #
    # def test_first_400_solution(self):
    #     self.assertEqual(400, self.problem.solve(d=33855231633))  # takes around 0.6 seconds

    def test_larger_solution(self):
        self.assertEqual(11365, self.problem.solve(d=int(1e12)))

    def test_solution(self):
        self.assertEqual(11408450515, self.problem.solve(d=int(1e18)))  # takes around 1.5 seconds


if __name__ == '__main__':
    unittest.main()
