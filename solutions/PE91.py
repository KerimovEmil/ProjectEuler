"""
The points P(x1,y1) and Q(x2,y2) are plotted at integer co-ordinates and are joined to the origin, O to form OPQ.

There are exactly fourteen triangles containing a right angle that can be formed when each co-ordinate lies between
0 and 2 inclusive; that is, 0<= x1,x2,y1,y2 <=2

Given that 0<= x1,x2,y1,y2 <=50, how many right triangles can be formed?

ANSWER: 14234
Solve time ~0.6 seconds
"""

import unittest


# divide into cases of where the right angle is:
# case 1 - right angle at origin
#   - n options for x, n options for y -> n^2 options
# case 2 - right angle on y-axis
#   - n options for x, n options for y -> n^2 options
# case 3 - right angle on y-axis
#   - n options for y, n options for x -> n^2 options
# case 4 - right angle not on the axis - more complicated case
#   - if we define the line from O to P as "a" and the line from P to Q as "b"
#     then the criteria is "a" dot "b" = 0 implies that the lines are perpendicular.
#     therefore: x1 * (x2 - x1) + y2 * (y2 - y1) = 0


class Problem91:
    def __init__(self):
        pass

    @staticmethod
    def solve(n: int):
        ans = 3 * (n**2)

        for x1 in range(1, n + 1):
            for x2 in range(x1, n + 1):
                for y1 in range(1, n + 1):
                    for y2 in range(0, y1):
                        if x1 * (x2 - x1) == -y1 * (y2 - y1):
                            ans += 2
        return ans

class Solution91(unittest.TestCase):
    def setUp(self):
        self.problem = Problem91()

    def test_sample_solution(self):
        self.assertEqual(14, self.problem.solve(n=2))

    def test_solution(self):
        self.assertEqual(14234, self.problem.solve(n=50))


if __name__ == '__main__':
    unittest.main()
