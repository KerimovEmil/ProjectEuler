"""
Let F5(n) be the number of strings s such that:
- s consists only of '0's and '1's,
- s has length at most n, and
- s contains a palindromic substring of length at least 5.

For example, F5(4) = 0, F5(5) = 8, F5(6) = 42 and F5(11) = 3844.

Let D(L) be the number of integers n such that 5 ≤ n ≤ L and F5(n) is divisible by 87654321.

For example, D(10^7) = 0 and D(5·10^9) = 51.

Find D(10^18).

ANSWER: ~
Solve time: ~
"""

from util.utils import timeit
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

# Key facts
# 2^6 == 1 mod 9
# 2^1996 == 1 mod 1997
# 2^4876 == 1 mod 4877

# Case 1: n = 6k, f(n) = 2*(2**n - 16*n + 56 - (2*n - 3)/3)
# f(k) = 2*((2^6)^k - 96k + 57 - 4k), since 2 is never divisible by 9, 1997, or 4877, we can focus on
# f(k) = (2^6)^k - 100k + 57

# find k such that f(k) == 0 mod 9
# k == 4  mod 9

# Case 2: n = 6k + 1, f(n) = 2*(2**n - 16*n + 56 - (2*n - 5)/3)
# f(k) = 2^1*(2^6)^k - 96k - 16 + 56 - (12k + 2 - 5)/3
# f(k) = 2^1*(2^6)^k - 100k + 41

# find k such that f(k) == 0 mod 9
# k == 7 mod 9

# Case 3: n = 6k + 2, f(n) = 2*(2**n - 16*n + 56 - (2*n - 7)/3)
# f(k) = 4*(2^6)^k - 100k + 25

# find k such that f(k) == 0 mod 9
# k == 2 mod 9

# Case 4: n = 6k + 3, f(n) = 2*(2**n - 16*n + 56 - (2*n - 9)/3)
# f(k) = 2^3*(2^6)^k - 96k - 48 + 56 - (12k + 6 - 9)/3
# f(k) = 8*(2^6)^k - 100k + 9

# find k such that f(k) == 0 mod 9
# k == 8 mod 9

# Case 5: n = 6k + 4, f(n) = ...
# f(k) = 2^4*(2^6)^k - 96k - 64 + 56 - 4k
# f(k) = 16*(2^6)^k - 100k - 8

# find k such that f(k) == 0 mod 9
# k == 8 mod 9

# Case 6: n = 6k + 5
# f(k) = 2^5*(2^6)^k - 96k - 80 + 56 - 4k - 2
# f(k) = 32*(2^6)^k - 100k - 26

# find k such that f(k) == 0 mod 9
# k == 6 mod 9


# Summary of mod 9 results
# n=6k + 0 -> k = 9t + 4 -> n = 54t + 24
# n=6k + 1 -> k = 9t + 7 -> n = 54t + 43
# n=6k + 2 -> k = 9t + 2 -> n = 54t + 14
# n=6k + 3 -> k = 9t + 8 -> n = 54t + 51
# n=6k + 4 -> k = 9t + 8 -> n = 54t + 52
# n=6k + 5 -> k = 9t + 6 -> n = 54t + 41

# n = 54t + {14, 24, 41, 43, 51, 52}, for all t has f5(t) divisible by 9

class Problem486:
    def __init__(self):

        # (for a in 0 to 5)
        # Relations for divisibility by 9  (for all T1)
        # n = dc_9_3[a] + 6*9*T1
        # Relations for divisibility by 1997 (for all T2)
        # n = dc_1997_3[a] + 6*998*1997*T2
        # Relations for divisibility by 4877 (for all T3)
        # n = dc_4877_3[a] + 6*2438*4877*T3

        self.dc_9_3 = self.get_mod_equations_3(9)
        self.dc_1997_3 = self.get_mod_equations_3(1997)
        self.dc_4877_3 = self.get_mod_equations_3(4877)

    @staticmethod
    def get_mod_equations_3(x):
        """
        f(n) = 2**(6b + a) - 100k + 16a  + 56 + p[a] mod x = 0
        0<=a<6, 0<=b<v
        n == a mod 6 -> n = 6k + a
        k == b mod v -> k = rv + b
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
                # 6 * (998 * (dc_1997_2[4][123] + 2 * 1997) + 123) + 4
                # 5988*dc_1997_2[a][b] + 6*b + a + 11958036*T
                dc_sol[a].add(6*v*r + 6*b + a)
        return dc_sol

    def get_sol_for_given_a(self, d=int(5e9), a=0):  # todo speed up
        """
        Return the number of integers n == a mod 6 such that 5<=n<=d and F_5(n) is divisible by 87654321
        n = 6k + a
        """
        s_1997 = set()
        s_4877 = set()

        for i in range(d // (6 * 2438 * 4877) + 1):
            s_4877 = s_4877.union({x + 6 * 2438 * 4877 * i for x in self.dc_4877_3[a]})
        for i in range(d // (6 * 998 * 1997) + 1):
            s_1997 = s_1997.union({x + 6 * 998 * 1997 * i for x in self.dc_1997_3[a]})

        w = s_4877.intersection(s_1997)
        y = []
        remainder_54 = list(self.dc_9_3[a])[0]  # there is only one element here todo think of better way
        for t in w:
            if (t - remainder_54) % 54 == 0:
                y.append(t)
        return len(y)

    @timeit
    def solve(self, d):
        total = 0
        for a in range(6):
            total += self.get_sol_for_given_a(d=d, a=a)
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
        self.assertEqual(51, self.problem.solve(d=5*int(1e9)))  # takes around 42 seconds


if __name__ == '__main__':
    unittest.main()


# mod 9 -> 54 = 6*9
# mod 1997 -> 11958036 = 6*1997*998
# mod 4877 -> 71340756 = 6*4877*2438

# n = 54t + {14, 24, 41, 43, 51, 52}, for all t has f5(t) divisible by 9

# 87654321 = 3^2×1997×4877
# 87654321 = 9 × 1997 × 4877

# n split into 6 cases for analytic solution. Therefore n=6k + x. 2^n = 2^{6k} * 2^x

# 2^6 == 1 mod 9
# 2^1996 == 1 mod 1997
# 2^4876 == 1 mod 4877

# mod 9    -> 6      = 6*1    = 6*v
# mod 1997 -> 1996*3 = 6*998  = 6*v
# mod 4877 -> 4876*3 = 6*2438 = 6*v
# mod x -> 2^(6v) == 1 mod x -> given an x, easy to find smallest v

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


# 6*dc_9_2[a][0] + a + 54*T1 = 5988*dc_1997_2[a][b] + 6*b + a + 11958036*T2
# 6*dc_9_2[a][0] + 54*T1 = 5988*dc_1997_2[a][b] + 6*b + 11958036*T2
# 6*dc_9_2[a][0] - 5988*dc_1997_2[a][b] = 6*b + 11958036*T2 - 54*T1
# 6*dc_9_2[a][0] - 5988*dc_1997_2[a][b] = 6(b + 1993006*T2 - 9*T1)
# dc_9_2[a][0] - 998*dc_1997_2[a][b] = b + 1993006*T2 - 9*T1
# dc_9_2[a][0] - 998*dc_1997_2[a][b] = b + 998*1997*T2 - 9*T1
# if b = 0
# -556880 = 998*1997*T2 - 9*T1, find T1 and T2 which work (if any??)
# 199300 = 22144*9 + 4
# 9 = 2*4 + 1
# 4 = 4*1 + 0
# 1	= (1 * 9) + (-2 * 4) = (-2 * 199300) + (44289 * 9)
# T2 = 111376, T1 = -1828601464





# r(a=0) = 10
# r(a=1) = 14
# r(a=2) = 10
# r(a=3) = 7
# r(a=4) = 6
# r(a=5) = 4
# total = 10 + 14 + 10 + 7 + 6 + 4 = 51


# r2(a=0)
# [604567122, 1312942470, 1325507676, 1549519224, 1776581556, 2182638390, 3065794620, 3475760406, 3585507468, 4559634096]

# r2(a=1)
# [318731749, 373915105, 576834685, 879562681, 1009360915, 1424736691, 1428145441, 1433492683, 2437447399, 3311243107,
# 3503520745, 3507223093, 3849723709, 4457322745]

# r2(a=2)
# [95440424, 101714738, 478919156, 1220169056, 2297654708, 2666828300, 3,423,823,034, 3,895,848,158,
# 4,146,707,480, 4,951,748,930]

# r2(a=3)
# [204995229, 238948971, 1155177015, 1703229765, 1957680303, 2724076113, 2874690537]

# r2(a=4)
# [2597051860, 2924804860, 3406650964, 3803677864, 3904467784, 4897807936]

# r2(a=5)
# [1646490281, 2463945899, 2880042143, 4098746111]


# Some test answer:
# D(95,440,424)=1
# D(879,562,681)=10
# D(9,524,776,956)=100
# D(18,010,838,498)=200
# D(26,168,704,503)=300
# D(33,855,231,633)=400
#
# These are first time they become this value, example: D(33855231632)=399


# (for a in 0 to 5)
# Relations for divisibility by 9  (for all T1)
# n = dc_9_3[a] + 6*9*T1
# Relations for divisibility by 1997 (for all T2)
# n = dc_1997_3[a] + 6*998*1997*T2
# Relations for divisibility by 4877 (for all T3)
# n = dc_4877_3[a] + 6*2438*4877*T3
# period = 639821496386412 = 6*9*998*1997*2438*4877 / 2
