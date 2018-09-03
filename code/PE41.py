# We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n
# exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

# What is the largest n-digit pandigital prime that exists?

# Answer: 7652413

import itertools
from util.utils import timeit


class Problem41:
    def __init__(self, n):
        self.n = n
        self.ans = 0

    @staticmethod
    def is_prime(n):  # todo reconcile with other is_prime functions
        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0: return False
        if n < 9: return True
        if n % 3 == 0: return False
        r = int(n ** 0.5)
        f = 5
        while f <= r:
            if n % f == 0: return False
            if n % (f + 2) == 0: return False
            f += 6
        return True

    @timeit
    def solve(self):
        ls_nums = itertools.permutations(range(1, self.n + 1))
        for i in ls_nums:
            num = int(''.join(map(str, list(i))))
            if Problem41.is_prime(num):
                if num > self.ans:
                    self.ans = num
        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    # 0: for 9 digits
    # 0 : for 8 digits
    # 7652413 : for 7 digits

    obj = Problem41(n=7)
    sol = obj.solve()
    print(sol)
