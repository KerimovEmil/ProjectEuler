"""
PROBLEM

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number;
for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

As n increases, the proportion of bouncy numbers below n increases such that there are only 12951 numbers below
one-million that are not bouncy and only 277032 non-bouncy numbers below 10^10.

How many numbers below a googol (10^100) are not bouncy?

ANSWER: 51161058134250
Solve time ~0.001 seconds
"""

# constant numbers
# 1 digits - 9
# 2 digits - 9
# 3 digits - 9
# . digits - 9
# n digits - 9

# increasing numbers - A000581
# 1 digits - 9  = sum_{n=1}^{9} 1 = q
# 2 digits - 45 (9+8+7+6+5+4+3+2+1) = sum_{n=1}^{9} n = 1/2*q*(1 + q)
# 3 digits - 165 = sum_{n=1}^{9} (10-n)*n = 1/6*n*(1 + n)*(2 + q)
# 4 digits - 495 = sum_{n=1}^{9} 1/6*n*(1 + n)*(2 + n)
# ..
# n digits - binomial coefficient C(8+n,8)

# decreasing numbers - A035927
# 1 digits - 9  = sum_{n=1}^{9} 1 = q
# 2 digits - 54 = sum_{n=2}^{10} n
# 3 digits - 219
# 4 digits - 714
# 5 digits - 2001
# ..
# n digits - binomial coefficient C(10+n-1, n) - 1

# Therefore, number of non-bouncy numbers with n-digits is:
# increasing + # decreasing - # constant
# for n-digits
# = C(8+n,8) + C(10+n-1, n) - 1 - 9
# = C(8+n,8) + C(9+n, n) - 10
# = (n+8)!/[8! * n!] + (n+9)!/[9! * n!] - 10
# = (n+8)*(n+7)*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)/[8!]
# + (n+9)*(n+8)*(n+7)*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)/[9!] - 10
# = (n+8)*(n+7)*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)(1/[8!] + (n+9)/[9!]) - 10
# = (2 + n/9)*(n+8)*(n+7)*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)/[8!] - 10
# = (2 + n/9)*(n+8)*(n+7)*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1)/40320 - 10
# = (18 + n)*(n+8)*(n+7)*(n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1) // 362880 - 10


from util.utils import timeit
import unittest


class Problem113:
    def __init__(self):
        pass

    @timeit
    def solve(self, num_digit):
        return sum(self.n_digit_non_bouncy(n) for n in range(1, num_digit + 1))

    @staticmethod
    def n_digit_non_bouncy(n: int)-> int:
        value = (18 + n) * (n + 8) * (n + 7) * (n + 6) * (n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1) // 362880 - 10
        return int(value)

class Solution113(unittest.TestCase):
    def setUp(self):
        self.problem = Problem113()

    def test_solution(self):
        self.assertEqual(51161058134250, self.problem.solve(num_digit=100))


if __name__ == '__main__':
    unittest.main()
