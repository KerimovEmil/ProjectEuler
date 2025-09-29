"""
PROBLEM

It can be shown that the polynomial n^4 + 4n^3 + 2n^2 + 5n is a multiple of 6 for every integer n.
It can also be shown that 6 is the largest integer satisfying this property.

Define M(a, b, c) as the maximum m such that n^4 + an^3 + bn^2 + cn is a multiple of m for all integers n.
For example, M(4, 2, 5) = 6.

Also, define S(N) as the sum of M(a, b, c) for all 0 < a, b, c ≤ N.

We can verify that S(10) = 1972 and S(10000) = 2024258331114.

Let Fk be the Fibonacci sequence:
F_0 = 0, F_1 = 1 and
F_k = F_{k-1} + F_{k-2} for k ≥ 2.

Find the last 9 digits of ∑ S(F_k) for 2 ≤ k ≤ 1234567890123.

ANSWER: 356019862
Solve time: ? seconds
"""

from util.utils import timeit
import unittest
from util.utils import primes_upto as primes


# f = lambda n: n**4 + 4*n**3 + 2*n**2 + 5*n

# after getting s(10000), need to look into
# https://en.wikipedia.org/wiki/Pisano_period for fib sum
# Fib(n) mod 1e9 is periodic with period 1.5e9 (pisano period)
# S(n) is periodic mod 1e9 with period ?

def q(max_sum):
    """Generator of sums of (a+b+c) such that the max integer is not exactly 1 or 2"""
    i = 2
    while i <= max_sum:
        i += 1
        if i > max_sum:
            break
        yield i
        i += 2
        if i > max_sum:
            break
        yield i
        i += 2
        if i > max_sum:
            break
        yield i
        i += 1
        if i > max_sum:
            break
        yield i
        i += 3
        if i > max_sum:
            break
        yield i
        i += 3
        if i > max_sum:
            break
        yield i


def ones(max_sum):
    """Generator of sums of (a+b+c) such that the max integer is exactly 1"""
    i = 0
    while i <= max_sum:
        i += 4
        if i > max_sum:
            break
        yield i
        i += 2
        if i > max_sum:
            break
        yield i


def twos(max_sum):
    """Generator of sums of (a+b+c) such that the max integer is exactly 2"""
    i = 1
    while i <= max_sum:
        i += 8
        if i > max_sum:
            break
        yield i
        i += 4
        if i > max_sum:
            break
        yield i


def M(a, b, c):
    """Get max divisor integer"""
    # by observation, M can only have up to 3 powers of 2 and up to 1 power of 3
    # todo come up with a proof for this
    return M3(a, b, c) * M8(a, b, c)


def M3(a, b, c):
    """Get max divisor integer power of 3"""
    if is_module(a, b, c, 3):
        return 3
    else:
        return 1


def M8(a, b, c):
    """Get max divisor integer power of 2 up to 2^3"""
    if is_module(a, b, c, 8):
        return 8
    elif is_module(a, b, c, 4):
        return 4
    elif is_module(a, b, c, 2):
        return 2
    else:
        return 1


def is_module(a, b, c, m):
    for n in range(1, m):
        p = n*(n*(n*(n+a)+b)+c)
        if p % m:
            return False
    return True


# def is_module(a, b, c, m):
#     for i in range(1, m):
#         val = ((i ** 4) % m) + a * ((i ** 3) % m) + b * ((i ** 2) % m) + c * i
#         if val % m != 0:
#             return False
#     return True


def max_int(a, b, c):
    # f(-1) is max value to try (min(f(-1), f(1))
    # f(1) = 1 + a + b + c
    # f(-1) = 1 - a + b - c
    # f(-2) = 16 - 8*a + 4*b - 2*c
    f_neg_1 = abs(1 - a + b - c)
    if f_neg_1 != 0:
        max_modular = f_neg_1
    else:
        f_pos_1 = 1 + a + b + c
        max_modular = f_pos_1

    max_modular = min(max_modular, 24)  # check this condition

    for module in range(max_modular, 0, -1):
        if is_module(a % module, b % module, c % module, module):
        # if M(a % module, b % module, c % module):
            return module
    print(f'oh no, {a}, {b}, {c}')


class Problem402:
    def __init__(self):
        pass

    @staticmethod
    def old_s(max_coeff):
        going_sum = 0
        for a in range(1, max_coeff+1):
            print(f'a={a}')
            for b in range(1, max_coeff+1):
                print(f'b={b}')
                for c in range(1, max_coeff+1):
                    # going_sum += max_int(a, b, c)
                    going_sum += M(a, b, c)
        return going_sum

    @staticmethod
    def s(max_coeff):
        going_sum = 0

        a_range = lambda coeff_sum: range(max(coeff_sum - 2*max_coeff, 1), min(max_coeff+1, coeff_sum-1))

        # if max = 10
        # 9-nomial coefficient array: Coefficients of the polynomial (1+...+X^8)^n, n=0,1,...

        # if max = 11
        # 10-nomial coefficient array: Coefficients of the polynomial (1 + ... + X^9)^n, n=0,1,...

        # add ones
        for coeff_sum in ones(3*max_coeff):
            print(f'ones coeff_sum={coeff_sum}')
            for a in a_range(coeff_sum):
                max_b = min(max_coeff, coeff_sum-a-1)
                min_b = max(coeff_sum-a-max_coeff, 1)
                going_sum += (max_b - min_b) + 1

        # add twos
        for coeff_sum in twos(3*max_coeff):
            print(f'twos coeff_sum={coeff_sum}')
            for a in a_range(coeff_sum):
                max_b = min(max_coeff, coeff_sum-a-1)
                min_b = max(coeff_sum-a-max_coeff, 1)
                going_sum += 2*((max_b - min_b) + 1)

        for coeff_sum in q(3*max_coeff):
            print(f'q coeff_sum={coeff_sum}')
            for a in a_range(coeff_sum):
                # print(f'  a={a}')
                for b in range(min(max_coeff, coeff_sum-a-1), 0, -1):
                    # print(f'    b={b}')
                    c = coeff_sum - a - b
                    if c > max_coeff:
                        break
                    # print(f'      c={c}')
                    going_sum += M(a, b, c)
        return going_sum

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution402(unittest.TestCase):
    def setUp(self):
        self.problem = Problem402()

    def test_is_modular(self):
        self.assertEqual(True, is_module(a=4, b=2, c=5, m=6))

    def test_max_multiple(self):
        self.assertEqual(6, max_int(a=4, b=2, c=5))

    def test_solution(self):
        self.assertEqual(1972, self.problem.s(10))

    def test_solution_2(self):
        # S(10000) = 2024258331114
        self.assertEqual(2024258331114, self.problem.s(10000))


if __name__ == '__main__':
    unittest.main()

