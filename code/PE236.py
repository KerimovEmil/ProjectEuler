"""
PROBLEM

Suppliers 'A' and 'B' provided the following numbers of products for the luxury hamper market:

Product	'A'	'B'
Beluga Caviar	5248	640
Christmas Cake	1312	1888
Gammon Joint	2624	3776
Vintage Port	5760	3776
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

ANSWER:
123/59
Solve time ~ 0.23 seconds
"""
import unittest
from math import floor
from util.utils import timeit, farey
from fractions import Fraction


# EQ1) b_i / B_i = m * a_i / A_i for i in range(5)
# EQ2) (sum_i b_i) / (sum_i B_i) = (1/m) * (sum_i a_i) / (sum_i A_i)
# Where B_i and A_i are the total number of provided goods as given in the problem and b_i and a_i are the number
# of spoiled items for good i.

# EQ1 can be written as b_i = (B_i / A_i) * m * a_i
# Plugging b_i into EQ 2 and multiplying by m, we get:
# EQ2) m^2 * (sum_i (B_i / A_i) * a_i) / (sum_i B_i) = (sum_i a_i) / (sum_i A_i)
# The goal is to find integer a_i such that the solution is satisfied, subject to the bounds:
# 0 < a_i < A_i, and (B_i / A_i) * m * a_i < B_i

# Plugging in the values of A_i and B_i we get:
# m^2 *(59/41) *(5/59 a1 + a2 + a3 + 41/90 a4 + a5) = 6/5 * 41/59 * (a1 + a2 + a3 + a4 + a5)

# Also noting that we have:
# B1/A1 = 5/41
# B2/A2 = 59/41
# B3/A3 = 59/41
# B4/A4 = 59/90
# B5/A5 = 59/41
# this means that the 2nd, 3rd, and 5th goods can all be treated together as they do not have any new constraints

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

    def find_all_possible_m(self, debug=False):
        max_value = 0
        possible_m = []
        for f in farey(self.max_den, descending=True):
            if f[0] == 0:
                continue
            test_fraction = Fraction(41 * f[1], 59 * f[0])
            if float(test_fraction) > 1:
                is_pass = self.test_m(test_fraction, debug=debug)
                if is_pass:
                    self.num_of_m_found += 1
                    if float(test_fraction) > max_value:
                        max_value = float(test_fraction)
                        possible_m.append(test_fraction)
                        if debug:
                            print("NEW MAX:{}, value:{}, {}/{}".format(test_fraction, float(test_fraction), f[1], f[0]))

        return possible_m

    @timeit
    def solve(self):
        self.possible_m = self.find_all_possible_m()
        return self.possible_m[-1]

    def test_m(self, m, debug=True):
        """

        Args:
            m: <fractions.Fraction>
            debug: <bool>

        Returns:

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
        for k1 in range(1, floor(a_total[0] / (m*multiples[0]))):
            for k4 in range(1, floor(a_total[3] / (m*multiples[3]))):
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
                        if debug:
                            print("a1:{}, a4:{}, a235:{}".format(a1, a4, a235))
                            can_work = True
                        else:
                            return True
        return can_work


class Solution236(unittest.TestCase):
    def setUp(self):
        a_total = [5248, 1312, 2624, 5760, 3936]
        b_total = [640, 1888, 3776, 3776, 5664]
        self.problem = Problem236(a_total, b_total, max_den=60)

    # def test_solution(self):
    #     self.assertEqual(Fraction(123, 59), self.problem.solve())

    def test_all_solution(self):

        # Check solution
        self.assertEqual(Fraction(123, 59), self.problem.solve())

        # check that all found m are accurate
        ls_all = [Fraction(41, 40),
                  Fraction(328, 295),
                  Fraction(369, 295),
                  Fraction(451, 295),
                  Fraction(492, 295),
                  Fraction(574, 295),
                  Fraction(123, 59),
                  Fraction(60, 59),
                  Fraction(63, 59),
                  Fraction(80, 59),
                  Fraction(81, 59),
                  Fraction(82, 59),
                  Fraction(108, 59),
                  Fraction(123, 118),
                  Fraction(205, 118),
                  Fraction(697, 590),
                  Fraction(861, 590),
                  Fraction(902, 885),
                  Fraction(1066, 885),
                  Fraction(205, 177),
                  Fraction(1353, 1180),
                  Fraction(1599, 1180),
                  Fraction(287, 236),
                  Fraction(369, 236),
                  Fraction(1476, 1475),
                  Fraction(1722, 1475),
                  Fraction(492, 413),
                  Fraction(615, 413),
                  Fraction(738, 413),
                  Fraction(533, 472),
                  Fraction(615, 472),
                  Fraction(3321, 3245),
                  Fraction(738, 649),
                  Fraction(1230, 1003),
                  Fraction(2460, 1711)
                  ]

        self.assertEqual(len(ls_all), 35)
        print("Num found: {}/{}".format(self.problem.num_of_m_found, 35))
        in_bool = True
        for frac in self.problem.possible_m:
            in_bool = in_bool and (frac in ls_all)
        self.assertTrue(in_bool)


if __name__ == '__main__':
    unittest.main()
