"""
PROBLEM

nI laser physics, a "white cell" is a mirror system that acts as a delay line for the laser beam. The beam enters the
cell, bounces around on the mirrors, and eventually works its way back out.
The specific white cell we will be considering is an ellipse with the equation 4x^2 + y^2 = 100

The section corresponding to −0.01 ≤ x ≤ +0.01 at the top is missing, allowing the light to enter and exit through the
hole.

he light beam in this problem starts at the point (0.0,10.1) just outside the white cell, and the beam first impacts
the mirror at (1.4,-9.6).
Each time the laser beam hits the surface of the ellipse, it follows the usual law of reflection "angle of incidence
equals angle of reflection." That is, both the incident and reflected beams make the same angle with the normal line at
the point of incidence.

In the figure on the left, the red line shows the first two points of contact between the laser beam and the wall of
the white cell; the blue line shows the line tangent to the ellipse at the point of incidence of the first bounce.

The slope m of the tangent line at any point (x,y) of the given ellipse is: m = −4x/y

The normal line is perpendicular to this tangent line at the point of incidence.

How many times does the beam hit the internal surface of the white cell before exiting?

ANSWER: 354
Solve time ~0.004 seconds
"""

from util.utils import timeit
import unittest
from typing import List, Tuple


class Problem144:
    def __init__(self, initial_point: Tuple[float, float], initial_slope: float):
        self.initial_point = initial_point
        self.initial_slope = initial_slope

    @staticmethod
    def normal_slope(x: float, y: float) -> float:
        """
        Return the slope of the normal line to the tangent for each point (x,y).
        Since normal is perpendicular to tangent, we have normal*tangent = -1
        normal*(-4x/y) = -1
        """
        return y/(4*x)

    @staticmethod
    def reflect_slope(initial_slope: float, normal_slope: float) -> float:
        """
        Returns the reflected slope. For reflections the following must hold:
        (m1 - m_normal) / (1+m_normal*m1) = (m_normal - m2) / (1+m_normal*m2)
        Solving this for m2 we get:
        m2 = (2*m_normal - m1 + m_normal^2* m1) / (2*m_normal*m1 - m_normal^2 +1)

        Details:
        (m1 - m_normal) * (1+m_normal*m2) / (1+m_normal*m1) = m_normal - m2
        m2 = m_normal - (m1 - m_normal) * (1+m_normal*m2) / (1+m_normal*m1)
        m2 = m_normal - (m1 - m_normal) / (1+m_normal*m1) - m_normal*m2* (m1 - m_normal) / (1+m_normal*m1)
        m2 * (1 + m_normal*(m1 - m_normal) / (1+m_normal*m1)) = m_normal - (m1 - m_normal) / (1+m_normal*m1)
        m2 = (m_normal - (m1 - m_normal) / (1+m_normal*m1)) / (1 + m_normal*(m1 - m_normal) / (1+m_normal*m1))
        m2 = (m_normal*(1+m_normal*m1) - (m1 - m_normal)) / (1 + m_normal*(m1 - m_normal))
        m2 = (2*m_normal + m_normal^2*m1 - m1) / (1 + m_normal*m1 - m_normal^2)
        """
        n, m = normal_slope, initial_slope
        return (2*n - m + m*n*n)/(2*m*n - n*n + 1)

    @staticmethod
    def next_point(m: float, c: float, x_old: float) -> Tuple[float, float]:
        """
        Solving for x,y intercepts of 4x^2 + y^2 = 100 and y = mx + c, given one of the solutions x_old

        Details
        4x^2 + (mx + c)^2 = 100
        4x^2 + m^2 x^2 + 2mxc + c^2  = 100
        (m^2 + 4)x^2 + (2mc)x + (c^2 - 100) = 0

        given that x_old is a solution, we have the following equation
        (m^2 + 4)x^2 + (2mc)x + (c^2 - 100) = (x - x_old) * (x - x_new)
        Therefore x_old * x_new = (c^2 - 100)/(m^2 + 4)
        x_new = (c^2 - 100)/(m^2 + 4)/x_old
        """
        x_new = (c*c-100)/(m*m+4)/x_old
        return x_new, m*x_new + c

    @timeit
    def solve(self):
        count = 0
        m = self.initial_slope
        x, y = self.initial_point[0], self.initial_point[1]

        while not (abs(x) <= 0.01 and y > 0):
            n = self.normal_slope(x=x, y=y)
            m = self.reflect_slope(initial_slope=m, normal_slope=n)
            x, y = self.next_point(m=m, c=y - m*x, x_old=x)
            count += 1
        return count

    @staticmethod
    def solve_with_no_description():
        x, y = 1.4, -9.6
        m = -197/14

        count = 0
        while not (abs(x) <= 0.01 and y > 0):
            # get new slope
            m = y*x*(1 + m*m)/(2*x*x + m*y*x - y*y/8) - m
            # get new point
            c = y - m*x
            x = (c*c-100)/(m*m+4)/x
            y = m*x + c

            count += 1
        return count


class Solution144(unittest.TestCase):
    def setUp(self):
        self.problem = Problem144(initial_point=(1.4, -9.6), initial_slope=-197/14)

    def test_solution(self):
        self.assertEqual(354, self.problem.solve())

    def test_no_description(self):
        self.assertEqual(354, self.problem.solve_with_no_description())


if __name__ == '__main__':
    unittest.main()

