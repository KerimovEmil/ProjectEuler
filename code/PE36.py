# PROBLEM

# The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

# Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

# (Please note that the palindromic number, in either base, may not include leading zeros.)

# ANSWER
# 872187


def is_palindromic(num):  # TODO: consider moving to utils?
    r = str(num)
    if len(r) == 1:
        return True
    first = r[:int(len(r) / 2)]
    second = r[-len(first):]
    return first == second[::-1]


class Problem36:
    def __init__(self, max_value):
        self.max_value = max_value
        self.sum = 0

    def solve(self):
        for i in range(self.max_value):
            if is_palindromic(i):
                if is_palindromic(bin(i)[2:]):
                    self.sum += i

        return self.sum


if __name__ == "__main__":
    a = Problem36(int(1e6))
    sol = a.solve()
    print(sol)
