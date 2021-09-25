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
# (2^6)^k - 96k + 57 - 4k == 0 mod 9
# 1 + 3k + 3 + 5k == 0 mod 9
# k == 4  mod 9

# find k such that f(k) == 0 mod 1997
# 2^(6k) - 100k + 57 == 0 mod 1997
# 2^(6k) + 1897k + 57 == 0 mod 1997
# k = 1996r + a
# 2^(11976r + 6a) + 1897k + 57 == 0 mod 1997
# 2^(11976r) * 2^(6a) + 1897k + 57 == 0 mod 1997
# 2^(1996 * 6 * r) * 2^(6a) + 1897k + 57 == 0 mod 1997
# 1^(6 * r) * 2^(6a) + 1897k + 57 == 0 mod 1997
# 2^(6a) + 1897k + 57 == 0 mod 1997
# 2^1996 == 1 mod 1997
# ...

# Case 2: n = 6k + 1, f(n) = 2*(2**n - 16*n + 56 - (2*n - 5)/3)
# f(k) = 2^1*(2^6)^k - 96k - 16 + 56 - (12k + 2 - 5)/3
# f(k) = 2^1*(2^6)^k - 100k + 41

# find k such that f(k) == 0 mod 9
# 2^1*(2^6)^k - 100k + 41 == 0 mod 9
# k == 7 mod 9

# find k such that f(k) == 0 mod 1997
# 2^1*(2^6)^k - 100k + 41 == 0 mod 1997
# ...

# find k such that f(k) == 0 mod 4877
# 2^1*(2^6)^k - 100k + 41 == 0 mod 4877
# ...

# Case 3: n = 6k + 2, f(n) = 2*(2**n - 16*n + 56 - (2*n - 7)/3)
# f(k) = 2^2*(2^6)^k - 96k - 32 + 56 - (12k + 4 - 7)/3
# f(k) = 4*(2^6)^k - 100k + 25

# find k such that f(k) == 0 mod 9
# 4*(2^6)^k - 100k + 25 == 0 mod 9
# 4k + 1 == 0 mod 9
# k == 2 mod 9

# find k such that f(k) == 0 mod 1997
# 4*(2^6)^k - 100k + 25 == 0 mod 1997
# ...

# find k such that f(k) == 0 mod 4877
# 4*(2^6)^k - 100k + 25 == 0 mod 4877
# ...

# Case 4: n = 6k + 3, f(n) = 2*(2**n - 16*n + 56 - (2*n - 9)/3)
# f(k) = 2^3*(2^6)^k - 96k - 48 + 56 - (12k + 6 - 9)/3
# f(k) = 8*(2^6)^k - 100k + 9

# find k such that f(k) == 0 mod 9
# 8k == 1 mod 9
# k == 8 mod 9

# find k such that f(k) == 0 mod 1997
# ... == 0 mod 1997
# ...

# find k such that f(k) == 0 mod 4877
# ... == 0 mod 4877
# ...

# Case 5: n = 6k + 4, f(n) = ...
# f(k) = 2^4*(2^6)^k - 96k - 64 + 56 - 4k
# f(k) = 16*(2^6)^k - 100k - 8

# find k such that f(k) == 0 mod 9
# k == 8 mod 9

# find k such that f(k) == 0 mod 1997
# ... == 0 mod 1997
# ...

# find k such that f(k) == 0 mod 4877
# ... == 0 mod 4877
# ...

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
