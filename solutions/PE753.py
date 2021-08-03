from util.utils import timeit
import unittest
from numpy import pi, exp, arange, cos
from primesieve import primes
import numpy as np

def r(a, p):
    np_range = arange(1, p//2 + 1)
    return cos(2*pi/p * a * np_range**3)

# returns -0.5
# np.array([r(a, 13) for a in range(1, 13//2 + 1)]).sum(axis=0)


# for p in primes(3, 100):
#     if p % 3 == 1:
#         p_pi_2 = 2 * pi / p
#         np_range = arange(1, p // 2 + 1)
#
#         f = -(16 * sum(sum(cos(p_pi_2 * a * np_range ** 3)) ** 3 for a in np_range) / (p - 1) + 1) / p
#         form_f = int(round(f, 4))
#         print(p, form_f, given_p(p), p ** 2 - 3 * p + 2 - form_f * (p - 1))


# 7 5 2
# 13 11 4
# 19 -1 6
# 31 2 10
# 37 17 12
# 43 14 14
# 61 5 20
# 67 11 22
# 73 -1 24
# 79 23 26
# 97 -13 32


# for p in primes(3,100):
#     if p%3 == 1:
#         p_pi_2 = 2 * pi/p
#         np_range = arange(1, p//2 + 1)
#         cos_sum = 16 * sum(sum(cos(p_pi_2 * a * np_range ** 3)) ** 3 for a in np_range)
#         f = -(cos_sum / (p - 1) + 1) / p
#         form_f = int(round(f, 4))
#         form_cossum_3 = int(round(cos_sum/3, 4))
#         print(p, form_f, form_f+p, (form_f+p)//3,(p-1)/3 , given_p(p), p**2- 3*p + 2 - form_f*(p-1), cos_sum, cos_sum/(p-1)/3/3)


# def int_print(*args):
#     ls = []
#     for x in args:
#         if abs(int(round(x, 4)) - x) <= 1e-3:
#             ls.append(int(round(x, 4)))
#         else:
#             raise NotImplementedError(f'{x} is not an integer')
#     print(ls)
#
# for p in primes(3,100):
#     if p%3 ==1:
#         np_range = arange(1, p//2 + 1)
#         cos_sum = 16 * sum(sum(cos(2 * pi/p * a * np_range ** 3)) ** 3 for a in np_range)
#         f = -(cos_sum / (p - 1) + 1) / p
#         int_print(p, given_p(p), f, cos_sum, cos_sum/(p-1)/9)

# for p in primes(3,200):
#     if p%3 ==1:
#         np_range = arange(1, p//2 + 1)
#         cos_sum = 16 * sum(sum(cos(2 * pi/p * a * np_range ** 3)) ** 3 for a in np_range)
#         f = -cos_sum / (p - 1)/p - 1/ p
#         g_p = (p-1)**3/p + cos_sum/p
#         int_print(p, f, cos_sum/(p-1)/9 + 2*p, g_p/(p-1)/9, (p//3)/2)


class Problem753:
    def __init__(self):
        pass

    @staticmethod
    def given_p_simple(p: int) -> int:
        if p % 3 != 1:
            return (p-1)*(p-2)

        dc_c_values = {}
        for i in range(1, p):
            i3 = i ** 3 % p
            dc_c_values[i3] = 1 + dc_c_values.get(i3, 0)

        ans = 0

        for i in range(1, p):
            cubed_sum = (2*i**3) % p
            ans += dc_c_values.get(cubed_sum, 0)

        for i in range(1, p):
            for j in range(i+1, p):
                cubed_sum = (i**3 + j**3) % p
                ans += 2*dc_c_values.get(cubed_sum, 0)

        return ans

    @staticmethod
    def given_p_simple_2(p: int) -> int:
        """
        Only called when p%3 == 1.
        Returns (p-1)* number of solutions to (a^3 + 1 = c^3)
        """
        # if p % 3 != 1:
        #     return (p-1)*(p-2)

        set_c_values = {i ** 3 % p for i in range(1, p)}  # there are 3 values of i for each one value of i^3

        ans = 3* sum((i**3 + 1) % p in set_c_values for i in range(1, p))

        # ans = 0
        # for i in range(1, p):
        #     cubed_sum = (i**3 + 1) % p
        #     if cubed_sum in set_c_values:
        #         ans += 3

        return ans*(p-1)

    @staticmethod
    def given_p(p: int) -> int:
        if p % 3 != 1:
            return (p-1)*(p-2)

        # given_p must be divisible by (p-1)

        # therefore p-1 must be divisible by 3
        # therefore cos_sum must be divisible by 3

        # magic_number = None
        # return (p**2 - 3*p + 2) - magic_number*(p-1)
        # return p(p - 3) + 2 - magic_number*(p-1)

        p_pi_2 = 2 * pi/p
        np_range = arange(1, p//2 + 1)

        ans = (p-1)**3
        ans += 16*sum(sum(cos(p_pi_2 * a * np_range**3))**3 for a in np_range)
        # cos sum is divisible by 9*(p-1)

        # (-16*cos_sums/(p-1) -1) /p must be an integer

        # for 37, = (-0.5) * len(np_range) * (37//3) * 210
        # for 37, = (-0.5) * len(np_range) * 2520
        # for 43, = (-0.5) * len(np_range) * 2412
        # for 43, final answer is 1134
        # for 43, 1134 = ((43-1)^3 + (-0.5) * len(np_range) * 2412) / 43
        # for 43, 1134 = (43^3 - 3*43^2 + 3*43 -1 + (-0.5) * len(np_range) * 2412) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) + (-1 + (-0.5) * len(np_range) * 2412) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) + (-1 + (-0.5) * (43-1)/2 * 2412) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) + (-1 - (43-1)/4 * 2412) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) + (-1 - (43-1) * 603) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) + (-(43-1) * 603 - 1) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) + (-43* 603 + 1*603 - 1) / 43
        # for 43, 1134 = (43^2 - 3*43 + 3) - 603 + (603 - 1) / 43
        #  (603 - 1) / 43 = 14 = 43 // 3
        # for 43, 1134 = (43**2 - 3*43 + 3) - (43*(43//3) +1) + (43//3)

        # for 37, final answer is 648
        # for 37, 648 = ((37-1)**3 + (-0.5) * (37-1)/2 * 2520) / 37
        # for 37, 648 = ((37-1)**3 - (37-1) * 630) / 37
        # for 37, 648 = (37**2 - 3*37 + 3) + (-(37-1) * 630 - 1) / 37
        # for 37, 648 = (37**2 - 3*37 + 3) - 630 + (630 - 1) / 37
        # (630 - 1) / 37 = 17

        # [a, b, c]
        # [d, e, f]
        # [g, h, i]

        # sum = (a+b+c)^3 + (d+e+f)^3 + (g+h+i)^3
        # we know that (a+d+g) = -0.5, and (b+e+h) = -0.5, and (g+h+i) = -0.5

        return int(round((ans/p), 4))

    @timeit
    def solve(self, max_p: int) -> int:
        ans = sum((p-1)*(p-2) for p in primes(max_p) if p % 3 != 1)

        mod_3_1_primes = (p for p in primes(max_p) if p % 3 == 1)

        for p in mod_3_1_primes:
            ans += self.given_p_simple_2(p)
        return ans


class Solution753(unittest.TestCase):
    def setUp(self):
        self.problem = Problem753()

    def test_specific_p(self):
        with self.subTest('testing p=5'):
            self.assertEqual(12, self.problem.given_p(5))
            # self.assertEqual(12, self.problem.given_p_simple(5))
        with self.subTest('testing p=7'):
            self.assertEqual(0, self.problem.given_p(7))
            # self.assertEqual(0, self.problem.given_p_simple(7))

    def test_solution(self):
        # self.assertEqual(None, self.problem.solve(6000000))
        self.assertEqual(37501868762, self.problem.solve(10000))
        # self.assertEqual(5041836452, self.problem.solve(5000))
        # self.assertEqual(48911172, self.problem.solve(1000))
        # self.assertEqual(6910616, self.problem.solve(500))
        # self.assertEqual(59762, self.problem.solve(100))


if __name__ == '__main__':
    unittest.main()

