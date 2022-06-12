"""
If a box contains twenty-one coloured discs, composed of fifteen blue discs and six red discs, and two discs were
taken at random, it can be seen that the probability of taking two blue discs, P(BB) = (15/21)×(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box
containing eighty-five blue discs and thirty-five red discs.

By finding the first arrangement to contain over 10^12 = 1,000,000,000,000 discs in total, determine the number of blue
 discs that the box would contain.

ANSWER: 756872327473
Solve time ~0.001 seconds
"""
from util.utils import timeit
import unittest

# B is number of Blue chips
# N is total number of chips

# need B/N * (B-1)/(N-1) = 1/2
# 2B(B-1) = N(N-1)
# Using (2q-1)^2 = 4q^2 - 4q + 1
# 4B^2 + 4B + 1 = 2N^2 + 2N + 1
# (2B-1)^2 = 2N^2 + 2N + 1
# 2(2B-1)^2 = (2N-1)^2 + 1
# setting y = 2B-1 and x = 2N-1
# x^2 - 2y^2 = -1

# fundamental solution: x=1, y=1 -> u = (1+sqrt(2))
# x_n + y_n * sqrt(2) = (1+sqrt(2))^{2n + 1}
# set 2n + 1 to 33 to get x_n larger than 10^12
# u_33 = (1+sqrt(2))^33 = 2140758220993 + 1513744654945*sqrt(2)
# 2N-1 = 2140758220993 -> N = 1070379110497 > 10^12
# 2B-1 = 1513744654945 -> B = 756872327473


class FieldExtensionD:
    """Numbers of the form x + y*sqrt(D) for x,y integers"""
    def __init__(self, x: int, y: int, d: int):
        self.x = x
        self.y = y
        self.d = d
        self.u_float = x + y * (d ** 0.5)

    def conjugate(self):
        return FieldExtensionD(x=self.x, y=-self.y, d=self.d)

    def norm(self):
        return self*self.conjugate()

    def __mul__(self, other):
        assert self.d == other.d
        f = self.x * other.x + self.y * self.d * other.y
        s = self.y * other.x + self.x * other.y
        return FieldExtensionD(x=f, y=s, d=self.d)

    def __pow__(self, power: int):
        # power is always greater than 0
        if power <= 0:
            raise NotImplementedError('Negative powers are not implemented.')
        result = self
        num_to_mult = power - 1
        while num_to_mult > 0:
            result *= self
            num_to_mult -= 1
        return result


class Problem100:
    def __init__(self):
        self.u = FieldExtensionD(x=1, y=1, d=2)

    @timeit
    def solve(self, min_num):
        u_sq = self.u * self.u

        u_current = self.u
        total_n = (u_current.x + 1) // 2

        while total_n < min_num:
            u_current = u_current * u_sq
            total_n = (u_current.x + 1) // 2

        return (u_current.y + 1) // 2


class Solution100(unittest.TestCase):
    def setUp(self):
        self.problem = Problem100()

    def test_solution(self):
        self.assertEqual(756872327473, self.problem.solve(min_num=pow(10, 12)))


if __name__ == '__main__':
    unittest.main()
