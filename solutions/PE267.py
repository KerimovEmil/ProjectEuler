"""
You are given a unique investment opportunity.

Starting with £1 of capital, you can choose a fixed proportion, f, of your capital to bet on a fair coin toss
 repeatedly for 1000 tosses.
Your return is double your bet for heads and you lose your bet for tails.

For example, if f=1/4, for the first toss you bet £0.25, and if heads comes up you win £0.5 and so then have £1.5.
You then bet £0.375 and if the second toss is tails, you have £1.125.

Choosing f to maximize your chances of having at least £1,000,000,000 after 1,000 flips, what is the chance that you
become a billionaire?

All computations are assumed to be exact (no rounding), but give your answer rounded to 12 digits behind the decimal
 point in the form 0.abcdefghijkl.

ANSWER: 0.999992836187
Solve time: ~0.1 seconds
"""
from util.utils import timeit, combin
import unittest
from math import log as ln

# note that after n coin flips, the total value (regardless of order is):
# V = (1+2f)^h (1-f)^{n-h}

# for a given f and n, the amount of heads required to surpass a certain value x (10^9):
# (1+2f)^h (1-f)^{n-h} >= x
# h ln(1+2f) + (n-h) ln(1-f) >= ln(x)
# h ln((1+2f)/(1-f)) >= ln(x) - n ln(1-f)
# h >= (ln(x) - n ln(1-f)) / ln((1+2f)/(1-f))

# the goal now is to minimize the expression on the right in terms of f, we take the derivative and set it to 0
# y = (ln(x) - n ln(1-f)) / ln((1+2f)/(1-f))
# y' = [(n/(1-f))*ln((1+2f)/(1-f)) - (ln(x) - n ln(1-f)) * (2/(1+2f) + 1/(1-f))]/ (ln((1+2f)/(1-f)))^2 = 0
# n/(1-f) * ln((1+2f)/(1-f)) = (ln(x) - n ln(1-f)) * (2/(1+2f) + 1/(1-f))
# n * ln((1+2f)/(1-f)) = (ln(x) - n ln(1-f)) * (2(1-f)/(1+2f) + 1)
# n * (1+2f) * ln((1+2f)/(1-f)) = (ln(x) - n ln(1-f)) * (2(1-f) + (1+2f))
# n * (1+2f) * ln((1+2f)/(1-f)) = 3ln(x) - 3n ln(1-f)
# n * (1+2f) * ln(1+2f) - n * (1+2f) ln(1-f) = 3ln(x) - 3n ln(1-f)
# n * (1+2f) * ln(1+2f) + n * (3 - (1+2f)) ln(1-f) = 3ln(x)
# (1+2f) * ln(1+2f) + 2 * (1-f) * ln(1-f) = 3ln(x)/n

# solving numerically using ln(1+x) = x - x^2/2 + ..., ln(1-x) = -x - x^2/2 + ...
# (1+2f) * (2f - (2f)^2/2) + 2 * (1-f) (-f - f^2/2) = 3ln(x)/n
# (1+2f) * 2f * (1-f) - f * (1-f) (2 + f) = 3ln(x)/n
# f * (1-f) * (2+4f - (2 + f) = 3ln(x)/n
# f * (1-f) * 3f = 3ln(x)/n
# f^2 * (1-f) = ln(x)/n

# solving numerically using ln(1+x) = x
# (1+2f) * (2f) + 2 * (1-f) * (-f) = 3ln(x)/n
# 2f * ((1+2f) - (1-f)) = 3ln(x)/n
# 2f * (f) = ln(x)/n
# f = sqrt( ln(x)/(2n) )  (good initial guess)

# plug into original equation to get minimal heads (h) required

# the final probability once we solve for f is:
# sum_{h=min_h}^{n} (n choose h) / 2^n


class Problem267:
    def __init__(self, n, x, decimals):
        self.n = n
        self.ln_x = ln(x)
        self.decimals = decimals

    def eq_error(self, f):
        return abs((1+2*f)*ln(1+2*f) + 2*(1-f)*ln(1-f) - 3*self.ln_x/self.n)

    def find_optimal_f(self):
        f_temp = (self.ln_x/(2*self.n))**0.5
        step = 0.01
        min_error = self.eq_error(f_temp)
        while True:
            error = self.eq_error(f_temp)
            converge = error > min_error
            if converge:
                return f_temp - step
            f_temp += step
            min_error = min(error, min_error)

    def get_h(self, f):
        h = (self.ln_x - self.n * ln(1-f)) / ln((1 + 2*f) / (1 - f))
        return int(h) + 1

    def get_final_probability(self, min_h):
        total = 0
        for h in range(min_h, self.n + 1):
            total += combin(self.n, h)
        p = total / pow(2, self.n)
        return round(p, self.decimals)

    @timeit
    def solve(self):
        opt_f = self.find_optimal_f()
        min_h = self.get_h(opt_f)
        prob = self.get_final_probability(min_h)
        return prob


class Solution267(unittest.TestCase):
    def setUp(self):
        self.problem = Problem267(n=1000, x=int(1e9), decimals=12)

    def test_solution(self):
        self.assertEqual(0.999992836187, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
