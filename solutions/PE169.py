"""
PROBLEM

Define f(0) = 1 and f(n) to be the number of different ways n can be expressed as a sum of integer powers of 2 using
each power no more than twice.

For example, f(10) = 5 since there are five different ways to express 10:
1+1+8
1+1+4+4
1+1+2+2+4
2+4+4
2+8

What is f(10^25)?

ANSWER: 178653872807
Solve time ~0.001 seconds
"""

# 10 = 8 + 2 = 2^3 + 2^1 = 1010 in binary
# 1010 = 0210 = 1002 = 0202 = 0122
# Therefore 5 ways to represent 10 using powers of 2 with no more than 2 of each power
# idea: 1000 -> 0200 -> 0120 -> 0111,  etc
# key idea is the (# zeros after 1) when in binary is what matters to count the number of options
# however we can't simply take the product of all the (# zeros after 1) + 1 since that undercounts the following case:
# 1010 can become 0210, 1002, 0202, but also 0122, so to count this extra case when we remove the leading one,
# this is as if we added some cases in which the number of consecutive zeros grows

# e.g. 18
# - 10010
# - 10002
# - 02010
# - 01210
# - 02002
# - 01202
# - 01122
from util.utils import timeit
import unittest


class Problem169:
    def __init__(self):
        pass

    @timeit
    def solve(self, n):
        """f_i = f_{i-1} + zeros[i] * sum_{k=1 to i-1} f_k"""
        n_binary_str = bin(n)[2:]
        ls_len_consecutive_zeros = [len(x) for x in n_binary_str.split('1')][1:]  # first one is always 0
        result, rolling_sum = 1, 1
        for len_consecutive_zeros in ls_len_consecutive_zeros:
            result += len_consecutive_zeros * rolling_sum
            rolling_sum += result
        return result


class Solution169(unittest.TestCase):
    def setUp(self):
        self.problem = Problem169()

    def test_sample_solution_1(self):
        self.assertEqual(5, self.problem.solve(n=10))

    def test_sample_solution_2(self):
        self.assertEqual(7, self.problem.solve(n=18))

    def test_sample_solution_3(self):
        self.assertEqual(13, self.problem.solve(n=42))

    def test_solution(self):
        self.assertEqual(178653872807, self.problem.solve(n=pow(10,25)))


if __name__ == '__main__':
    unittest.main()

