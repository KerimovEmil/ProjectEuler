# PROBLEM

# Consider quadratic Diophantine equations of the form:
#
# x^2 – Dy^2 = 1
#
# For example, when D=13, the minimal solution in x is 649^2 – 13×180^2 = 1.
#
# It can be assumed that there are no solutions in positive integers when D is square.
#
# By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:
#
# 3^2 – 2×2^2 = 1
# 2^2 – 3×1^2 = 1
# 9^2 – 5×4^2 = 1
# 5^2 – 6×2^2 = 1
# 8^2 – 7×3^2 = 1
#
# Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.
#
# Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.

# ANSWER:
# 661

import decimal

decimal.getcontext().prec = 100


class Problem66:
    def __init__(self, max_d):
        self.max_d = max_d
        self.max_min_x = 0
        self.d_max_min_x = None

    @staticmethod
    def get_min_x_given_d(d):  # TODO: consider moving this to a util
        old_p = decimal.Decimal(1).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        old_q = decimal.Decimal(0).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        p = decimal.Decimal(d).sqrt().to_integral_exact(rounding=decimal.ROUND_FLOOR)
        q = 1
        rem = decimal.Decimal(d).sqrt()
        a = rem.to_integral_exact(rounding=decimal.ROUND_FLOOR)

        while (p ** 2 - d * q ** 2 > 1) or (p ** 2 - d * q ** 2 < 1):
            older_p = old_p
            older_q = old_q
            old_p = p
            old_q = q
            old_rem = rem
            rem = 1 / (old_rem - a)
            a = rem.to_integral_exact(rounding=decimal.ROUND_FLOOR)
            p = a * old_p + older_p
            q = a * old_q + older_q

        return (p, q)

    def solve(self):
        non_sqr_ls = [x for x in range(1, self.max_d+1) if int(x ** 0.5) != x ** 0.5]

        for i in non_sqr_ls:
            min_x = Problem66.get_min_x_given_d(i)[1]

            if min_x > self.max_min_x:
                self.max_min_x = min_x
                self.d_max_min_x = i
        return self.d_max_min_x


if __name__ == "__main__":
    obj = Problem66(1000)
    sol = obj.solve()
    print(sol)
