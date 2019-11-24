# PROBLEM

# If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

# Not all numbers produce palindromes so quickly. For example,

# 349 + 943 = 1292,
# 1292 + 2921 = 4213
# 4213 + 3124 = 7337
#
# That is, 349 took three iterations to arrive at a palindrome.
#
# Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome.
# A number that never forms a palindrome through the reverse and add process is called a Lychrel number.
# Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that
#  a number is Lychrel until proven otherwise. In addition you are given that for every number below
# ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one,
# with all the computing power that exists, has managed so far to map it to a palindrome.
# In fact, 10677 is the first number to be shown to require over fifty iterations before producing a
# palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).
#
# Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.
#
# How many Lychrel numbers are there below ten-thousand?

# ANSWER
# 249


def is_palin(n):  # todo: add this to utils?
    ls = list(str(n))
    return ls == ls[::-1]


def add_reverse(n):  # todo: add this to utils?
    reverse = int("".join(list(str(n))[::-1]))
    return n + reverse


def is_lychrel(n, max_iter):  # todo: add this to utils?
    number_to_test = add_reverse(n)
    for i in range(max_iter):
        if is_palin(number_to_test):
            return False
        else:
            number_to_test = add_reverse(number_to_test)

    return True


class Problem55:
    """
    How many Lychrel numbers are there below ten-thousand?
    """

    def __init__(self, max_iter, max_value):
        self.max_iter = max_iter
        self.max_value = max_value
        self.count = 0

    def solve(self):
        for i in range(1, self.max_value):
            if is_lychrel(i, self.max_iter):
                self.count += 1
        return self.count


if __name__ == "__main__":
    a = Problem55(50, 10000)
    sol = a.solve()
    print(sol)
