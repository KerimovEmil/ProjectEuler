"""
Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.


Working clockwise, and starting from the group of three with the numerically lowest external node
(4,3,2 in this example), each solution can be described uniquely. For example, the above solution
can be described by the set: 4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight
solutions in total.

Total	Solution Set
9	4,2,3; 5,3,1; 6,1,2
9	4,3,2; 6,2,1; 5,1,3
10	2,3,5; 4,5,1; 6,1,3
10	2,5,3; 6,3,1; 4,1,5
11	1,4,6; 3,6,2; 5,2,4
11	1,6,4; 5,4,2; 3,2,6
12	1,5,6; 2,6,4; 3,4,5
12	1,6,5; 3,5,4; 2,4,6
By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon ring
is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings.
 What is the maximum 16-digit string for a "magic" 5-gon ring?

ANSWER: 6531031914842725
Solve time: 0 seconds
"""

from util.utils import timeit
import unittest


# paper and pencil method.
# maximizing the sum would result in the numbers 6,7,8,9,10 in the outer ring and 1,2,3,4,5 in the inner
# given this assumption we must have 2*(1+2+3+4+5) + (6+7+8+9+10) = 70
# this implies that each line adds up to 14.

# Since we start with the lowest number in the outer ring we can use 6 as the starting point, and then the next
# largest inner number (5).
# Therefore, the first line is 6,5,3
# That implies that the next line must be 10,3,1 since we need to place 10 somewhere
# by some trial and error we have to fill the next line as 4,1,9 and the last one needs to be 7,2,5
# this only leaves the line 2,4,8
# combining everything we get 6531031914842725


class Problem68:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        return 6531031914842725


class Solution68(unittest.TestCase):
    def setUp(self):
        self.problem = Problem68()

    def test_solution(self):
        self.assertEqual(6531031914842725, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

