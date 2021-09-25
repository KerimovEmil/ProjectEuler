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
    p = [3, 5, 7, 9, 8, 4]
    t = 2**n - 16*n + 56 - (2*n - p[n % 6]) // 3
    if n == 5:
        t -= 2
    return 2*t


# Let D(L) be the number of integers n such that 5 ≤ n ≤ L and F5(n) is divisible by 87654321 = 3^2 × 1997 × 4877
# Figure out when F5(n) is divisible by 9, and 1997, and 4877

# Key facts
# 2^6 == 1 mod 9
# 2^999 == 1 mod 1997
# 2^4875 == 1 mod 4877

# Case 1: n = 6k, f(n) = 2*(2**n - 16*n + 56 - (2*n - 3)/3)
# f(k) = 2*((2^6)^k - 96k + 57 - 4k), since 2 is never divisible by 9, 1997, or 4877, we can focus on
# f(k) = (2^6)^k - 96k + 57 - 4k

# find k such that f(k) == 0 mod 9
# (2^6)^k - 96k + 57 - 4k == 0 mod 9
# 1 + 3k + 3 + 5k == 0 mod 9
# k == 4  mod 9

# find k such that f(k) == 0 mod 1997
# (2^6)^k - 96k + 57 - 4k == 0 mod 1997
# ...

# Case 2: n = 6k + 1, f(n) = 2*(2**n - 16*n + 56 - (2*n - 5)/3)
# f(k) = 2^1*(2^6)^k - 96k - 16 + 56 - (12k + 2 - 5)/3
# f(k) = 2^1*(2^6)^k - 100k + 41

# find k such that f(k) == 0 mod 9
# 2^1*(2^6)^k - 100k + 41 == 0 mod 9
# 4k == 1 mod 9
# k == 7 mod 9

# find k such that f(k) == 0 mod 1997
# 2^1*(2^6)^k - 100k + 41 == 0 mod 1997
# ...

# find k such that f(k) == 0 mod 4877
# 2^1*(2^6)^k - 100k + 41 == 0 mod 4877
# ...

# Case 3: n = 6k + 2, f(n) = 2*(2**n - 16*n + 56 - (2*n - 7)/3)


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
            with self.subTest('n=5'):
                self.assertEqual(brute_force_f5(i), f5(i))

    # def test_solution(self):
    #     self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

