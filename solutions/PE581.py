"""
A number is p-smooth if it has no prime factors larger than p.
Let T be the sequence of triangular numbers, i.e. T(n) = n(n+1)/2

Find the sum of all indices n such that T(n) is 47-smooth.

ANSWER: 2,227,616,372,734
Solve time: ~24 seconds

Key Idea:
Størmer's theorem - that is, all P-smooth consecutive numbers can be generated using the solution to Pell's equation
x^2 - dy^2 = 1.
Essentially, for every squarefree 47-smooth q not equal to 2, we solve sufficiently many solutions to x^2-dq y^2 = 1
For each solution, (x-1)/2 is a candidate for this problem's n.

See here for more details: https://en.wikipedia.org/wiki/St%C3%B8rmer%27s_theorem

Using that theorem and https://oeis.org/A117581 we get:
 the upperbound on consecutive 47-smooth numbers is 1,109,496,723,126
"""
from util.utils import timeit, smooth_numbers
import unittest


class Problem581:
    def __init__(self):
        self.ls_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    @timeit
    def solve(self):
        ls_47_smooth = smooth_numbers(current_prime_index=0, current_value=1, ls_primes=self.ls_prime,
                                      max_n=1_109_496_723_127)
        set_47_smooth = set(ls_47_smooth)
        # 2 consecutive smooth numbers implies that t(n) was also smooth, since n and n+1 are smooth
        return sum([n for n in set_47_smooth if n + 1 in set_47_smooth])


class Solution581(unittest.TestCase):
    def setUp(self):
        self.problem = Problem581()

    def test_solution(self):
        self.assertEqual(2_227_616_372_734, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
