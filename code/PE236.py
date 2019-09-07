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
Solve time ~ ____ seconds
"""
from util.utils import timeit
import unittest

# todo clean up commented notes
# EQ1) b_i / B_i = m * a_i / A_i for i in range(5)
# EQ2) (sum_i b_i) / (sum_i B_i) = (1/m) * (sum_i a_i) / (sum_i A_i)
# Where B_i and A_i are the total number of provided goods as given in the problem and b_i and a_i are the number
# of spoiled items for good i.

# EQ1 can be written as b_i = (B_i / A_i) * m * a_i
# Plugging b_i into EQ 2 and multiplying by m, we get:
# EQ2) m^2 * (sum_i (B_i / A_i) * a_i) / (sum_i B_i) = (sum_i a_i) / (sum_i A_i)
# The goal is to find integer a_i such that the solution is satisfied, subject to the bounds:
# 0 < a_i < A_i, and (B_i / A_i) * m * a_i < B_i

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


# m that work:
# m = 1476 / 1475 = 36*41 / 25*59 = 1.000677966101695
# m = 123/118 = 3*41 / 2*59 = 1.0423728
# m = 328/295 = 8*41 / 5*59 value:1.111864406779661
# m = 533/472 = 13*41 / 8*59 value:1.1292372881355932
# NEW MAX IS: 738/649, value:1.1371340523882896, 18/11
# NEW MAX IS: 205/177, value:1.1581920903954803, 5/3
# m = 1722 / 1475 = 6*41*7/(25*59) = 1.16745762711
# NEW MAX IS: 697/590, value:1.1813559322033897, 17/10
# NEW MAX IS: 492/413, value:1.1912832929782082, 12/7
# NEW MAX IS: 287/236, value:1.2161016949152543, 7/4
# NEW MAX IS: 369/295, value:1.2508474576271187, 9/5
# NEW MAX IS: 615/472, value:1.3029661016949152, 15/8
# NEW MAX IS: 82/59, value:1.3898305084745763, 2/1
# NEW MAX IS: 615/413, value:1.4891041162227603, 15/7
# NEW MAX IS: 451/295, value:1.528813559322034, 11/5
# NEW MAX IS: 369/236, value:1.5635593220338984, 9/4
# m = 492/295 = 36*41*10/(25*59*6) = 6*41*2/(5*59) = 1.667796610
# NEW MAX IS: 205/118, value:1.7372881355932204, 5/2
# NEW MAX IS: 533/295, value:1.806779661016949, 13/5
# NEW MAX IS: 328/177, value:1.8531073446327684, 8/3
# NEW MAX IS: 123/59, value:2.0847457627118646, 3/1

# n = 100
# NEW MAX IS: 1476/1475, value:1.000677966101695, 36/25
# NEW MAX IS: 902/885, value:1.0192090395480227, 22/15
# NEW MAX IS: 123/118, value:1.0423728813559323, 3/2
# NEW MAX IS: 328/295, value:1.111864406779661, 8/5
# NEW MAX IS: 533/472, value:1.1292372881355932, 13/8
# NEW MAX IS: 738/649, value:1.1371340523882896, 18/11
# NEW MAX IS: 1353/1180, value:1.1466101694915254, 33/20
# NEW MAX IS: 205/177, value:1.1581920903954803, 5/3
# NEW MAX IS: 1722/1475, value:1.167457627118644, 42/25
# NEW MAX IS: 697/590, value:1.1813559322033897, 17/10
# NEW MAX IS: 492/413, value:1.1912832929782082, 12/7
# NEW MAX IS: 1066/885, value:1.2045197740112994, 26/15
# NEW MAX IS: 287/236, value:1.2161016949152543, 7/4
# NEW MAX IS: 1230/1003, value:1.226321036889332, 30/17
# NEW MAX IS: 369/295, value:1.2508474576271187, 9/5
# NEW MAX IS: 615/472, value:1.3029661016949152, 15/8
# NEW MAX IS: 1599/1180, value:1.3550847457627118, 39/20
# NEW MAX IS: 82/59, value:1.3898305084745763, 2/1
# NEW MAX IS: 2460/1711, value:1.4377556984219755, 60/29
# NEW MAX IS: 861/590, value:1.459322033898305, 21/10
# NEW MAX IS: 615/413, value:1.4891041162227603, 15/7
# NEW MAX IS: 451/295, value:1.528813559322034, 11/5
# NEW MAX IS: 369/236, value:1.5635593220338984, 9/4
# NEW MAX IS: 492/295, value:1.6677966101694914, 12/5
# NEW MAX IS: 205/118, value:1.7372881355932204, 5/2
# NEW MAX IS: 123/59, value:2.0847457627118646, 3/1
# count:26

import fractions
from math import floor

A_total = [5248, 1312, 2624, 5760, 3936]
B_total = [640, 1888, 3776, 3776, 5664]


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

def test_m(m, debug=True):
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
        # Since the Fraction class automatically computes the fraction in lowest terms, this should always work.
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
            if diff <= 1e-9:
                # check a_i bounds
                if 1 <= a235 < A_total[1] + A_total[2] + A_total[4]:
                    # check b_i bounds, b_i = (B_i / A_i) * m * a_i, b_i < B_i
                    # simplifies to: m * a_i < A_i
                    # todo: simplify with previous conditions and loops
                    if m*a1 < A_total[0] and m*a4 < A_total[3] and m*a235 < (A_total[1] + A_total[2] + A_total[4]):
                        if debug:
                            print("a1:{}, a4:{}, a235:{}".format(a1, a4, int(a235)))
                            can_work = True
                        else:
                            return True
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

max_value = 0
for i in range(1, 20):
    for j in range(1, 10):
        frac = fractions.Fraction(41 * i, 59 * j)
        is_pass = test_m(frac, debug=False)
        if is_pass:
            if float(frac) > max_value:
                max_value = float(frac)
                print("NEW MAX IS: {}, value:{}".format(frac, float(frac)))


def farey(n, descending=False):
    """Print the n'th Farey sequence. Allow for either ascending or descending."""
    a, b, c, d = 0, 1, 1, n
    if descending:
        a, c = 1, n - 1
    ls_farey = [(a, b)]
    # print(a, b)
    while (c <= n and not descending) or (a > 0 and descending):
        k = int((n + b) / d)
        a, b, c, d = c, d, k * c - a, k * d - b
        # print(a, b)
        ls_farey.append((a, b))
    return ls_farey


max_value = 0
n = 10
for f in farey(n):
    if f[0] == 0:
        continue
    frac = fractions.Fraction(41 * f[1], 59 * f[0])
    is_pass = test_m(frac, debug=False)
    if is_pass:
        if float(frac) > max_value:
            max_value = float(frac)
            print("NEW MAX IS: {}, value:{}".format(frac, float(frac)))



max_value = 0
n = 18
count = 0
for f in farey(n, descending=True):
    if f[0] == 0:
        continue
    frac = fractions.Fraction(41 * f[1], 59 * f[0])
    if float(frac) > 1:
        is_pass = test_m(frac, debug=False)
        if is_pass:
            count += 1
            if float(frac) > max_value:
                max_value = float(frac)
                print("NEW MAX IS: {}, value:{}, {}/{}".format(frac, float(frac), f[1], f[0]))
print("count:{}".format(count))


max_value = 0
n=200
count=0
for f in farey(n, descending=True):
    if f[0] == 0:
        continue
    frac = fractions.Fraction(41 * f[1], 59 * f[0])
    if (float(frac) > 1) and (f[0]%41 != 0) and (f[1]%59 != 0):
        is_pass = test_m(frac, debug=False)
        if is_pass:
            count += 1
            if float(frac) > max_value:
                max_value = float(frac)
                print("NEW MAX IS: {}, value:{}, {}/{}".format(frac, float(frac), f[1], f[0]))
print("count:{}".format(count))