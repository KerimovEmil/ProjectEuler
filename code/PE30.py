"""
PROBLEM

Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

1634 = 1^4 + 6^4 + 3^4 + 4^4
8208 = 8^4 + 2^4 + 0^4 + 8^4
9474 = 9^4 + 4^4 + 7^4 + 4^4
As 1 = 1^4 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.

ANSWER:
443839
Solve time ~ 0.72 seconds
"""


# 9^5 = 59049.
# So the maximum sum would be 9*59049 = 531441,

# solve: n*9^5 == 10^n

# 6 digits: 6 * 9**5 = 354294 (6 digits)
# 7 digits: 7 * 9**5 = 413343 (6 digits)

# n*9^5 == 10^n
# log(n) + power*log(9) = n log(10)

from util.utils import timeit
import unittest


class Problem30:
    def __init__(self, power, max_num):
        self.power = power
        self.max_num = max_num
        self.ans = 0
        self.digit_powers = {str(i): i**self.power for i in range(10)}

    @timeit
    def solve(self):
        # in one line
        self.ans = sum(n for n in range(10, self.max_num) if n == sum(self.digit_powers[d] for d in str(n)))
        return self.ans

    @timeit
    def solve_readable(self):
        for i in range(10, self.max_num):  # excluding 1
            if sum([self.digit_powers[digit] for digit in str(i)]) == i:
                self.ans += i
        return self.ans


class Solution30(unittest.TestCase):
    def setUp(self):
        self.problem = Problem30(power=5, max_num=int(6 * 9**5))

    def test_solution(self):
        self.assertEqual(443839, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
