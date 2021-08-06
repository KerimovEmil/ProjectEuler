# PROBLEM

# The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

# Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

# ANSWER
# 9110846700
from util.utils import timeit


class Problem48:
    @timeit
    def __init__(self, n, last_n_digits):
        self.n = n
        self.mod_div = int(10 ** last_n_digits)
        self.ans = 0

    @timeit
    def solve(self):
        for i in range(1, self.n + 1):
            temp = (i % self.mod_div) ** i
            temp = temp % self.mod_div
            self.ans += temp
            self.ans = self.ans % self.mod_div
        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    last_n_digits = 10
    n = 1000
    obj = Problem48(n=n, last_n_digits=last_n_digits)
    sol = obj.solve()
    print(sol)
