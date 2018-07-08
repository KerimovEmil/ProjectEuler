# PROBLEM

# The 5-digit number, 16807=7^5, is also a fifth power.
#  Similarly, the 9-digit number, 134217728=8^9, is a ninth power.

# How many n-digit positive integers exist which are also an nth power?

# ANSWER:
# 49

# MATH PART
# n-digit-number = x^n
# log(n-digit-number) = log(x^n)
# n-1 <= log(n digit number) < n    Using log based 10
# n-1 <= n log(x) < n
# (n-1)/n <= log(x) < 1
# log(x) < 1 implied x < 10
# max n such that (n-1)/n <= log(9)
# 1 - 1/n <= log(9)
# 1 - log(9) <= 1/n
# n <= 1/(1-log(9))
# n <= 21.9
# n < 22

# therefore to satisfy: n-digit-number = x^n
# only need to check 1<=x<=9 and n < 22 for n digit number = x^n

import math


class Problem63:
    def __init__(self):
        self.count = 0

    def solve(self):
        for x in range(1, 10):
            for n in range(1, 22):
                if (n - 1) / n <= math.log(x, 10):
                    self.count += 1
        return self.count


if __name__ == "__main__":
    obj = Problem63()
    sol = obj.solve()
    print(sol)
