"""
PROBLEM

Consider the following Diophantine equation:
 15(x^2+y^2+z^2) = 34(xy+xz+yz)
where x, y and z are positive integers.

Let S(N) be the sum of all solutions, (x,y,z), of this equation such that, 1<=x<=y<=z<=N and gcd(x,y,z)=1.

For N=100, there are three such solutions - (1, 7, 16), (8,9,39), (11, 21, 72). So S(100)=184.

Find S(10^9).

ANSWER:
Solve time:  seconds
"""
from util.utils import timeit
import unittest


# using (x+y+z)^2 = x^2+y^2+z^2 + 2(xy+xz+yz)
# this equation becomes 17(x+y+z)^2 = 17(x^2+y^2+z^2) + 34(xy+xz+yz)
# this equation becomes 17(x+y+z)^2 = 32(x^2+y^2+z^2)
# d = 17(x+y+z)^2 - 32(x^2+y^2+z^2)


import math


def f1(x, y, z):
    return 17*(x+y+z)**2


def f2(x, y, z):
    return 32*(x**2+y**2+z**2)


def d(x, y, z):
    return f1(x, y, z) - f2(x, y, z)


def direction(v, a1, a2):
    return 34*(a1+a2) - 30*v


def is_int(n):
    return abs(n - int(n)) < 1e-8


class Problem785:
    def __init__(self):
        self.ls_solution = []
        self.ls_x = []
        self.ls_y = []
        self.ls_z = []

    def test_sol(self, x: int, y: int, z: int) -> None:
        if 1 <= x <= y and d(x, y, z) == 0 and math.gcd(x, y, z) == 1:
            print((x, y, z))
            self.ls_solution.append((x, y, z))
            self.ls_x.append(x)
            self.ls_y.append(y)
            self.ls_z.append(z)

    @timeit
    def solve(self, n):
        # x+y+z == {0,2} mod 4
        # if z == 2 mod 4 then gcd(x,y,z)!=1, therefore z == 3 mod 4
        for z in range(1, n + 1):
            if z in [1, 2]:
                continue
            # if z%4 == 2:
            #     continue
            if z % 32 not in {0, 1, 3, 5, 7, 8, 9, 11, 13, 15, 16, 17, 19, 21, 23, 24, 25, 27, 29, 31}:
                continue

            # for y in range(1, z+1):
            # for y in range(1, int(0.6*z)+1+1):
            for y in range(int(0.2 * z), int(0.6 * z) + 1 + 1):  # never 2 mod 4
                # x^2 - x*(34/17)*(z+y) + (z^2 + y^2 - (34/17)*y*z) = 0
                # 15x = 17(y+z) +/- 8*sqrt(z^2 + 17zy + y^2)
                sq_r_disc = 8 * (z ** 2 + 17 * z * y + y ** 2) ** 0.5  # (z+y)^2 + 15zy = k^2, 15zy = k^2 - (z+y)^2
                # 15zy = k^2 - (z+y)^2 = (k+z+y)*(k-z-y)
                # 3|(k+z+y) or 3|(k-(z+y)) or 5|(k+z+y) or 5|(k-(z+y))
                # todo don't test every y, just the y's that make z^2+17zy+y^2 into a perfect square
                if is_int(sq_r_disc):
                    sq_r_disc = int(sq_r_disc)
                else:
                    continue
                b_term = 17 * (y + z)
                if (b_term + sq_r_disc) % 15 == 0:
                    self.test_sol(x=(b_term + sq_r_disc) // 15, y=y, z=z)
                if (b_term - sq_r_disc) % 15 == 0:
                    self.test_sol(x=(b_term - sq_r_disc) // 15, y=y, z=z)

        print(len(self.ls_solution))
        print('ls_x = ', self.ls_x)
        print('ls_y = ', self.ls_y)
        print('ls_z = ', self.ls_z)
        print('ls_solution =', self.ls_solution)
        return len(self.ls_solution)  # todo later replace with sum of solutions


class Solution785(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem785()
        pass

    # def test_solution(self):
    #     problem = Problem785()
    #     self.assertEqual(None, problem.solve(n=int(1e9))

    def test_solution_100(self):
        problem = Problem785()
        self.assertEqual(3, problem.solve(n=100))

    def test_solution_200(self):
        problem = Problem785()
        self.assertEqual(7, problem.solve(n=200))

    def test_solution_500(self):
        problem = Problem785()
        self.assertEqual(19, problem.solve(n=500))

    def test_solution_1000(self):
        problem = Problem785()
        self.assertEqual(38, problem.solve(n=1000))

    def test_solution_2000(self):
        problem = Problem785()
        self.assertEqual(77, problem.solve(n=2000))

    def test_solution_3000(self):
        problem = Problem785()
        self.assertEqual(177, problem.solve(n=3000))  # or 118??

    def test_solution_5000(self):
        problem = Problem785()
        self.assertEqual(195, problem.solve(n=5000))  # or 197?

    def test_solution_10000(self):
        problem = Problem785()
        self.assertEqual(388, problem.solve(n=10000))  # or 395?


if __name__ == '__main__':
    unittest.main()

# N = 200
# (1, 7, 16)
# (8, 9, 39)
# (11, 21, 72)
# (15, 32, 105)
# (13, 40, 115)
# (15, 65, 168)
# (3, 104, 189)


# sq_r = (z**2 + 17*z*y + y**2)**0.5
# z=48, y=3, sq_r=69
# z=48, y=14, sq_r=118
# z=48, y=21, sq_r=141
# z=48, y=31, sq_r=169

# z = 48, y^2 + 816y + 2304 = square = k^2
# (y+408+k)*(y+408-k) = 408^2 - 2304

# in general, x,y,z,k all int
# (2y+17z)^2 - (2k)^2 = 285*z^2 = 3*5*19*z^2
# and
# 15x - 17(y+z) = +/- 8k

# therefore x+y+z == 0 mod 8
