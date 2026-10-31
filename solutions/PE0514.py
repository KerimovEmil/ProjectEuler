"""
PROBLEM

A geoboard (of order N) is a square board with equally-spaced pins protruding from the surface,
representing an integer point lattice for coordinates 0 <= x, y <= N.

John begins with a pinless geoboard. Each position on the board is a hole that can be filled with a pin.
John decides to generate a random integer between 1 and N + 1 (inclusive) for each hole in the geoboard.
If the random integer is equal to 1 for a given hole, then a pin is placed in that hole.

After John is finished generating numbers for all (N + 1)^2 holes and placing any/all corresponding pins,
he wraps a tight rubberband around the entire group of pins protruding from the board. Let S represent
the shape that is formed. S can also be defined as the smallest convex shape that contains all the pins.

Let E(N) be the expected area of S given a geoboard of order N.
For example, E(1) = 0.18750, E(2) = 0.94335, and E(10) = 55.03013 when rounded to five decimal places each.

Calculate E(100) rounded to five decimal places.

ANSWER: 8986.86698
Solve time: ~1.05 seconds

---
MATHEMATICAL DERIVATION:

1. Linearity of Expectation and the Shoelace Formula:
   By the Shoelace formula, the area of any counter-clockwise simple polygon with vertices P_0, ..., P_{k-1} is:
     Area = (1 / 2) * sum_{i=0}^{k-1} ((x_i - cx) * (y_{i+1} - cy) - (y_i - cy) * (x_{i+1} - cx)),
   where (cx, cy) = (N / 2, N / 2) is the geometric center of the [0, N]^2 board.
   By linearity of expectation, the expected area equals the sum over all possible directed lattice line segments
   P_1 -> P_2 of:
     (1 / 2) * Cross(P_1 - C, P_2 - C) * Pr(P_1 -> P_2 is a directed edge of the convex hull).
   (Note: If all pins are collinear, the forward and backward extreme segments cancel out with opposite signed
   areas, yielding exactly 0 expected area as specified).

2. Probability of a Hull Edge:
   A directed segment P_1 -> P_2 is a CCW convex hull edge if and only if:
   - Both P_1 and P_2 contain pins (each chosen with probability p = 1 / (N + 1)).
   - No points on the open line segment P_1 P_2 or on the line outside the segment contain pins.
   - No points strictly to the right of the directed line P_1 -> P_2 contain pins.
   If 'excluded' is the number of lattice points that must not contain pins, the probability is:
     p^2 * (1 - p)^{excluded}.

3. Aggregation along Lattice Lines:
   For any primitive direction (ux, uy) with gcd(ux, uy) = 1 (1 <= ux, uy <= N):
   - All lattice points on a line L with normal direction have a constant projection C = x * uy - y * ux.
   - For a line containing M >= 2 lattice points, the cross product with the center C depends only on C and
     the step separation k = j - i:
       Cross(P_i - C, P_j - C) = k * (C - (cx * uy - cy * ux)).
   - Summing over all pairs 0 <= i < j < M on the line:
       W(M) = p^2 * sum_{k=1}^{M-1} (M - k) * k * (1 - p)^{M - 1 - k}.
   - The number of points strictly to the right of the line is given by the suffix sum of point counts for lines
     with larger values of C.

4. Symmetry Reduction:
   By 4-fold rotational symmetry around (cx, cy), the total expected area equals 4 times the sum over the positive
   quadrant (dx > 0, dy >= 0), evaluated in O(N^3) time (~1.05s for N = 100).
"""

import math
import unittest
import numpy as np
from util.utils import timeit


class Problem514:
    def __init__(self, n: int = 100):
        self.n = n

    @staticmethod
    def expected_area(n: int) -> float:
        p = 1.0 / (n + 1)
        q = 1.0 - p
        q_pow = np.power(q, np.arange((n + 1) ** 2 + 1))
        cx = n / 2.0
        cy = n / 2.0
        total_expected_twice_area = 0.0

        # Horizontal edges: dy == 0, dx > 0
        for y in range(n + 1):
            for dx in range(1, n + 1):
                count_x = n + 1 - dx
                excluded = y * (n + 1) + (n - dx)
                prob = p * p * float(q_pow[excluded])
                cross = -dx * (y - cy)
                total_expected_twice_area += count_x * prob * cross

        # Weight table for line segments with M lattice points
        w_table = np.zeros(n + 2)
        for m in range(2, n + 2):
            s = 0.0
            for k in range(1, m):
                s += (m - k) * k * float(q_pow[m - 1 - k])
            w_table[m] = p * p * s

        grid_idx = np.arange(n + 1, dtype=np.int32)
        for ux in range(1, n + 1):
            for uy in range(1, n + 1):
                if math.gcd(ux, uy) != 1:
                    continue
                offset = n * ux
                size = n * (ux + uy) + 1
                counts = np.zeros(size, dtype=np.int32)

                # Starting points with x0 < ux and 0 <= y0 <= n
                x0 = np.arange(ux, dtype=np.int32)[:, None]
                y0 = grid_idx[None, :]
                idx1 = x0 * uy - y0 * ux + offset
                m1 = np.minimum((n - x0) // ux, (n - y0) // uy) + 1
                counts[idx1.ravel()] = m1.ravel()

                # Starting points with y0 < uy and ux <= x0 <= n
                if ux <= n:
                    x0_2 = np.arange(ux, n + 1, dtype=np.int32)[:, None]
                    y0_2 = np.arange(uy, dtype=np.int32)[None, :]
                    idx2 = x0_2 * uy - y0_2 * ux + offset
                    m2 = np.minimum((n - x0_2) // ux, (n - y0_2) // uy) + 1
                    counts[idx2.ravel()] = m2.ravel()

                # Suffix sum of counts: points strictly to the right of the line
                rev_cum = np.cumsum(counts[::-1])[::-1]
                below = np.empty_like(rev_cum)
                below[:-1] = rev_cum[1:]
                below[-1] = 0

                mask = counts >= 2
                m_vals = counts[mask]
                b_vals = below[mask]
                c_vals = np.nonzero(mask)[0] - offset - (cx * uy - cy * ux)
                total_expected_twice_area += float(np.sum(w_table[m_vals] * q_pow[b_vals] * c_vals))

        return 2.0 * total_expected_twice_area

    @timeit
    def solve(self) -> float:
        return round(self.expected_area(self.n), 5)


class Solution514(unittest.TestCase):
    def setUp(self):
        self.problem = Problem514()

    def test_sample(self):
        self.assertAlmostEqual(0.18750, self.problem.expected_area(1), places=5)
        self.assertAlmostEqual(0.94335, self.problem.expected_area(2), places=5)
        self.assertAlmostEqual(55.03013, self.problem.expected_area(10), places=5)

    def test_solution(self):
        self.assertEqual(8986.86698, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
