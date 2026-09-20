"""
Let (a, b, c) represent the three sides of a right angle triangle with integral length sides.
It is possible to place four such triangles together to form a square with length c.

For example, (3, 4, 5) triangles can be placed together to form a 5 by 5 square with a 1 by 1 hole in the middle and
 it can be seen that the 5 by 5 square can be tiled with twenty-five 1 by 1 squares.

However, if (5, 12, 13) triangles were used then the hole would measure 7 by 7 and these could not be used to tile the
 13 by 13 square.

Given that the perimeter of the right triangle is less than one-hundred million, how many Pythagorean triangles would
 allow such a tiling to take place?

ANSWER: 10057761
Solve time: ~9.5 seconds using brute force
Solve time: ~0.003 seconds using pell equations
"""

from math import gcd

import unittest
from util.utils import timeit


# set up
# if m, n are co-prime, and m<n<0, and different parity then we have
# a = m^2 - n^2, b = 2mn, c = m^2 + n^2
# perimeter = a + b + c = 2m(m+n) < 1e8
# gap = b - a

# simple solution:
# loop over m from 1 to 1e4, and check if gap divides c, if it does then add all of the multiples possible

# better solution:
# area of gap = (b-a)^2 and area of gap = c^2 - 2ab
# Therefore for gap to divide c, (b-a)|c, it implied (b-a)^2|c^2, therefore we only need to check if (b-a)^2 | 2ab
# note that since gcd(a,b) = 1, then this implies that b - a = 1. i.e. a^2 + (a + 1)^2 = c^2
# therefore  n^2 + 2mn - m^2 = -1 = (n - m)^2 - 2 m^2
# this is the Pell equation for d = 2 (x^2 - 2y^2 = -1), i.e. a convergent of sqrt(2)

# initial solution that works, is 7^2 - 2*5^2 = 49 - 50 = -1
# smallest solution to x^2 - 2y^2 = 1 is 3^2 - 2*2^2 = 9 - 8 = 1. Hence 3 + 2*sqrt(2) is a unit

class Problem139:
    def __init__(self):
        pass

    @timeit
    def simple_solve(self, max_p):
        count = 0
        max_m = int((max_p / 2) ** 0.5) + 1
        for m in range(2, max_m):
            for n in range(1, m):
                if (n + m) % 2 != 1:  # different parity
                    continue
                if gcd(m, n) != 1:  # this is already counted in the sum
                    continue

                # Use Pythagorean triples
                a, b, c = m * m - n * n, 2 * m * n, m * m + n * n
                p = a + b + c
                if p >= max_p:
                    break
                if c % (b - a) == 0:
                    count += max_p // p

        return count

    @timeit
    def pell_equation_solve(self, max_p):
        """See here for implementation https://projecteuler.net/thread=139;page=4"""
        x, y, count = 7, 5, 0
        # 7^2 - 2*5^2 = 49 - 50 = -1
        while x + y < max_p:
            count += (max_p - 1) // (x + y)
            # 3^2 - 2*2^2 = 9 - 8 = 1, therefore 3 + 2*sqrt(2) is a unit, hence we get all other solutions by
            # multiplying by 3 + 2*sqrt(2)
            # (x + y*sqrt(2)) * (3 + 2*sqrt(2)) = (3x + 4y) + (2x + 3y)*sqrt(2)
            x, y = 3 * x + 4 * y, 2 * x + 3 * y
        return count


class Solution139(unittest.TestCase):
    def setUp(self):
        self.problem = Problem139()

    def test_solution(self):
        limit = int(1e8)
        self.assertEqual(10057761, self.problem.pell_equation_solve(max_p=limit))


if __name__ == '__main__':
    unittest.main()
