"""
PROBLEM

Three distinct points are plotted at random on a Cartesian plane, for which
-1000 <= x,y <= 1000, such that a triangle is formed.

Consider the following two triangles:
A(-340,495), B(-153, -910), C(835,-947)
X(-175,41), Y(-421, -714), Z(574,-645)

It can be verified that triangle ABC contains the origin, whereas triangle XYZ does not.

find the number of triangles for which the interior contains the origin.

ANSWER: 228
Solve time: ~14 milliseconds
"""

from util.utils import timeit
import unittest
import os


def is_in_triangle(p: tuple[int, int], v1: tuple[int, int], v2: tuple[int, int], v3: tuple[int, int]) -> bool:
    """
    Return True if point p is in the triangle defined by the vertices v1,v2, & v3.
    Args:
        p: point to test
        v1: vertex 1
        v2: vertex 2
        v3: vertex 3

    Returns: True if point is in triangle
    """

    area = 0.5 * (-v2[1] * v3[0] + v1[1] * (-v2[0] + v3[0]) + v1[0] * (v2[1] - v3[1]) + v2[0] * v3[1])

    s = 1 / (2 * area) * (v1[1] * v3[0] - v1[0] * v3[1] + (v3[1] - v1[1]) * p[0] + (v1[0] - v3[0]) * p[1])
    t = 1 / (2 * area) * (v1[0] * v2[1] - v1[1] * v2[0] + (v1[1] - v2[1]) * p[0] + (v2[0] - v1[0]) * p[1])

    return (s >= 0) and (t >= 0) and (1-s-t >= 0)


class Problem102:
    def __init__(self, data):
        self.data = data

    @timeit
    def solve(self):
        num_in = 0
        for row in self.data:
            num_in += is_in_triangle(p=(0, 0), v1=row[0:2], v2=row[2:4], v3=row[4:6])
        return num_in


class Solution102(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p102_triangles.txt')
        with open(file_path) as f:
            triangle = [[int(n) for n in s.split(',')] for s in f.readlines()]

        self.problem = Problem102(triangle)

    def test_in_triangle(self):
        """origin in A(-340,495), B(-153, -910), C(835,-947)"""
        self.assertTrue(is_in_triangle(p=(0, 0), v1=(-340, 495), v2=(-153, -910), v3=(835, -947)))

    def test_not_in_triangle(self):
        """origin not in X(-175,41), Y(-421, -714), Z(574,-645)"""
        self.assertFalse(is_in_triangle(p=(0, 0), v1=(-175, 41), v2=(-421, -714), v3=(574, -645)))

    def test_solution(self):
        self.assertEqual(228, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
