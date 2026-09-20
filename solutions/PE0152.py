"""
PROBLEM

There are several ways to write the number 1/2 as a sum of inverse squares using distinct integers.

For instance, the numbers {2,3,4,5,7,12,15,20,28,35} can be used.

In fact, only using integers between 2 and 45 inclusive, there are exactly three ways to do it,
the remaining two being: {2,3,4,6,7,9,10,20,28,35,36,45} and
 {2,3,4,6,7,9,12,15,28,30,35,36,45}.

How many ways are there to write the number 1/2 as a sum of inverse squares
 using distinct integers between 2 and 80 inclusive?

ANSWER: 301
Solve time: ~27 seconds
"""
from util.utils import timeit
import unittest
from fractions import Fraction

# to reduce the list of possible candidates to add we can do some pre-work by consider the integer only equation of:
# lcm(2^2,..,80^2) / 2 = lcm(1^2,..,80^2)/2^2 + ... + lcm(1^2,..,80^2)/80^2

# taking mod 121 of each term, we see that the LHS is 0 while the RHS only has the following terms as non-zero:
# lcm(1^2,..,80^2)/11^2 == 56 mod 121
# lcm(1^2,..,80^2)/22^2 == 14 mod 121
# lcm(1^2,..,80^2)/33^2 == 60 mod 121
# lcm(1^2,..,80^2)/44^2 == 64 mod 121
# lcm(1^2,..,80^2)/55^2 == 70 mod 121
# lcm(1^2,..,80^2)/66^2 == 15 mod 121
# lcm(1^2,..,80^2)/77^2 == 53 mod 121
# since all possible subset sums of 6, 14, 60, 64, 70, 15, 53 are all not multiples of 121
# we can remove all multiples of 11's.

# considering mod 17^2 = 289, we can remove all multiples of 17 since the only non-zero terms are:
# lcm(1^2,..,80^2)/17^2 == 104 mod 289
# lcm(1^2,..,80^2)/34^2 == 26 mod 289
# lcm(1^2,..,80^2)/51^2 == 140 mod 289
# lcm(1^2,..,80^2)/68^2 == 151 mod 289
# since all possible subset sums of 104, 26, 140, 151 are all not multiples of 289
# we can remove all multiples of 17's.

# The same analysis can be done on every prime squared larger than 13:
# 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79
# to remove all multiples of those primes.

# consider special case of p=13:
# taking mod 169 of each term, we see that the LHS is 0 while the RHS only has the following terms as non-zero:
# lcm(1^2,..,80^2)/13^2 == 22 mod 169
# lcm(1^2,..,80^2)/26^2 == 90 mod 169
# lcm(1^2,..,80^2)/39^2 == 40 mod 169
# lcm(1^2,..,80^2)/52^2 == 107 mod 169
# lcm(1^2,..,80^2)/65^2 == 82 mod 169
# lcm(1^2,..,80^2)/78^2 == 10 mod 169
# note that the only subset that adds up to a multiple of 169 is 22 + 40 + 107 = 169.
# That is the only subset. Therefore if we include 13 we must include 1/13^2 * (1 + 1/3^2 + 1/4^2)
# this corresponds to 1/13^2 + 1/39^2 + 1/52^2 = 1/12^2
# Hence we can remove all multiples of 13 and replace it with another possible 12.

# We can also remove all multiples of 25
# taking mod 25 of each term, we see that the LHS is 0 while the RHS only has the following 3 terms as non-zero:
# lcm(1^2,..,80^2)/25^2 == 6 mod 25
# lcm(1^2,..,80^2)/50^2 == 14 mod 25
# lcm(1^2,..,80^2)/75^2 == 9 mod 25
# since 6, 14, 9, 6+14, 6+9, 9+14, 6+14+9 are all not multiples of 25, we can remove all multiples of 25

# We can also remove 32 and 64 in the same way:
# lcm(2^2,..,80^2) / 2 = lcm(1^2,..,80^2)/2^2 + ... + lcm(1^2,..,80^2)/80^2
# taking mod 16 of each term, we see that the LHS is 0 while the RHS only has the following 3 terms as non-zero:
# lcm(1^2,..,80^2)/32^2 == 4 mod 16
# lcm(1^2,..,80^2)/64^2 == 9 mod 16
# since 4+9 are not multiples of 16, we can remove 32 and 64.

# considering mod 3 we can eliminate 27 and 54 since the only non-zero terms are:
# lcm(1^2,..,80^2)/27^2 == 1 mod 3
# lcm(1^2,..,80^2)/54^2 == 1 mod 3

# considering mod 64 we can eliminate 16, 32, 48, 64, and 80 since the only non-zero terms are:
# lcm(1^2,..,80^2)/16^2 == 16 mod 16
# lcm(1^2,..,80^2)/32^2 == 36 mod 16
# lcm(1^2,..,80^2)/48^2 == 16 mod 16
# lcm(1^2,..,80^2)/64^2 == 41 mod 16
# lcm(1^2,..,80^2)/80^2 == 16 mod 16
# since no combination of 16, 36, 16, 41, 16 will give a multiple of 64, we can eliminate 16, 32, 48, 64, and 80

# considering mod 7 we can eliminate 49 since that is the only non-zero term:
# lcm(1^2,..,80^2)/49^2 == 4 mod 7

# Therefore, in summary we can remove the following numbers
# [11, 16, 17, 19, 22, 23, 25, 26, 27, 29, 31, 32, 33, 34, 37, 38, 41, 43, 44, 46, 47, 48, 49, 50, 51, 53, 54, 55, 57,
# 58, 59, 61, 62, 64, 65, 66, 67, 68, 69, 71, 73, 74, 75, 76, 77, 78, 79, 80]

# which leaves the following candidates under 80:
# [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 39, 40, 42, 45, 52, 56, 60, 63,
# 70, 72]
# Since the 13 can only occur in 1/13^2+1/39^2+1/52^2 = 1/144 = 1/12^2, we can remove all 3 and just add an extra 12
# [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 12, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 40, 42, 45, 56, 60, 63, 70, 72]

# note that if we need to only use numbers less than 40, we should simply remove all 3.


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
    def __init__(self, target: Fraction, debug: bool = False):
        self.target = target
        self.debug = debug

    @timeit
    def solve(self, ls_numbers: list):
        count = 0
        for sol in subset_sum(ls_numbers, self.target):
            if self.debug:
                print(sol)
            count += 1
        return count


class Solution152(unittest.TestCase):
    def setUp(self):
        self.problem = Problem152(target=Fraction(1, 2))

    def test_simple_solution(self):
        """Only three solution with numbers from 2 to 45"""
        ls_candidates = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 40, 42, 45]
        self.assertEqual(3, self.problem.solve(ls_numbers=ls_candidates))

    def test_solution(self):
        ls_candidates = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 12, 14, 15, 18, 20, 21, 24, 28,
                         30, 35, 36, 40, 42, 45, 56, 60, 63, 70, 72]
        self.assertEqual(301, self.problem.solve(ls_numbers=ls_candidates))


if __name__ == '__main__':
    unittest.main()
