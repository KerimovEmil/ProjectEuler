r"""
PROBLEM

It is easily proved that no equilateral triangle exists with integral length sides and integral area.
However, the almost equilateral triangle $5$-$5$-$6$ has an area of $12$ square units.

We shall define an almost equilateral triangle to be a triangle for which two sides are equal
and the third differs by no more than one unit.

Find the sum of the perimeters of all almost equilateral triangles with integral side lengths and area
and whose perimeters do not exceed one billion ($1\,000\,000\,000$).

ANSWER: 518408346
Solve time: ~0.001 seconds
"""

import unittest

from util.utils import timeit


class Problem94:
    def __init__(self, limit=1_000_000_000):
        self.limit = limit

    @timeit
    def solve(self):
        # For an almost equilateral triangle with sides (a, a, c) and c = a ± 1:
        # Altitude squared: h^2 = a^2 - (c/2)^2 = (4a^2 - c^2) / 4
        # Case 1: c = a + 1 => 4a^2 - (a+1)^2 = 3a^2 - 2a - 1 = y^2
        #         Multiply by 3: (3a - 1)^2 - 3y^2 = 4 => x^2 - 3y^2 = 4 with x = 3a - 1 (x ≡ 2 mod 3)
        # Case 2: c = a - 1 => 4a^2 - (a-1)^2 = 3a^2 + 2a - 1 = y^2
        #         Multiply by 3: (3a + 1)^2 - 3y^2 = 4 => x^2 - 3y^2 = 4 with x = 3a + 1 (x ≡ 1 mod 3)
        #
        # Solutions to x^2 - 3y^2 = 4 are generated from (x_1, y_1) = (4, 2) and (x + y*sqrt(3))*(2 + sqrt(3)).
        x, y = 4, 2
        total_perimeter = 0

        while True:
            # Advance to next solution of Pell's equation x^2 - 3y^2 = 4
            x, y = 2 * x + 3 * y, x + 2 * y

            if x % 3 == 2:
                # c = a + 1
                a = (x + 1) // 3
                p = 3 * a + 1
                if p > self.limit:
                    break
                if a > 1:
                    total_perimeter += p
            elif x % 3 == 1:
                # c = a - 1
                a = (x - 1) // 3
                c = a - 1
                p = 3 * a - 1
                if p > self.limit:
                    break
                if c > 0:
                    total_perimeter += p

        return total_perimeter


class Solution94(unittest.TestCase):
    def setUp(self):
        self.problem = Problem94()

    def test_solution(self):
        self.assertEqual(518408346, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
