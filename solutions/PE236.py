"""
PROBLEM

Suppliers 'A' and 'B' provided the following numbers of products for the luxury hamper market:

Product	             'A'	'B'
Beluga Caviar	    5248	640
Christmas Cake	    1312	1888
Gammon Joint	    2624	3776
Vintage Port	    5760	3776
Champagne Truffles	3936	5664
Although the suppliers try very hard to ship their goods in perfect condition, there is inevitably some spoilage
- i.e. products gone bad.

The suppliers compare their performance using two types of statistic:

The five per-product spoilage rates for each supplier are equal to the number of products gone bad divided by the
number of products supplied, for each of the five products in turn.
The overall spoilage rate for each supplier is equal to the total number of products gone bad divided by the total
number of products provided by that supplier.
To their surprise, the suppliers found that each of the five per-product spoilage rates was worse (higher) for 'B' than
for 'A' by the same factor (ratio of spoilage rates), m>1; and yet, paradoxically, the overall spoilage rate was worse
for 'A' than for 'B', also by a factor of m.

There are thirty-five m>1 for which this surprising result could have occurred, the smallest of which is 1476/1475.

What's the largest possible value of m?
Give your answer as a fraction reduced to its lowest terms, in the form u/v.

ANSWER: 123/59
Solve time ~ 0.23 seconds
"""
from fractions import Fraction
from math import ceil

import unittest
from util.utils import timeit, farey


# ----------------------------
# SETTING UP THE PROBLEM
# ----------------------------

# defining A_i to be the number of items in good i provided by A and a_i to be the number of spoiled items
# in good i by A, and the same definitions for B, we get:

# EQ1) b_i / B_i = m * a_i / A_i for i in range(5)
# EQ2) (sum_i b_i) / (sum_i B_i) = (1/m) * (sum_i a_i) / (sum_i A_i)
# Where B_i and A_i are the total number of provided goods as given in the problem and b_i and a_i are the number
# of spoiled items for good i.

# EQ1 can be written as b_i = (B_i / A_i) * m * a_i
# Plugging b_i into EQ 2 and multiplying by m, we get:
# EQ2) m^2 * (sum_i (B_i / A_i) * a_i) / (sum_i B_i) = (sum_i a_i) / (sum_i A_i)
# The goal is to find integer a_i such that the solution is satisfied, subject to the bounds:
# 0 < a_i < A_i, and (B_i / A_i) * m * a_i < B_i

# ----------------------------
# USING THE GIVEN VALUES
# ----------------------------

# Plugging in the values of A_i and B_i we get:
# m^2 *(59/41) *(5/59 a1 + a2 + a3 + 41/90 a4 + a5) = 6/5 * 41/59 * (a1 + a2 + a3 + a4 + a5)

# Also noting that we have:
# B1/A1 = 5/41
# B2/A2 = 59/41
# B3/A3 = 59/41
# B4/A4 = 59/90
# B5/A5 = 59/41
# this means that the 2nd, 3rd, and 5th goods can all be treated together as they do not have any new constraints
# therefore let us define a235 = a2 + a3 + a5, rewriting our equation we get
# m^2 *(59/41) *(5/59 a1 + 41/90 a4 + a235) = 6/5 * 41/59 * (a1 + a4 + a235)

# ----------------------------
# TESTING EACH M
# ----------------------------

# notice that the values of a1 and a4 are limited to values that result in integer bi.
# since b_i = (B_i / A_i) * m * a_i,
# therefore a_i can only be multiples of the denominator of (B_i / A_i) * m (when the fraction is in reduced form)
# this means that we only need to test ai in multiples of ((B_i / A_i) * m).denominator
# also note that since the resulting b_i must be less than B_i, we get (B_i / A_i) * m * a_i < B_i
# this simplifies to a_i < A_i / m
# therefore we only need to loop over ai from 1 until A_i / m in multiples of ((B_i / A_i) * m).denominator

# given a a1 and an a4 we can solve for a235 and check if it is an integer, using
# scalar = m^2 * (59/41)^2 * 5 / 6
# a235 = [(scalar * 5/59 - 1) * a1 + (scalar * 41/90 - 1) * a4] / [1 - scalar]

# -----------------
# POSSIBLE M
# -----------------

# INITIAL APPROACH

# now this part I just kinda guessed, I assumed the form of m will be (41/59) * some_fraction
# and then got every fraction in lowest form that has a max denominator of 60 (this is a parameter)
# reverted that fraction and looped over those in ascending order.
# this is possibly why this code does not find all 35 solutions, but this allowed me to greatly reduce the search
# todo see how other solutions handled this in the thread

# ALTERNATIVE APPROACH

# Using the definition of m we have:
# (b_i / a_i)  * (A_i / B_i) = m
# and
# m = (sum_i a_i)/(sum_i b_i)  * (sum_i B_i) / (sum_i A_i)
# plugging in our variables we get 4 equations
# (b_1 / a_1) * (41 / 5) = m
# (b_4 / a_4) * (90 / 59) = m
# (b_235 / a_235) * (41 / 59) = m
# (sum_i a_i)/(sum_i b_i) * (246/295) = m
# Pick one of these equations and loop over ai and bi, using m>1 to reduce the search space

# -----------------
# EXAMPLES
# -----------------

# details of solution for smallest m case:
# if m = 1476 / 1475 then
# a1 = 295*k1
# a4 = 125*k4
# ai = 25*ki for i = 2, 3, 5

# k1:7, k4:9, k235:110
# k1:7, k4:22, k235:129
# k1:7, k4:35, k235:148
# k1:14, k4:5, k235:201
# k1:14, k4:18, k235:220
# k1:14, k4:31, k235:239
# k1:14, k4:44, k235:258
# implies
# a1:2065, a4:1125, a235:2750  note that a235 = a2 + a3 + a5
# a1:2065, a4:2750, a235:3225
# a1:2065, a4:4375, a235:3700
# a1:4130, a4:625, a235:5025
# a1:4130, a4:2250, a235:5500
# a1:4130, a4:3875, a235:5975
# a1:4130, a4:5500, a235:6450


class Problem236:
    def __init__(self, ls_total_a, ls_total_b, max_den):
        self.ls_total_A = ls_total_a
        self.ls_total_B = ls_total_b
        self.max_den = max_den
        self.possible_m = []
        self.num_of_m_found = 0

    def all_possible_m_faray(self):
        return [Fraction(41 * f[1], 59 * f[0]) for f in farey(self.max_den, descending=True) if f[0] != 0]

    @staticmethod
    def possible_m_given_a_b(a, b):
        t_set = set()

        # get min a, and corresponding b
        m_scalar = Fraction(a, b)  # (A_i / B_i) = (41 / 59)
        m_scalar_float = float(m_scalar)

        # loop over possible a_i and b_i values
        for a_i in range(1, a):
            # (b_i / a_i) * (A_i / B_i) = m  > 1
            # b_i > (B_i / A_i) * a_i
            for b_i in range(int(a_i / m_scalar_float) + 1, b):  # todo include an upper bound for m
                t_set.add(Fraction(b_i, a_i))

        return {m_scalar * t for t in t_set}

    def all_possible_m_loop(self):
        """ Using m = (b_i / a_i)  * (A_i / B_i) """
        # set_possible_m = None
        # for a, b in zip(self.ls_total_A, self.ls_total_B):
        #     new_set = self.possible_m_given_a_b(a, b)
        #     if set_possible_m is None:
        #         set_possible_m = new_set
        #     else:
        #         set_possible_m = set_possible_m.intersection(new_set)
        #
        # return set_possible_m

        a_min, b_min = min(zip(self.ls_total_A, self.ls_total_B))
        return self.possible_m_given_a_b(a_min, b_min)

    def find_all_m(self, debug=False):
        max_value = 0
        possible_m = []
        all_possible_m = self.all_possible_m_faray()
        # all_possible_m = self.all_possible_m_loop()  # way too slow
        for test_fraction in all_possible_m:
            if float(test_fraction) > 1:
                is_pass = self.test_m(test_fraction, debug=debug)
                if is_pass:
                    self.num_of_m_found += 1
                    if float(test_fraction) > max_value:
                        max_value = float(test_fraction)
                        possible_m.append(test_fraction)
                        if debug:
                            print("NEW MAX:{}, value:{}".format(test_fraction, float(test_fraction)))

        return possible_m

    @timeit
    def solve(self):
        self.possible_m = self.find_all_m()
        return max(self.possible_m)

    def test_m(self, m, debug=False):  # misses two valid possibilities: 574/295 and 738/413
        """
        Note that this function does not work for a general a_totals and b_totals.
        Args:
            m: <fractions.Fraction>
            debug: <bool>

        Returns: True if the specified m can work given the A's and B's.

        """
        if m <= 1:
            return False
        b_total = self.ls_total_B
        a_total = self.ls_total_A
        can_work = False
        multiples = []
        scalar = m ** 2 * (59 / 41) ** 2 * 5 / 6
        den = (1 - scalar)
        for i in range(5):
            # Since the Fraction class automatically computes the fraction in lowest terms, this should always work.
            multiples.append((Fraction(b_total[i], a_total[i]) * m).denominator)
        assert multiples[1] == multiples[2]
        assert multiples[4] == multiples[2]
        for k1 in range(1, ceil(a_total[0] / (m * multiples[0])) + 1):
            for k4 in range(1, ceil(a_total[3] / (m * multiples[3])) + 1):
                a1 = k1 * multiples[0]
                a4 = k4 * multiples[3]
                num = a1 * (scalar * 5 / 59 - 1) + a4 * (scalar * 41 / 90 - 1)
                is_integer = abs(num % den) <= 1e-9
                if is_integer:
                    a235 = int(num / den)  # a2 + a3 + a5
                    # check a_i bounds and check b_i bounds
                    # b_i = (B_i / A_i) * m * a_i, b_i < B_i
                    # simplifies to: m * a_i < A_i
                    if 1 <= a235 < m * (a_total[1] + a_total[2] + a_total[4]):
                        if (0 < a1 < a_total[0]) and (0 < a4 < a_total[3]):
                            if debug:
                                print("a1:{}, a4:{}, a235:{}".format(a1, a4, a235))
                                can_work = True
                            else:
                                return True
        return can_work


class Solution236(unittest.TestCase):
    def setUp(self):
        # Note that there are a lot of simplifications in the code due to the exact values of a_total and b_total,
        # therefore the code does not work if a_total and b_total were to change.
        a_total = [5248, 1312, 2624, 5760, 3936]
        b_total = [640, 1888, 3776, 3776, 5664]
        self.problem = Problem236(a_total, b_total, max_den=60)  # max_den=100

    def test_all_solution(self):
        self.assertEqual(Fraction(123, 59), self.problem.solve())


if __name__ == '__main__':
    unittest.main()

# MANUAL ATTEMPTS
# a_total = [5248, 1312, 2624, 5760, 3936]
# b_total = [640, 1888, 3776, 3776, 5664]
# m = Fraction(574, 295)
#
# def get_set_b(i, m):
#     set_bi = set()
#     for ai in range(1, a_total[i]):
#         # b_i = (B_i / A_i) * m * a_i
#         bi = (b_total[i] / a_total[i]) * m * ai
#         if abs(bi - int(bi)) < 1e-9:
#             set_bi.add(int(bi))
#     return set_bi
# set_b1 = get_set_b(0, m)
# set_b2 = get_set_b(1, m)
# set_b3 = get_set_b(2, m)
# set_b4 = get_set_b(3, m)
# set_b5 = get_set_b(4, m)
#
# BT = sum(b_total)
# AT = sum(a_total)
# mf = float(m)
# RT = AT * mf / BT
# for b1 in set_b1:
#     a1 = int((a_total[0] / b_total[0]) * b1 / mf)
#     for b2 in set_b2:
#         a2 = int((a_total[1] / b_total[1]) * b2 / mf)
#         for b3 in set_b3:
#             a3 = int((a_total[2] / b_total[2]) * b3 / mf)
#             for b4 in set_b4:
#                 a4 = int((a_total[3] / b_total[3]) * b4 / mf)
#                 for b5 in set_b5:
#                     a5 = int((a_total[4] / b_total[4]) * b5 / mf)
#                     # m = (sum_i a_i)/(sum_i b_i)  * BT / AT
#                     if abs(RT - (a1 + a2 + a3 + a4 + a5)/ (b1 + b2 + b3 + b4 + b5))<1e-9:
#                         print(a1,a2,a3,a4,a5,b1,b2,b3,b3,b4,b5)
# # 2182 5 5 449 5 518 14 14 14 574 14
