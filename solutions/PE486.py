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
        x = 0
        while x < 2 ** n:
            yield bin(x)[2:].rjust(n, '0')
            x += 1
    else:
        yield ''


def gen_strings(n=6):
    options = set()
    for i in range(5, n + 1):
        for x in gen_palindrome(i):
            options.add(x)
            num_free = n - i
            for numprefix in range(0, num_free+1):
                for numsuffix in range(num_free - numprefix + 1):
                    for prefix in yield_all_binary(numprefix):
                        for suffix in yield_all_binary(numsuffix):
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


p = [3, 5, 7, 9, 8, 4]


def f5(n):
    t = 2**n - 16*n + 56 - (2*n - p[n % 6]) // 3
    if n == 5:
        t -= 2
    return 2*t


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

