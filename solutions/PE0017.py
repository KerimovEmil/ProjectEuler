"""
PROBLEM

If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 =
19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115
(one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with
British usage.

ANSWER: 21124
Solve time: ~0.001 seconds
"""

import unittest
from util.utils import timeit

ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
        'seventeen', 'eighteen', 'nineteen']
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def number_to_words(n):
    """Convert an integer in [0, 1000] to its English words (no spaces/hyphens)."""
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + (ONES[n % 10] if n % 10 else '')
    if n < 1000:
        hundreds = ONES[n // 100] + 'hundred'
        rest = n % 100
        if rest:
            return hundreds + 'and' + number_to_words(rest)
        return hundreds
    return 'onethousand'


class Problem17:
    def __init__(self, max_n):
        self.max_n = max_n

    @timeit
    def solve(self):
        return sum(len(number_to_words(i)) for i in range(1, self.max_n + 1))


class Solution17(unittest.TestCase):
    def setUp(self):
        self.problem = Problem17(1000)

    def test_solution(self):
        self.assertEqual(21124, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
