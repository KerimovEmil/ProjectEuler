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
    # p = [3, 5, 7, 9, 8, 4]
    # t = 2**n - 16*n + 56 - (2*n - p[n % 6]) // 3

    p = [1, 1, 1, 1, 0, -2]
    k = n // 6
    t = 2**n - 16*n + 56 - 4*k + p[n % 6]
    if n == 5:
        t -= 2
    return 2*t

# the link between both solutions
# (2*n - p[n % 6]) / 3
# n = 6k + 0 -> (12k + 0 - 3)/3 = 4k - 1
# n = 6k + 1 -> (12k + 2 - 5)/3 = 4k - 1
# n = 6k + 2 -> (12k + 4 - 7)/3 = 4k - 1
# n = 6k + 3 -> (12k + 6 - 9)/3 = 4k - 1
# n = 6k + 4 -> (12k + 8 - 8)/3 = 4k
# n = 6k + 5 -> (12k + 10 - 4)/3 = 4k + 2


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

# find k such that f(k) == 0 mod 1997
# 2^(6k) - 100k + 57 == 0 mod 1997
# 2^(6k) + 1897k + 57 == 0 mod 1997
# n = 6k
# k = 998r + a -> k==a mod 998
# 2^(5988 + 6a) + 1897k + 57 == 0 mod 1997
# 2^(1996 * 3 * r) * 2^(6a) + 1897k + 57 == 0 mod 1997
# 1^(3 * r) * 2^(6a) + 1897k + 57 == 0 mod 1997
# 2^(6a) + 1897k + 57 == 0 mod 1997
# 2^(6a) + 1897*(998r + a) + 57 == 0 mod 1997
# 2^(6a) + 1893206r + 1897a + 57 == 0 mod 1997
# 2^(6a) + 50r + 1897a + 57 == 0 mod 1997
# 2^(6a) + 50r - 100a + 57 == 0 mod 1997
# ...
# ...

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

# find k such that f(k) == 0 mod 1997
# ... == 0 mod 1997
# ...

# find k such that f(k) == 0 mod 4877
# ... == 0 mod 4877
# ...

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
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


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

    # def test_solution(self):
    #     self.assertEqual(51, self.problem.solve(5*int(1e9)))


if __name__ == '__main__':
    unittest.main()


def g(n):
    return 2**n - 100*n//6 + 57
    # return 64**k - 100*k + 57
    # return 64**(9t + 4) - 100*(9t + 4) + 57
    # return 16777216 * 18014398509481984**(t) - 900*t - 343

def h(t):
    return 16777216 * 18014398509481984**t - 900*t - 343

def h_1997(t):
    return (419 * 782**t - 900*t - 343) % 1997

def h_4877(t):
    return (336 * 2507**t - 900*t - 343) % 4877

# L = 5*int(1e9)
# n = 6k
# k = 9t + 4
# n = 54t + 24
# n==0 mod 6 -> n=6k
# k==4 mod 9 -> k=9t + 4

# for t in range(10000):
# # for t in range((L - 24) // 54 + 1):
#     # fn = g(54 * t + 24)
#     fn = h(t)
#     assert fn % 9 == 0
#     if fn % 1997 == 0:
#         k = 9 * t + 4  # case 1, k==4 mod 9
#         n = 6 * k  # case 1, n==0 mod 6
#         assert fn % 9 == 0
#         # print(f'1997, n={n}, k={k}, t={t}, f(n)={fn}')
#         print(f'1997, n={n}, k={k}, t={t}')
#     if fn % 4877 == 0:
#         k = 9 * t + 4
#         n = 6 * k
#         assert fn % 9 == 0
#         # print(f'4877, n={n}, k={k}, t={t}, f(n)={fn}')
#         print(f'4877, n={n}, k={k}, t={t}')

# 4877, n=69846, k=11641, t=1293
# 4877, n=99870, k=16645, t=1849
# 1997, n=134214, k=22369, t=2485
# 1997, n=163914, k=27319, t=3035
# 4877, n=199608, k=33268, t=3696
# 1997, n=206034, k=34339, t=3815
# 1997, n=417768, k=69628, t=7736
# 1997, n=434724, k=72454, t=8050


# for t in range((L - 24) // 54 + 1):
# for t in range(10000):
#     if h_1997(t) == 0:
#         k = 9 * t + 4  # case 1, k==4 mod 9
#         n = 6 * k  # case 1, n==0 mod 6
#         print(f'1997, n={n}, k={k}, t={t}')
#     if h_4877(t) == 0:
#         k = 9 * t + 4
#         n = 6 * k
#         print(f'4877, n={n}, k={k}, t={t}')

# ls_n = []
# ls_k = []
# ls_t = []
# for t in range(15000):
#     if h_1997(t) == 0:
#         k = 9 * t + 4  # case 1, k==4 mod 9
#         n = 6 * k  # case 1, n==0 mod 6
#         print(f'1997, n={n}, k={k}, t={t}')
#         ls_t.append(t)
#         ls_k.append(k)
#         ls_n.append(n)
# print(ls_n)
# print(ls_k)
# print(ls_t)

# 1997, values of t, s.t. h(t) is divisible by 1997
# 1997, n=134214, k=22369, t=2485
# 1997, n=163914, k=27319, t=3035
# 1997, n=206034, k=34339, t=3815
# 1997, n=417768, k=69628, t=7736
# 1997, n=434724, k=72454, t=8050
# 1997, n=632850, k=105475, t=11719
# 1997, n=733506, k=122251, t=13583
# 1997, n=749220, k=124870, t=13874
# 1997, n=764880, k=127480, t=14164
# 1997, n=861216, k=143536, t=15948
# 1997, n=928122, k=154687, t=17187
# 1997, n=982392, k=163732, t=18192
# 1997, n=1026294, k=171049, t=19005
# 1997, n=1369734, k=228289, t=25365
#


# mod 9 -> 54 = 6*9
# mod 1997 -> 11958036 = 6*1997*998
# mod 4877 -> 71340756 = 6*4877*2438

# n = 54t + {14, 24, 41, 43, 51, 52}, for all t has f5(t) divisible by 9

def find(m, v):
    ls = []
    for i in range(v):
        ans = f5(i)
        if ans % m == 0:
            ls.append(i)
    return ls
# find(9, 54) -> [14, 24, 41, 43, 51, 52]
# -> n = 54t + {14, 24, 41, 43, 51, 52}, for all t has f5(t) divisible by 9

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


def get_mod_equations(x):
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
    for b in range(v):
        dc_sol[b] = {}
        for a in range(6):
            rhs = 2 ** (6 * b + a) - 100 * b - 16 * a + 56 + p[a]
            r = (rhs * inv_100 * inv_v) % x
            dc_sol[b][a] = r
    return dc_sol


def get_mod_equations_2(x):
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
        dc_sol[a] = {}
        for b in range(v):
            rhs = 2 ** (6 * b + a) - 100 * b - 16 * a + 56 + p[a]
            r = (rhs * inv_100 * inv_v) % x
            dc_sol[a][b] = r
    return dc_sol


dc_9 = get_mod_equations(9)
dc_1997 = get_mod_equations(1997)
dc_4877 = get_mod_equations(4877)

# from util.utils import ChineseRemainderTheorem
# theorem = ChineseRemainderTheorem()
# theorem.solve(a_list=[0, 3, 4], n_list=[3, 4, 5])  # solves

dc_9_2 = get_mod_equations_2(9)
dc_1997_2 = get_mod_equations_2(1997)

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
# 6*dc_9_2[a][0] + a + 54*T

# Relations for divisibility by 1997 (for a in 0 to 5) (for b in 0 to 997) (v-1 = 997) (for all T)
# 6*(998*(dc_1997_2[a][b] + T*1997) + b) + a
# 5988*dc_1997_2[a][b] + 5988*T*1997 + 6*b + a
# 5988*dc_1997_2[a][b] + 6*b + a + 11958036*T
