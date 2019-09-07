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
______
Solve time ~ ____ seconds
"""
from util.utils import timeit
import unittest

# todo clean up commented notes
# m^2 *(59/41) *(5/59 a1 + a2 + a3 + 41/90 a4 + a5) = 6/5 * 41/59 * (a1 + a2 + a3 + a4 + a5)

# if m = 1476 / 1475 then
# a1 = 295*k1
# a2 = 25*k2
# a3 = 25*k3
# a4 = 125*k4
# a5 = 25*k5

# then k1=7
# case 1) k4=9 implies k2 + k3 + k5 = 110
# case 2) k4=22 implies k2 + k3 + k5 = 129
# case 3) k4=35 implies k2 + k3 + k5 = 148

# then k1=14
# case 1) k4=5 implies k2 + k3 + k5 = 201
# case 2) k4=18 implies k2 + k3 + k5 = 220
# case 3) k4=31 implies k2 + k3 + k5 = 239
# case 4) k4=44 implies k2 + k3 + k5 = 258

# B1/A1 = 5/41
# B2/A2 = 59/41
# B3/A3 = 59/41
# B4/A4 = 59/90
# B5/A5 = 59/41

# smallest m = (36 * 41) / (25 * 59)

# m = 1476 / 1475
# B_t = 640
# A_t = 5248
# s = m * B_t / A_t
# for i in [i * s for i in range(1, A_t)]:
#     if int(i) == i:
#         print("A: {}, B:{}, extra:{}".format(i, i / s, i / 36))


# m that work:
# m = 1476 / 1475 = 36*41 / 25*59 = 1.000677966101695
# m = 1722 / 1475 = 6*41*7/(25*59) = 1.16745762711
# m = 492/295 = 36*41*10/(25*59*6) = 6*41*2/(5*59) = 1.667796610
# m = 738/295 = 36*41*15/(25*59*6) = 6*41*3/(5*59) = 2.50169491
# fractions.Fraction(36*41*10, 25*59*6)

import fractions
from math import floor

A_total = [5248, 1312, 2624, 5760, 3936]
B_total = [640, 1888, 3776, 3776, 5664]

# m = fractions.Fraction(1476,1475)


# for k1 in range(1, floor(A_total[0]/295)):  # 17 = floor(5248/295)
#     for k2 in range(1, floor(A_total[1]/25)):
#         for k3 in range(1, floor(A_total[2]/25)):
#             for k4 in range(1, floor(A_total[3]/125)):
#                 for k5 in range(1, floor(A_total[4]/25)):
#                     lhs = 216 * (k1/5 + 41/90 * k4 + k2/5 + k3/5 + k5/5)
#                     rhs = 295*k1 + 25*k2 + 25*k3 + 125*k4 + 25*k5
#                     diff = abs(lhs-rhs)
#                     if diff < 1e-8:
#                         print("k1:{}, k2:{}, k3:{}, k4:{}, k5:{}, diff:{}".format(k1,k2,k3,k4,k5,diff))


# k1:7, k4:9, k235:110
# k1:7, k4:22, k235:129
# k1:7, k4:35, k235:148
# k1:14, k4:5, k235:201
# k1:14, k4:18, k235:220
# k1:14, k4:31, k235:239
# k1:14, k4:44, k235:258
# implies
# a1:2065, a4:1125, a235:2750
# a1:2065, a4:2750, a235:3225
# a1:2065, a4:4375, a235:3700
# a1:4130, a4:625, a235:5025
# a1:4130, a4:2250, a235:5500
# a1:4130, a4:3875, a235:5975
# a1:4130, a4:5500, a235:6450

def test_m(m):
    """

    Args:
        m: <fractions.Fraction>

    Returns:

    """
    can_work = False
    multiples = []
    scalar = m ** 2 * (59 / 41) ** 2 * 5 / 6
    den = (1 - scalar)
    for i in range(5):
        # Since the numerator and denominator don't share any prime factors, this should always work?
        # todo check
        multiples.append((fractions.Fraction(B_total[i], A_total[i]) * m).denominator)
    assert multiples[1] == multiples[2]
    assert multiples[4] == multiples[2]
    for k1 in range(1, floor(A_total[0] / multiples[0])):  # 17 = floor(5248/295)
        for k4 in range(1, floor(A_total[3] / multiples[3])):
            a1 = multiples[0] * k1
            a4 = k4 * multiples[3]
            num = a1 * (scalar * 5 / 59 - 1) + a4 * (scalar * 41 / 90 - 1)
            a235 = num/den  # a2 + a3 + a5
            diff = abs(a235 - int(a235))
            if diff <= 1e-8:
                if a235 <= A_total[1] + A_total[2] + A_total[4]:
                    if a235 >= 1:
                        print("a1:{}, a4:{}, a235:{}, diff:{}".format(a1, a4, int(a235), diff))
                        can_work = True
    return can_work


class Problem236:
    def __init__(self, ls_total_A, ls_total_B):
        self.ls_total_A = ls_total_A
        self.ls_total_B = ls_total_B

    @timeit
    def solve(self):
        # return fractions.Fraction(6*41*3, 5*59)  # todo add solution
        return None


class Solution236(unittest.TestCase):
    def setUp(self):
        A_total = [5248, 1312, 2624, 5760, 3936]
        B_total = [640, 1888, 3776, 3776, 5664]
        self.problem = Problem236(A_total, B_total)

    def test_solution(self):
        self.assertEqual(None, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
