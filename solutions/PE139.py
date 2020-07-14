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
Solve time ~9.5 seconds
"""

from util.utils import timeit
import unittest
from math import gcd


class Problem139:
    def __init__(self):
        pass

    @timeit
    def solve(self, max_p):
        count = 0
        max_m = int((max_p/2)**0.5) + 1
        for m in range(2, max_m):
            for n in range(1, m):
                if (n + m) % 2 != 1:  # different parity
                    continue
                if gcd(m, n) != 1:  # this is already counted in the sum
                    continue

                # Use Pythagorean triples
                a, b, c = m*m - n*n, 2*m*n, m*m + n*n
                p = a + b + c
                if p >= max_p:
                    break
                if c % (b-a) == 0:
                    count += max_p // p

        return count


class Solution139(unittest.TestCase):
    def setUp(self):
        self.problem = Problem139()

    def test_solution(self):
        limit = int(1e8)
        self.assertEqual(10057761, self.problem.solve(max_p=limit))


if __name__ == '__main__':
    unittest.main()

