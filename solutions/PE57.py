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
Solve time ~0.2 seconds
"""
import unittest
import decimal

decimal.getcontext().prec = 2000


class Problem57:
    def __init__(self, digit, max_iter):
        self.max_iter = max_iter
        self.num = digit

    def solve(self):
        old_p = decimal.Decimal(1).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        old_q = decimal.Decimal(0).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        p = decimal.Decimal(self.num).sqrt().to_integral_exact(rounding=decimal.ROUND_FLOOR)
        q = decimal.Decimal(1).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        rem = decimal.Decimal(self.num).sqrt()
        a = rem.to_integral_exact(rounding=decimal.ROUND_FLOOR)

        count = 0

        for i in range(self.max_iter):
            older_p = old_p
            older_q = old_q
            old_p = p
            old_q = q
            old_rem = rem
            rem = 1 / (old_rem - a)
            a = rem.to_integral_exact(rounding=decimal.ROUND_FLOOR)
            p = a * old_p + older_p
            q = a * old_q + older_q
            if len(str(p)) > len(str(q)):
                count += 1
        return count


class Solution57(unittest.TestCase):
    def setUp(self):
        self.problem = Problem57(digit=2, max_iter=1000)

    def test_solution(self):
        self.assertEqual(153, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
