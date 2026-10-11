"""
PROBLEM

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number;
for example, 134468.
Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand
(525) are bouncy. In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time we reach 21780 the proportion of bouncy
numbers is equal to 90%.

Find the least number for which the proportion of bouncy numbers is exactly 99%.

ANSWER: 1587000
Solve time: ~0.65 seconds
"""

from util.utils import timeit
import unittest


def is_increasing(a):
    return all(j >= i for i, j in zip(a[:-1], a[1:]))


def is_decreasing(a):
    return all(j <= i for i, j in zip(a[:-1], a[1:]))


def is_bouncy(n: int) -> bool:
    last = n % 10
    n //= 10
    inc = False
    dec = False
    while n:
        cur = n % 10
        if cur < last:
            inc = True
        elif cur > last:
            dec = True
        if inc and dec:
            return True
        last = cur
        n //= 10
    return False


class Problem112:
    def __init__(self):
        pass

    @timeit
    def solve(self, limit):
        N = 10000000
        count = 0
        for n in range(1, N + 1):
            if is_bouncy(n):
                count += 1
            if count / n >= limit:
                return n

        return None


class Solution112(unittest.TestCase):
    def setUp(self):
        self.problem = Problem112()

    def test_small_solution(self):
        self.assertEqual(21780, self.problem.solve(limit=0.9))

    def test_solution(self):
        self.assertEqual(1587000, self.problem.solve(limit=0.99))


if __name__ == '__main__':
    unittest.main()
