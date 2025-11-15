"""
PROBLEM

If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome.
A number that never forms a palindrome through the reverse and add process is called a Lychrel number.
Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that
 a number is Lychrel until proven otherwise. In addition you are given that for every number below
ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one,
with all the computing power that exists, has managed so far to map it to a palindrome.
In fact, 10677 is the first number to be shown to require over fifty iterations before producing a
palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

How many Lychrel numbers are there below ten-thousand?

ANSWER: 249
Solve time: ~0.051 seconds
"""
import unittest
from util.utils import timeit, is_palindrome


def add_reverse(n):
    reverse = int(''.join(list(str(n))[::-1]))
    return n + reverse


def is_lychrel(n, max_iter):
    number_to_test = add_reverse(n)
    for i in range(max_iter):
        if is_palindrome(number_to_test):
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

    @timeit
    def solve(self):
        count = 0
        for i in range(1, self.max_value):
            if is_lychrel(i, self.max_iter):
                count += 1
        return count


class Solution55(unittest.TestCase):
    def setUp(self):
        self.problem = Problem55(max_iter=50, max_value=10000)

    def test_solution(self):
        self.assertEqual(249, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
