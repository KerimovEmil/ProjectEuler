# find pent nums s.t. sum and diff is pent and diff is minimized

# Answer= 5482660

# p(n) = n(3n−1)/2

# testing if a number is a penta number:
# n = (3x^2 - x)/2
# 3/2 x^2 - 1/2 x - n = 0
# x^2 - 1/3 x - 2/3 n = 0
# x = (1/3 +/- (1/3)*sqrt(1 + 24*n))/2
# x = 1/6 *(1 + sqrt(1 + 24*n))

# if p(n) + p(m) = p(k), m > n
# n(3n−1)/2 + m(3m−1)/2 = (3n^2-n + 3m^2-m)/2 = k(3k−1)/2
# 3n^2 + 3m^2 - m - n = 3k^2 - k
# if p(m) - p(m) = p(q)
# m(3m−1)/2 - n(3n−1)/2 = (3m^2-m - 3n^2-n)/2 = q(3q−1)/2
# 3m^2 - 3n^2 + n - m = 3q^2 - q

from util.utils import timeit


class Problem44:
    def __init__(self, max_pentagonal_sum, max_pentagonal_number):
        self.max_pentagonal_sum = max_pentagonal_sum
        self.max_pentagonal_number = max_pentagonal_number
        self.ans = 100000000

    @timeit
    def generate_ls_pentagonal_numbers(self):
        return [int(i * (3 * i - 1) / 2) for i in range(1, self.max_pentagonal_sum)]

    @staticmethod
    def is_pent(num):
        return ((1 + (24 * num + 1) ** 0.5) / 6).is_integer()

    @timeit
    def solve(self):
        ls_pentagonal_numbers = self.generate_ls_pentagonal_numbers()
        for m in range(1, self.max_pentagonal_number):
            for n in range(m + 1, self.max_pentagonal_number):
                pent_sum = ls_pentagonal_numbers[m] + ls_pentagonal_numbers[n]
                if Problem44.is_pent(pent_sum):
                    pent_diff = ls_pentagonal_numbers[n] - ls_pentagonal_numbers[m]
                    if Problem44.is_pent(pent_diff):
                        print(m, n, ls_pentagonal_numbers[m], ls_pentagonal_numbers[n], pent_diff)
                        self.ans = min(pent_diff, self.ans)
        return self.ans

    @timeit
    def solve_alternative(self):
        ls_pentagonal_numbers = set(self.generate_ls_pentagonal_numbers())
        for p_m in ls_pentagonal_numbers:
            for p_n in ls_pentagonal_numbers:
                pent_sum = p_m + p_n
                if Problem44.is_pent(pent_sum):
                    if p_n > p_m:
                        pent_diff = p_n - p_m
                        if Problem44.is_pent(pent_diff):
                            print(p_m, p_n, pent_diff)
                            self.ans = min(pent_diff, self.ans)
        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    obj = Problem44(max_pentagonal_sum=10000, max_pentagonal_number=3000)
    sol = obj.solve()
    print(sol)
