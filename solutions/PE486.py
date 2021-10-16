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
Solve time: 1 minute and 42 seconds  # todo make faster
"""

from util.utils import timeit, lcm
from util.crt import ChineseRemainderTheoremSets
import unittest


# brute force method

def yield_all_binary(n):
    if n > 0:
        for i in range(2 ** n):
            yield bin(i)[2:].rjust(n, '0')
    else:
        yield ''


def gen_strings(n=6):
    options = set()
    for i in range(5, n + 1):
        for x in gen_palindrome(i):
            options.add(x)
            num_free = n - i
            for num_prefix in range(0, num_free+1):
                for num_suffix in range(num_free - num_prefix + 1):
                    for prefix in yield_all_binary(num_prefix):
                        for suffix in yield_all_binary(num_suffix):
                            options.add(prefix + x + suffix)
    return options


def gen_palindrome(n):
    num_fixed = n // 2
    num_free = (n + 1) // 2

    free_options = yield_all_binary(num_free)
    for x in free_options:
        yield x + x[:num_fixed][::-1]


def brute_force_f5(n):
    return len(gen_strings(n))


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

# example with x = 9 -> v = 1
# v=1 -> b=0 -> k=r, n = 6k + a
# f(n) = 2^a - 100r + 16a + 56 + p[a] mod 9 = 0
# 0<=a<6
# p = [1, 1, 1, 1, 0, -2]
# if a == 0 -> f(n) = 1 - 100r + 56 + 1 mod 9 = 0 -> r == 4 mod 9
# if a == 1 -> f(n) = 2 - 100r + 16 + 56 + 1 mod 9 = 0 -> r == 7 mod 9
# if a == 2 -> f(n) = 4 - 100r + 16*2 + 56 + 1 mod 9 = 0 -> r == 2 mod 9
# if a == 3 -> f(n) = 8 - 100r + 16*3 + 56 + 1 mod 9 = 0 -> r == 8 mod 9
# if a == 4 -> f(n) = 16 - 100r + 16*4 + 56 + 0 mod 9 = 0 -> r == 8 mod 9
# if a == 5 -> f(n) = 32 - 100r + 16*5 + 56 - 2 mod 9 = 0 -> r == 8 mod 9

# this logic is coded up efficiently in get_mod_equations method below

class Problem486:
    def __init__(self):
        self.dc_9 = self.get_mod_equations(9)
        self.dc_1997 = self.get_mod_equations(1997)
        self.dc_4877 = self.get_mod_equations(4877)

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
            v = 1
            inv_100 = 1
            inv_v = 1
        elif x == 1997:
            v = 998
            inv_100 = 1338
            inv_v = 1995
        elif x == 4877:
            v = 2438
            inv_100 = 4243
            inv_v = 4875
        else:
            raise NotImplementedError
        p = [1, 1, 1, 1, 0, -2]
        dc_sol = {}
        for a in range(6):
            dc_sol[a] = set()
            for b in range(v):
                rhs = 2 ** (6 * b + a) - 100 * b - 16 * a + 56 + p[a]
                r = (rhs * inv_100 * inv_v) % x
                dc_sol[a].add(6*v*r + 6*b + a)
        return dc_sol

    def get_sol_for_given_a_fast_under_1e11(self, d=int(5e9), a=0):  # todo speed up
        """
        Return the number of integers n == a mod 6 such that 5<=n<=d and F_5(n) is divisible by 87654321
        n = 6k + a
        """
        # todo based on these two linear congruences, combine to one linear congruence
        # e.g. x==3 mod 4 and x == 5 mod 21 -> x == 47 mod 84

        y = []
        remainder_54 = list(self.dc_9[a])[0]  # todo fix
        for x in self.dc_4877[a]:
            start = (-(x - remainder_54)//6) % 9  # since (6 * 2438 * 4877) mod (6*9) == 6
            for i in range(start, (d-x) // (6 * 2438 * 4877) + 1, 9):
                num = x + 6 * 2438 * 4877 * i
                # todo use fact that each one x corresponds to exactly one value in self.dc_1997[a]
                if num % (6 * 998 * 1997) in self.dc_1997[a]:  # filter out based on dc_1997
                    y.append(num)
        return len(y)

    def get_sol_for_given_a(self, d=int(5e9), a=0):  # todo speed up
        """
        Return the number of integers n == a mod 6 such that 5<=n<=d and F_5(n) is divisible by 87654321
        n = 6k + a
        """

        m1 = 9 * 6
        m2 = 6 * 998 * 1997
        m3 = 6 * 2438 * 4877

        s1 = self.dc_9[a]  # much smaller
        s2 = self.dc_1997[a]
        s3 = self.dc_4877[a]

        # todo think of speeding up by filtering congruences that won't have any solutions
        obj_1 = ChineseRemainderTheoremSets([s1, s2], n_list=[m1, m2])
        sol_set_1 = obj_1()
        period_1 = lcm(m1, m2)
        print(f'created first solution set for a={a}')

        obj_2 = ChineseRemainderTheoremSets([sol_set_1, s3], n_list=[period_1, m3])  # todo split by even and odd
        sol_set_2 = obj_2()
        period_2 = lcm(period_1, m3)
        print(f'created second solution set for a={a}')

        num_sol = 0
        if d > period_2:
            multiple = (d // period_2)
            num_sol += multiple * len(sol_set_2)
            d -= period_2 * multiple

        num_sol += sum(x <= d for x in sol_set_2)

        print(f'added up all values under d for a={a}')
        return num_sol

    @timeit
    def solve(self, d):
        total = 0

        m1 = 9 * 6
        m2 = 6 * 998 * 1997
        m3 = 6 * 2438 * 4877
        period = lcm(lcm(m1, m2), m3)

        if d < period:
            func = self.get_sol_for_given_a_fast_under_1e11
        else:
            func = self.get_sol_for_given_a

        for a in range(6):
            total += func(d=d, a=a)
        return total


class Solution486(unittest.TestCase):
    def setUp(self):
        self.problem = Problem486()

    def test_brute_force_against_samples(self):
        with self.subTest('n=5'):
            self.assertEqual(brute_force_f5(5), 8)
        with self.subTest('n=6'):
            self.assertEqual(brute_force_f5(6), 42)
        with self.subTest('n=11'):
            self.assertEqual(brute_force_f5(11), 3844)

    def test_brute_force_against_analytic_solution(self):
        for i in range(5, 15):
            with self.subTest(f'n={i}'):
                self.assertEqual(brute_force_f5(i), f5(i))

    def test_smaller_solution(self):
        self.assertEqual(1, self.problem.solve(d=95440424))

    def test_smaller_solution_2(self):
        self.assertEqual(10, self.problem.solve(d=879562681))

    def test_given_sample_solution(self):
        self.assertEqual(51, self.problem.solve(d=5*int(1e9)))  # takes around 0.7 seconds

    def test_first_100_solution(self):
        self.assertEqual(100, self.problem.solve(d=9524776956))  # takes around 1 seconds

    def test_first_200_solution(self):
        self.assertEqual(200, self.problem.solve(d=18010838498))  # takes around 0.5 seconds

    def test_first_300_solution(self):
        self.assertEqual(300, self.problem.solve(d=26168704503))  # takes around 0.6 seconds

    def test_first_400_solution(self):
        self.assertEqual(400, self.problem.solve(d=33855231633))  # takes around 0.6 seconds

    # def test_larger_solution(self):
    #     self.assertEqual(11365, self.problem.solve(d=int(1e12)))  # takes around 8.7 seconds

    def test_solution(self):
        self.assertEqual(11408450515, self.problem.solve(d=int(1e18)))  # takes around 1 min 42 seconds


if __name__ == '__main__':
    unittest.main()




# Summary of mod 9 results
# n=6k + 0 -> k = 1r + 0 -> r = 9t + 4 -> n = 54t + 24
# n=6k + 1 -> k = 1r + 0 -> r = 9t + 7 -> n = 54t + 43
# n=6k + 2 -> k = 1r + 0 -> r = 9t + 2 -> n = 54t + 14
# n=6k + 3 -> k = 1r + 0 -> r = 9t + 8 -> n = 54t + 51
# n=6k + 4 -> k = 1r + 0 -> r = 9t + 8 -> n = 54t + 52
# n=6k + 5 -> k = 1r + 0 -> r = 9t + 6 -> n = 54t + 41


# if a == 0 (i.e. n = 6k)

# f5(6*dc_9_2[0][0]) % 9 == 0
# f5(6*(dc_9_2[3][0] + 9) + 3) % 9 == 0
# f5(6*998*dc_1997_2[0][0]) % 1997 == 0
# f5(6*998*dc_1997_2[0][1] + 6*1) % 1997 == 0
# f5(6*998*dc_1997_2[0][5] + 6*5) % 1997 == 0
# f5(6*998*dc_1997_2[4][5] + 6*5 + 4) % 1997 == 0
# f5(6*998*dc_1997_2[4][123] + 6*123 + 4) % 1997 == 0
# f5(6*(998*(dc_1997_2[4][123] + 1997) + 123) + 4) % 1997 == 0
# f5(6*(998*(dc_1997_2[4][123] + 2*1997) + 123) + 4) % 1997 == 0
# n == a mod 6 -> n = 6k + a
# k == b mod v -> k = rv + b
# n = 6k + a = 6(rv + b) + a
# n = 6vr + 6b + a

# Relations for divisibility by 9 (for a in 0 to 5) (for b in 0 to 0) (v-1 = 0) (for all T)
# 6*(dc_9_2[a][0] + T*9) + a
# 6*dc_9_2[a][0] + a + 6*9*T
# 6*dc_9_2[a][0] + a + 54*T

# Relations for divisibility by 1997 (for a in 0 to 5) (for b in 0 to 997) (v-1 = 997) (for all T)
# 6*(998*(dc_1997_2[a][b] + T*1997) + b) + a
# 6*998*dc_1997_2[a][b] + 6*b + a + 6*998*1997*T
# 5988*dc_1997_2[a][b] + 6*b + a + 11958036*T

# Relations for divisibility by 4877 (for a in 0 to 5) (for b in 0 to 2437) (for all T)
# 6*(2438*(dc_4877_2[a][b] + T*4877) + b) + a
# 6*2438*dc_4877_2[a][b] + 6*b + a + 6*2438*4877*T
# 14628*dc_4877_2[a][b] + 6*b + a + 71340756*T


# (for a in 0 to 5)
# Relations for divisibility by 9  (for all T1)
# n = dc_9[a] + 6*9*T1
# Relations for divisibility by 1997 (for all T2)
# n = dc_1997[a] + 6*998*1997*T2
# Relations for divisibility by 4877 (for all T3)
# n = dc_4877[a] + 6*2438*4877*T3
# period = 639821496386412 = 6*9*998*1997*2438*4877 / 2
