# PROBLEM

# The square root of 2 can be written as an infinite continued fraction.
#
# The infinite continued fraction can be written, √2 = [1;(2)], (2) indicates that 2 repeats ad infinitum.
# In a similar way, √23 = [4;(1,3,1,8)].
#
# It turns out that the sequence of partial values of continued fractions for square roots provide the best
# rational approximations. Let us consider the convergents for √2.
#
# Hence the sequence of the first ten convergents for √2 are:
#
# 1, 3 / 2, 7 / 5, 17 / 12, 41 / 29, 99 / 70, 239 / 169, 577 / 408, 1393 / 985, 3363 / 2378, ...
#
# What is most surprising is that the important mathematical constant,
# e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, ..., 1, 2k, 1, ...].
#
# The first ten terms in the sequence of convergents for e are:
#
# 2, 3, 8 / 3, 11 / 4, 19 / 7, 87 / 32, 106 / 39, 193 / 71, 1264 / 465, 1457 / 536, ...
# The sum of digits in the numerator of the 10th convergent is 1 + 4 + 5 + 7 = 17.
#
# Find the sum of digits in the numerator of the 100th convergent of the continued fraction for e.

# ANSWER:
# 272


import decimal
import math

decimal.getcontext().prec = 1000


class Problem65:
    def __init__(self, n, nth_convergent):
        self.n = n
        self.nth_convergent = nth_convergent
        self.numerator = None
        self.sum_of_digits_of_numerator = None

    def get_numerator(self):
        n = self.nth_convergent - 1
        old_p = 1
        p = decimal.Decimal(self.n).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        # p(n) = a(n) * p(n - 1) + p(n - 2)
        for i in range(n):
            older_p = old_p
            old_p = p
            if i % 3 == 0:
                a = 1
            elif i % 3 == 1:
                a = 2 * (int(i / 3) + 1)
            elif i % 3 == 2:
                a = 1
            p = a * old_p + older_p

        return p

    def solve(self):
        self.numerator = self.get_numerator()
        self.sum_of_digits_of_numerator = sum(int(x) for x in str(self.numerator))

        return self.sum_of_digits_of_numerator


if __name__ == "__main__":
    obj = Problem65(math.e, 100)
    sol = obj.solve()
    print(sol)
