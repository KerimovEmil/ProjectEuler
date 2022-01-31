"""
PROBLEM

There are several ways to write the number 1/2 as a sum of inverse squares using distinct integers.

For instance, the numbers {2,3,4,5,7,12,15,20,28,35} can be used.

In fact, only using integers between 2 and 45 inclusive, there are exactly three ways to do it,
the remaining two being: {2,3,4,6,7,9,10,20,28,35,36,45} and
 {2,3,4,6,7,9,12,15,28,30,35,36,45}.

How many ways are there to write the number 1/2 as a sum of inverse squares using distinct integers between 2 and 80 inclusive?

ANSWER: 301
Solve time ~56 seconds  # todo work on speeding this up
"""
from util.utils import timeit
import unittest
from fractions import Fraction

# ls_candidates = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 18, 20, 21, 24, 28,
#                  30, 35, 36, 39, 40, 42, 45, 52, 56, 60, 63, 70, 72]
# list of candidates can be reduced from range(1, 81) to this list by considering the only prime factors must be
# 2, 3, 5, 7 and 13, and multiples of those primes.
# Further additional numbers can be eliminated by considering mod n for the final equation.
# see https://projecteuler.net/thread=152 for further discussion on this.


def sum_of_recip_sq_frac(s):
    return sum(Fraction(1, i**2) for i in s)


def subset_sum(numbers, target, partial=None, partial_sum=Fraction(0, 1)):
    if partial is None:
        partial = []
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    if sum_of_recip_sq_frac(numbers) < (target - partial_sum):
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + Fraction(1, n**2))


class Problem152:
    def __init__(self, target: Fraction):
        self.target = target

    @timeit
    def solve(self, ls_numbers: list):
        count = 0
        for sol in subset_sum(ls_numbers, self.target):
            print(sol)
            count += 1
        return count


class Solution152(unittest.TestCase):
    def setUp(self):
        self.problem = Problem152(target=Fraction(1, 2))

    def test_simple_solution(self):
        """Only three solution with numbers from 2 to 45"""
        ls_candidates = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 39, 40, 42, 45]
        self.assertEqual(3, self.problem.solve(ls_numbers=ls_candidates))

    def test_solution(self):
        ls_candidates = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 18, 20, 21, 24, 28,
                         30, 35, 36, 39, 40, 42, 45, 52, 56, 60, 63, 70, 72]
        self.assertEqual(301, self.problem.solve(ls_numbers=ls_candidates))


if __name__ == '__main__':
    unittest.main()
