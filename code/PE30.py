# PROBLEM

# Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
# As 1 = 1^5 is not a sum it is not included.

# ANSWER:
# 443839
# Solve time ~ 0.65 seconds

# 9^5 = 59049.
# So the maximum sum would be 9*59049 = 531441,

# solve: n*9^5 == 10^n

# 6 digits: 6 * 9**5 = 354294 (6 digits)
# 7 digits: 7 * 9**5 = 413343 (6 digits)

# n*9^5 == 10^n
# log(n) + power*log(9) = n log(10)

from util.utils import timeit


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


if __name__ == "__main__":
    obj = Problem30(power=5, max_num=int(6 * 9**5))
    sol = obj.solve()
    print(sol)
