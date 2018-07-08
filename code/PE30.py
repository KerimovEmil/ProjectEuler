# PROBLEM

# Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
# As 1 = 1^5 is not a sum it is not included.

# ANSWER:
# 443839


class Problem30:
    def __init__(self, power):
        self.power = power
        self.ans = 0

    def solve(self):
        i = 2
        while i < 355000:
            p = str(i)

            temp_sum = sum([int(digit) ** self.power for digit in p])
            if temp_sum == i:
                self.ans += i
            i = i + 1
        return self.ans


if __name__ == "__main__":
    obj = Problem30(5)
    sol = obj.solve()
    print(sol)
