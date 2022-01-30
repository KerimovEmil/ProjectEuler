"""
PROBLEM

It is possible to show that the square root of two can be expressed as an infinite continued fraction.

√ 2 = 1 + 1/(2 + 1/(2 + 1/(2 + ... ))) = 1.414213...

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth expansion, 1393/985,
is the first example where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than denominator?

ANSWER: 153
Solve time ~0.004 seconds
"""
import unittest
from util.utils import timeit


class Problem57:
    def __init__(self, digit, max_iter):
        self.max_iter = max_iter
        self.num = digit

    @timeit
    def solve(self):
        dividend = self.num
        divisor = 1

        count = 0
        for i in range(self.max_iter):
            (dividend, divisor) = (self.num * dividend + divisor, dividend)
            if len(str(dividend + divisor)) > len(str(dividend)):
                count += 1
        return count


class Solution57(unittest.TestCase):
    def setUp(self):
        self.problem = Problem57(digit=2, max_iter=1000)

    def test_solution(self):
        self.assertEqual(153, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
