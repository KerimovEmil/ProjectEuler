"""
PROBLEM

The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of
the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

d2d3d4=406 is divisible by 2
d3d4d5=063 is divisible by 3
d4d5d6=635 is divisible by 5
d5d6d7=357 is divisible by 7
d6d7d8=572 is divisible by 11
d7d8d9=728 is divisible by 13
d8d9d10=289 is divisible by 17
Find the sum of all 0 to 9 pandigital numbers with this property.

ANSWER:
16695334890
Solve time ~0.007 seconds
"""

# d2 d3 d4 is divisible by 2 implies d4 = 0,2,4,6,8
# d3 d4 d5 is divisible by 3 implies d3 + d4 + d5 is divisible by 3
# d4 d5 d6 is divisible by 5 implies d6 = 0 or 5
# d5 5 d7 is divisible by 7 implies d5 d7 = (1,4), (2,9), (3,0), (3,7), (6,1), (6,8), (7,6), (8,4), (9,2)
# d6 d7 d8 is divisible by 11 implies d6 cant be 0, since 11, 22, .. 99, are not unique digits
# Therefore d6 = 5, and d7 d8 = (0,6), (1,7), (2,8), (3,9), (6,1), (7,2), (8,3), (9,4)
# note that (5,0) can't work since d6 = 5.

# d7 d8 d9 is divisible by 13, with the div by 11 conditions implies:
# d7 d8 d9 = (2,8,6), (3,9,0), (7,2,8), (8,3,2)

# d8 d9 d10 is divisible by 17 with the 13 condition implies:
# d6 d7 d8 d9 d10 = (5,2,8,6,7), (5,3,9,0,1), (5,7,2,8,9)

# combining this with the div by 7 condition:
# d5 d6 d7 d8 d9 d10 = (9,5,2,8,6,7), (3,5,7,2,8,9)

# follow this logic for 3 and 2 divisibility to get the answer. This is the basis
# for the smarter/faster solution of this problem.


import itertools

import unittest
from util.utils import timeit


class DumbProblem43:  # takes ~16 seconds
    def __init__(self, n_criteria):
        self.ans = 0
        self.n_criteria = n_criteria
        self.ls_pandigitals = itertools.permutations(range(10))
        self.ls_small_primes = [2, 3, 5, 7, 11, 13, 17]

    def check(self, str_num):
        for i in range(self.n_criteria):
            if int(str_num[i + 1:i + 4]) % self.ls_small_primes[i]:
                return False
        return True

    @timeit
    def solve(self):
        for pan_digit in self.ls_pandigitals:
            str_num = ''.join(map(str, list(pan_digit)))
            if self.check(str_num):
                self.ans += int(str_num)
        return self.ans


class Problem43:
    def __init__(self, n_criteria):
        self.ans = 0
        self.n_criteria = n_criteria
        self.ls_small_primes = [1, 2, 3, 5, 7, 11, 13, 17]

    def check(self, str_num):
        for i in range(self.n_criteria):
            if int(str_num[i + 1:i + 4]) % self.ls_small_primes[i]:
                return False
        return True

    @timeit
    def solve(self):
        # all possible last two digits
        ls_possible = [(x, y) for x in range(10) for y in range(10) if y != x]

        # looping over divisor criteria to reduce space
        for condition in range(self.n_criteria + 1)[::-1]:
            print("Condition: {} has {} starting solution space".format(condition, len(ls_possible)))
            q = ls_possible
            ls_possible = []
            for tup in q:
                for i in range(10):
                    if i not in tup:
                        test = int(''.join([str(i)] + [str(d) for d in tup[0:2]]))
                        if test % self.ls_small_primes[condition] == 0:
                            ls_possible.append((i,) + tup)

        # add all solutions which remain
        for tup in ls_possible:
            self.ans += int(''.join(map(str, list(tup))))
        return self.ans


class Solution43(unittest.TestCase):
    def setUp(self):
        self.problem = Problem43(n_criteria=7)

    def test_solution(self):
        self.assertEqual(16695334890, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
