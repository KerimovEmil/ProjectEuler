"""
PROBLEM

In the hexadecimal number system numbers are represented using 16 different digits:

0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F
The hexadecimal number AF when written in the decimal number system equals 10x16+15=175.

In the 3-digit hexadecimal numbers 10A, 1A0, A10, and A01 the digits 0,1 and A are all present.
Like numbers written in base ten we write hexadecimal numbers without leading zeroes.

How many hexadecimal numbers containing at most sixteen hexadecimal digits exist with all of the
digits 0,1, and A
present at least once?
Give your answer as a hexadecimal number.

(A,B,C,D,E and F in upper case, without any leading or trailing code that marks the number as hexadecimal and
without leading zeroes , e.g. 1A3F and not: 1a3f and not 0x1a3f and not $1A3F and not #1A3F and not 0000001A3F)

ANSWER: 3D58725572C62302  (int = 4420408745587516162)
Solve time: < 0.01 seconds
"""

from util.utils import timeit
import unittest

# get number of solutions with length k using inclusion-exclusion principle

# 1) all possible values with no leading 0:
#    15 * 16^(k-1)
# 2) Remove the ones that don't have any A or 1 (and no leading 0), or no 0
#    14 * 15^(k-1) + 14 * 15^(k-1) + 15^k
# 3) Account for any double counting ex. with no A and no 1
#    no 0 and A + no 0 and 1 + no A and 1
#    14^k + 14^k + 13 * 14^(k-1)
# 4) Account for and triple counting, no A, 1 or 0
#    13^k
# Putting it all together: 1) - 2) + 3) - 4)
# 15*16^(k-1) - 43*15^(k-1) + 41*14^(k-1) - 13^k


class Problem162:
    def __init__(self, max_digits):
        self.max_digits = max_digits

    @staticmethod
    def num_with_length_k(k: int):  # using inclusion-exclusion principle
        return 15*16**(k-1) - 43*15**(k-1) + 41*14**(k-1) - 13**k

    @timeit
    def solve(self):
        decimal_num = sum(self.num_with_length_k(k) for k in range(3, self.max_digits + 1))
        return hex(decimal_num)[2:].upper()


class Solution162(unittest.TestCase):
    def setUp(self):
        self.problem = Problem162(max_digits=16)

    def test_solution(self):
        self.assertEqual('3D58725572C62302', self.problem.solve())


if __name__ == '__main__':
    unittest.main()
