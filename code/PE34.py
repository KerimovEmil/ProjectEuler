# PROBLEM

# Find the sum of all numbers which are equal to the sum of the factorial of their digits.

# ANSWER:
# 40730

from util.utils import basic_factorial


class Problem34:
    def __init__(self, max_x):
        self.max_x = max_x
        self.sum = 0

    @staticmethod
    def sum_of_factorial_of_digits(number):
        """Sum of the factorial of digits"""
        return sum([basic_factorial(int(i)) for i in str(number)])

    def solve(self):
        for i in range(3, self.max_x):
            if Problem34.sum_of_factorial_of_digits(i) == i:
                self.sum += i
        return self.sum


if __name__ == "__main__":
    obj = Problem34(max_x=200000)
    sol = obj.solve()
    print(sol)
    # since 9! = 362880
    # 9999999 is an easy upper limit to come up with. 7 times 9! is less than 9999999.
    # todo: add math proof why 200,000 is the maximum.
    # https://en.wikipedia.org/wiki/Factorion
    # only four such numbers exist: 1,2, 145, 40585.
    # since 1 and 2 are not sums as the question stated then the answer is 145+40585 = 40730
