"""
PROBLEM

The number 209 can be expressed as  in two distinct ways:
209 = 8^2 + 3*8*5 + 5^2
209 = 13^2 + 3*13*1 + 1^2

Let f(n,r) be the number of integers k not exceeding n that can be expressed as
k=a^2 + 3ab + b^2, with a>b>0 integers, in exactly r different ways.

You are given that f(10^5, 4) = 237 and f(10^8, 6) = 59517.

Find f(10^15, 40).

ANSWER:
Solve time: ~ seconds
"""

from util.utils import timeit
import unittest


def g(a: int, b: int) -> int:
    return a**2 + 3*a*b + b**2


def g2(z: int, b: int) -> int:
    return z**2 - 5*b**2


# k = a^2 + 3ab + b^2 = (a+b)^2 + ab
# [
# (66671, [(121, 110), (151, 82), (178, 59), (193, 47), (206, 37), (242, 11)]),
# (71269, [(131, 108), (157, 84), (165, 77), (212, 39), (220, 33), (261, 4)]),
# (94259, [(154, 121), (169, 107), (218, 65), (223, 61), (257, 35), (275, 22)])
# ]

# 66671 = (121 + 110)^2 + 121*110 = 231^2 + 121*110
# 66671 = (151 + 82 )^2 + 151*82  = 233^2 + 151*82
# 66671 = (178 + 59 )^2 + 178*59  = 237^2 + 178*59

# a^2 + 3ab + b^2 = n
# a^2 + 3ab + b^2 = (a+b)^2 + ab
# set q = a+b
# (a+b)^2 + ab = q^2 + (q-b)*b = q^2 + qb - b^2

# multiply by 4 then factor:
# q^2 + qb - b^2 = n
# 4q^2 + 4qb - 4b^2 = 4n
# (2q+b)^2 - b^2 - 4b^2 = 4n
# (2q+b)^2 - 5b^2 = 4n
# set z = 2q+b
# z^2 - 5b^2 = 4n, where z = 2a + 3b

#  a>b>0 integers condition
#  integer and b>0 is easily carried over.
#  a>b implies that z = 2a + 3b > 5b

# therefore for a given n need number of (z,b) such that z^2 - 5b^2 = 4n, and z > 5b > 0


class Problem586:
    def __init__(self):
        pass

    @staticmethod
    def direct_form(n: int, r: int) -> int:
        """
        Return be the number of integers k not exceeding n that can be expressed as
        k=a^2 + 3ab + b^2, with a>b>0 integers, in exactly r different ways.
        """
        dc = dict()
        max_a_real = ((5+4*n)**0.5 - 3) / 2  # taken from a>b>0
        max_a_int = int(max_a_real)

        for a in range(1, max_a_int+1):
            # print(f'a = {a}')
            max_b_real = ((5*a*a + 4*n)**0.5 - 3*a) / 2  # taken from a>b>0
            max_b_int = min(int(max_b_real), a-1)
            # max_b_int = int(max_b_real)
            # for b in range(1, max_b_int + 1, a):
            for b in range(1, max_b_int + 1):
                t = g(a, b)
                dc[t] = dc.get(t, []) + [(a, b)]

        # print(dc)
        ls_r = [(k, v) for k, v in dc.items() if len(v) == r]
        print(ls_r)

        return len(ls_r)

    @staticmethod
    def adjusted_form(n: int, r: int) -> int:
        """
        Return be the number of integers k not exceeding n that can be expressed as
        4k = z^2 - 5b^2, and z > 5b > 0, and z, b integers in exactly r different ways.
        """
        dc = dict()
        # smallest value of b=1, therefore largest value of z is 4k + 5 = z^2, z = sqrt(4n + 5)
        max_z_int = int((5 + 4 * n) ** 0.5)

        for z in range(6, max_z_int + 1):
            # print(f'z = {z}')
            # 5b^2 = z^2 - 4k
            # b = sqrt((z^2 - 4k)/5)
            # max_b_real = ((z**2 - 4 * n) / 5) ** 0.5
            # max_b_int = min(int(max_b_real), 5*z - 1)
            max_b_int = z//5 - 1
            for b in range(1, max_b_int + 1):
                t = g2(z, b)
                if t % 4 == 0 and t > 0:
                    dc[t//4] = dc.get(t//4, []) + [(z, b)]

        # print(dc)
        ls_r = [(k, v) for k, v in dc.items() if len(v) == r]
        print(ls_r)

        return len(ls_r)

    @timeit
    def solve(self, n, r):
        return self.direct_form(n, r)
        # return self.adjusted_form(n, r)


class Solution586(unittest.TestCase):
    def setUp(self):
        self.problem = Problem586()

    def test_no_solution(self):
        self.assertEqual(0, self.problem.solve(n=208, r=2))

    def test_first_solution(self):
        self.assertEqual(1, self.problem.solve(n=209, r=2))

    def test_small_solution(self):
        self.assertEqual(237, self.problem.solve(n=int(1e5), r=4))
        # self.assertEqual(237, self.problem.solve(n=int(1e5), r=6))

    def test_1e6_solution(self):
        self.assertEqual(6, self.problem.solve(n=int(1e6), r=5))

    def test_5e6_solution(self):
        self.assertEqual(50, self.problem.solve(n=int(5e6), r=5))

    # def test_second_small_solution(self):
    #     self.assertEqual(59517, self.problem.solve(n=int(1e8), r=6))


if __name__ == '__main__':
    unittest.main()


# [
# (66671, [(121, 110), (151, 82), (178, 59), (193, 47), (206, 37), (242, 11)]),
# (71269, [(131, 108), (157, 84), (165, 77), (212, 39), (220, 33), (261, 4)]),
# (94259, [(154, 121), (169, 107), (218, 65), (223, 61), (257, 35), (275, 22)])
# ]

# real
# [(209, [(8, 5), (13, 1)])]

# a,b = (8,5) -> (z,b) = (31,5)
# a,b = (13,1) -> (z,b) = (29,1)


# 4k + 5b^2 = z^2
# 4*209 + 5b^2 = z^2
# 836 + 5b^2 = z^2

# z > 5b > 0
# z^2 > 25 b^2 > 0

# 4*209 + 5b^2 = z^2 > 25 b^2
# 4*209 > 20 b^2
# 209/5 > b^2
# b < sqrt(209/5)
