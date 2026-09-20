"""
PROBLEM

In the following equation x, y, and n are positive integers.
1/x+1/y=1/n
For a limit L we define F(L) as the number of solutions which satisfy x < y ≤ L.

We can verify that F(15) = 4 and F(1000) = 1069.
Find F(10^12).

ANSWER:

Solve time ~ seconds
"""

# related problems 110 and 108

# Math proof:
# Use the fact that:
# 1/x + 1/y = 1/n for y,x,n positive integers:
#
# implies that xy/(x+y) = n.
# Notice that if we assume x<y then we must get that
# n < x < 2n; and y = xn/(x-n).
#
# The problem now boils down to when y is an integer for all integers of x between n+1 and 2n-1.
# This problem can be written as when x-n divides xn for x from n+1 to 2n-1.
# Notice that for x = n+i for i from 1 to n-1, this implies
# i divides n * (n+i) = n^2 + n * i.
# Since i divides n*i for sure, then we only need to find how many i divide n^2, for i in 1 to n-1.

# To find out how many i divide n^2, for i in 1 to n-1, if we write n = p1^a1 * p2^a2 * p3^a3
# Then the number of divisors of n^2 = (2 * a1 + 1) * (2 * a2 + 1) * (2 * a3 + 1) .
#
# By a neat symmetry argument we can show that number of those divisors that are less than or equal to n are:
# ((2 * a1 + 1) * (2 * a2 + 1) * (2 * a3 + 1) + 1) / 2
#
# Therefore we only need to find a few possible sets that equal the max number of unique solutions that we are
#  looking for, and then figure out which one of those sets correspond to the smallest number.



from util.utils import timeit
import unittest


class Problem454:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution454(unittest.TestCase):
    def setUp(self):
        self.problem = Problem454()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
