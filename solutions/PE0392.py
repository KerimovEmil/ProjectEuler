"""
PROBLEM

A rectilinear grid is an orthogonal grid where the spacing between the gridlines does not have to be equidistant.

An example of such grid is logarithmic graph paper.

Consider rectilinear grids in the Cartesian coordinate system with the following properties:
- The gridlines are parallel to the axes of the Cartesian coordinate system.
- There are N+2 vertical and N+2 horizontal gridlines. Hence there are (N+1) x (N+1) rectangular cells.
- The equations of the two outer vertical gridlines are x = -1 and x = 1.
- The equations of the two outer horizontal gridlines are y = -1 and y = 1.
- The grid cells are colored red if they overlap with the unit circle (radius 1 centered at origin), black otherwise.

For this problem we would like you to find the positions of the remaining N inner horizontal and N inner vertical gridlines so that the area occupied by the red cells is minimized.

E.g. for N = 10, the area occupied by the red cells rounded to 10 digits behind the decimal point is 3.3469640797.

Find the positions for N = 400.
Give as your answer the area occupied by the red cells rounded to 10 digits behind the decimal point.

ANSWER: 3.1486734435
Solve time: ~0.005 seconds

---
MATHEMATICAL DERIVATION:

1. Symmetry and Boundary Points:
   By the fourfold rotational and reflection symmetry of the unit disk, the optimal grid is symmetric across
   the axes and the diagonal y = x.
   For N = 2k inner lines, there are k positive inner coordinates in each dimension:
   0 = x_0 < x_1 < x_2 < ... < x_k < x_{k+1} = 1, with y_i = x_i.
   A cell [x_i, x_{i+1}] x [y_j, y_{j+1}] overlaps the unit circle if and only if its closest point to the origin
   satisfies x_i^2 + y_j^2 <= 1.
   At optimality, the boundary cells of the staircase touch the circle:
   x_i^2 + x_{k+1-i}^2 = 1 for each i = 0, ..., k+1.
   Substituting x_i = sin(theta_i) with theta_0 = 0 and theta_{k+1} = pi/2, this implies:
   theta_{k+1-i} = pi/2 - theta_i, and x_{k+1-i} = cos(theta_i).

2. Total Area and Optimality Recurrence:
   The total area of the red cells across all four quadrants is:
   A = 4 * sum_{i=0}^k (sin(theta_{i+1}) - sin(theta_i)) * cos(theta_i)
   Setting d A / d theta_i = 0 yields:
   cos(theta_i) * cos(theta_{i-1}) - cos^2(theta_i) + sin^2(theta_i) - sin(theta_{i+1}) * sin(theta_i) = 0
   => sin(theta_{i+1}) = (cos(theta_i) * cos(theta_{i-1}) - cos(2 * theta_i)) / sin(theta_i)

3. 1D Shooting Method (Bisection):
   Given theta_0 = 0, every theta_i is uniquely determined once theta_1 is chosen.
   By symmetry:
   - If k is odd, the middle angle is theta_{(k+1)/2} = pi / 4.
   - If k is even, the two middle angles satisfy theta_{k/2} + theta_{k/2 + 1} = pi / 2.
   Since theta_{(k+1)/2} (or theta_{k/2} + theta_{k/2 + 1}) is strictly increasing with respect to theta_1,
   we solve for theta_1 via a binary search (shooting method) to high precision in O(k) steps.
"""

import math
import unittest
from util.utils import timeit


class Problem392:
    def __init__(self):
        pass

    def compute_min_area(self, n: int) -> float:
        k = n // 2
        half = k // 2
        is_k_odd = (k % 2 == 1)
        mid_idx = (k + 1) // 2

        low = 0.0
        high = math.pi / 2

        for _ in range(120):
            mid = (low + high) / 2
            thetas = [0.0, mid]
            valid = True

            target_steps = mid_idx if is_k_odd else half
            for i in range(1, target_steps + 1):
                num = math.cos(thetas[i]) * math.cos(thetas[i - 1]) - math.cos(2 * thetas[i])
                den = math.sin(thetas[i])
                if den == 0:
                    valid = False
                    break
                s_next = num / den
                if s_next > 1.0 or s_next < -1.0:
                    valid = False
                    break
                thetas.append(math.asin(s_next))

            if not valid:
                high = mid
                continue

            if is_k_odd:
                if thetas[mid_idx] > math.pi / 4:
                    high = mid
                else:
                    low = mid
            else:
                if (thetas[half] + thetas[half + 1]) > math.pi / 2:
                    high = mid
                else:
                    low = mid

        # Reconstruct full sequence
        target_steps = mid_idx if is_k_odd else half
        thetas = [0.0, low]
        for i in range(1, target_steps + 1):
            num = math.cos(thetas[i]) * math.cos(thetas[i - 1]) - math.cos(2 * thetas[i])
            den = math.sin(thetas[i])
            thetas.append(math.asin(num / den))

        full_thetas = [0.0] * (k + 2)
        for i in range(target_steps + 1):
            full_thetas[i] = thetas[i]
            full_thetas[k + 1 - i] = math.pi / 2 - thetas[i]

        area_q1 = 0.0
        for i in range(k + 1):
            area_q1 += (math.sin(full_thetas[i + 1]) - math.sin(full_thetas[i])) * math.cos(full_thetas[i])

        return 4.0 * area_q1

    @timeit
    def solve(self) -> str:
        area = self.compute_min_area(400)
        return f"{area:.10f}"


class Solution392(unittest.TestCase):
    def setUp(self):
        self.problem = Problem392()

    def test_sample(self):
        self.assertEqual("3.3469640797", f"{self.problem.compute_min_area(10):.10f}")

    def test_solution(self):
        self.assertEqual("3.1486734435", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
