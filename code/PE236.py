# todo fill description

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

A_total = [5248, 1312, 2624, 5760, 3936]
B_total = [640, 1888, 3776, 3776, 5664]

import fractions
m = fractions.Fraction(1476,1475)
for B, A in zip(B_total, A_total):
    print("===================================")
    # b/B = m * a/A
    # b = (m * B / A) * a
    s = m * B / A
    possible_a = range(1, A)
    possible_b = [a * s for a in possible_a]
    for b in possible_b:
        if int(b) == b:
            a = b/s
            print("a:{}, b:{}, b/36:{}, b/82:{}, a/25:{}, a/125:{}".format(a, b, b/36, b/82, a/25, a/125))

import fractions
m = fractions.Fraction(1476, 1475)
w = [None]*5
w_float = [None]*5
for i, (B, A) in enumerate(zip(B_total, A_total)):
    # b/a = m * B / A
    print(i, m*B/A)
    w[i] = m*B/A
    w_float[i] = float(m*B/A)


ratio = sum(B_total)/(sum(A_total)*m)
ratio_float = float(sum(B_total)/(sum(A_total)*m))

# print(sum(B_total)/(sum(A_total)*m))
import cvxpy
m = 1476/1475
A_bad = cvxpy.Variable(5, integer=True)
# A_bad = cvxpy.Variable(5, nonneg=True)
ls_constraints = []
lhs = sum([(B_total[i] / A_total[i]) * A_bad[i] for i in range(5)])
ls_constraints.append((m**2) * lhs == sum(B_total)/sum(A_total) * cvxpy.sum(A_bad))
# lower bound
ls_constraints.append(A_bad >= 0)
# upper bound
for i in range(5):
    ls_constraints.append(A_bad[i] <= A_total[i])

prob = cvxpy.Problem(cvxpy.Maximize(cvxpy.sum(A_bad)), ls_constraints)
prob.solve()
print(prob.status)
print(A_bad.value)



import cvxpy

# m = cvxpy.Variable(1)
# m = fractions.Fraction(1476, 1475)
m = 1476/1475
A_bad = cvxpy.Variable(5, integer=True)
B_bad = cvxpy.Variable(5, integer=True)

ls_constraints = []
for i in range(5):
    # c_i = B_bad[i] / B_total[i] == m * A_bad[i] / A_total[i]
    ls_constraints.append(B_bad[i] / B_total[i] == m * A_bad[i] / A_total[i])
# total rate
ls_constraints.append(m * cvxpy.sum(B_bad) / sum(B_total) == cvxpy.sum(A_bad) / sum(A_total))
# positive number of bad
ls_constraints.append(B_bad >= 0)
ls_constraints.append(A_bad >= 0)
# bad less than total
for i in range(5):
    ls_constraints.append(B_bad[i] <= B_total[i])
    ls_constraints.append(A_bad[i] <= A_total[i])

prob = cvxpy.Problem(cvxpy.Maximize(cvxpy.sum(A_bad)), ls_constraints)
prob.solve(verbose=True)
print(prob.status)
print(A_bad.value)
print(B_bad.value)


def f_lhs(ls_a):
    return (6/5)**3 * (9/59 * ls_a[0] + 41/90 * ls_a[3] + ls_a[1] + ls_a[2] + ls_a[4])


def f_lhs_m(ls_a, m):
    return m**2 * (59/41)**2 * 5/6 * (9/59 * ls_a[0] + 41/90 * ls_a[3] + ls_a[1] + ls_a[2] + ls_a[4])


def f_rhs(ls_a):
    return sum(ls_a)

from math import floor

for k1 in range(1, floor(A_total[0]/295)):  # 17 = floor(5248/295)
    for k2 in range(1, floor(A_total[1]/25)):
        for k3 in range(1, floor(A_total[2]/25)):
            for k4 in range(1, floor(A_total[3]/125)):
                for k5 in range(1, floor(A_total[4]/25)):
                    lhs = 216 * (k1/5 + 41/90 * k4 + k2/5 + k3/5 + k5/5)
                    rhs = 295*k1 + 25*k2 + 25*k3 + 125*k4 + 25*k5
                    diff = abs(lhs-rhs)
                    if diff < 1e-8:
                        print("k1:{}, k2:{}, k3:{}, k4:{}, k5:{}, diff:{}".format(k1,k2,k3,k4,k5,diff))


for k1 in range(1, floor(A_total[0]/295)):  # 17 = floor(5248/295)
    for k4 in range(1, floor(A_total[3]/125)):
        for k235 in range(3, floor(A_total[1]/25) + floor(A_total[2]/25) + floor(A_total[4]/25)):
            lhs = 216 * (k1/5 + 41/90 * k4 + k235/5)
            rhs = 295*k1 + 125*k4 + 25*k235
            diff = abs(lhs-rhs)
            if diff < 1e-8:
                print("k1:{}, k4:{}, k235:{}, diff:{}".format(k1, k4, k235, diff))

# k1:7, k4:9, k235:110, diff:0.0
# k1:7, k4:22, k235:129, diff:0.0
# k1:7, k4:35, k235:148, diff:0.0
# k1:14, k4:5, k235:201, diff:0.0
# k1:14, k4:18, k235:220, diff:0.0
# k1:14, k4:31, k235:239, diff:1.8189894035458565e-12
# k1:14, k4:44, k235:258, diff:0.0


m = fractions.Fraction(1476, 1475)
multiples = []
for i in range(5):
    # Since the numerator and denominator don't share any prime factors, this should always work?
    # todo check
    multiples.append((fractions.Fraction(B_total[i], A_total[i]) * m).denominator)
#
# assert multiples[1] == multiples[2]
# assert multiples[4] == multiples[2]
#
# for k1 in range(1, floor(A_total[0]/multiples[0])):  # 17 = floor(5248/295)
#     for k4 in range(1, floor(A_total[3]/multiples[3])):
#         for k235 in range(3, floor(A_total[1]/multiples[3]) + floor(A_total[2]/multiples[2]) + floor(A_total[4]/multiples[4])):
#             lhs = 216 * (k1/5 + 41/90 * k4 + k235/5)
#             rhs = 295*k1 + 125*k4 + 25*k235
#             diff = abs(lhs-rhs)
#             if diff < 1e-8:
#                 print("k1:{}, k4:{}, k235:{}, diff:{}".format(k1, k4, k235, diff))

assert multiples[1] == multiples[2]
assert multiples[4] == multiples[2]
for k1 in range(1, floor(A_total[0]/multiples[0])):  # 17 = floor(5248/295)
    for k4 in range(1, floor(A_total[3]/multiples[3])):
        for k235 in range(3, floor(A_total[1]/multiples[3]) + floor(A_total[2]/multiples[2]) + floor(A_total[4]/multiples[4])):
            lhs = m**2 * (59/41)**2 * 5/6 * (5/59 * k1 * multiples[0] + 41/90 * k4 * multiples[3] + k235*multiples[2])
            rhs = multiples[0]*k1 + multiples[3]*k4 + multiples[2]*k235
            diff = abs(lhs-rhs)
            if diff < 1e-8:
                print("k1:{}, k4:{}, k235:{}, diff:{}".format(k1, k4, k235, diff))
                can_work = True


def test_m(m):
    """

    Args:
        m: <fractions.Fraction>

    Returns:

    """
    can_work = False
    multiples = []
    for i in range(5):
        multiples.append((fractions.Fraction(B_total[i], A_total[i]) * m).denominator)
    assert multiples[1] == multiples[2]
    assert multiples[4] == multiples[2]
    for k1 in range(1, floor(A_total[0] / multiples[0])):  # 17 = floor(5248/295)
        for k4 in range(1, floor(A_total[3] / multiples[3])):
            # todo solve for k235 and then test if it's an integer within these bounds, Or solve for a2 + a3 + a5
            for k235 in range(3, floor(A_total[1] / multiples[3]) + floor(A_total[2] / multiples[2]) + floor(
                    A_total[4] / multiples[4])):
                lhs = m ** 2 * (59 / 41) ** 2 * 5 / 6 * (
                            5 / 59 * k1 * multiples[0] + 41 / 90 * k4 * multiples[3] + k235 * multiples[2])
                rhs = multiples[0] * k1 + multiples[3] * k4 + multiples[2] * k235
                diff = abs(lhs - rhs)
                if diff < 1e-8:
                    print("k1:{}, k4:{}, k235:{}, diff:{}".format(k1, k4, k235, diff))
                    can_work = True
    return can_work