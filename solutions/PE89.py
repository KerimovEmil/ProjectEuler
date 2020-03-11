"""
PROBLEM

For a number written in Roman numerals to be considered valid there are basic rules which must be followed.
Even though the rules allow some numbers to be expressed in more than one way there is always a "best" way
 of writing a particular number.

For example, it would appear that there are at least six ways of writing the number sixteen:

IIIIIIIIIIIIIIII
VIIIIIIIIIII
VVIIIIII
XIIIIII
VVVI
XVI

However, according to the rules only XIIIIII and XVI are valid, and the last example is considered to be the most
efficient, as it uses the least number of numerals.

Find the number of characters saved by writing each of these in their minimal form.

Note: You can assume that all the Roman numerals in the file contain no more than four consecutive identical units.

ANSWER:

Solve time ~ 0.037 seconds
"""

import unittest

from util.utils import timeit


# Numerals must be arranged in descending order of size.
# M, C, and X cannot be equalled or exceeded by smaller denominations.
# D, L, and V can each only appear once.

# Only one I, X, and C can be used as the leading numeral in part of a subtractive pair.
# I can only be placed before V and X.
# X can only be placed before L and C.
# C can only be placed before D and M.

DC_VALUE = {
    'I': 1,
    'IV': 4,
    'V': 5,
    'IX': 9,
    'X': 10,
    'XL': 40,
    'L': 50,
    'XC': 90,
    'C': 100,
    'CD': 400,
    'D': 500,
    'CM': 900,
    'M': 1000
}
LS_ORDER = sorted(DC_VALUE.keys(), key=lambda x: DC_VALUE[x])[::-1]


class RomanNumeral:
    @staticmethod
    def parse(s):
        """
        Parse valid roman numeral string
        Args:
            s: <str>
        Returns: <int>
        """
        sub_s = s
        value = 0
        while len(sub_s) > 0:
            for roman in LS_ORDER:
                if sub_s.startswith(roman):
                    sub_s = sub_s.replace(roman, '', 1)
                    value += DC_VALUE[roman]
        return value

    @staticmethod
    def construct(num):
        roman = ''
        value = num
        while value:
            for char in LS_ORDER:
                if value >= DC_VALUE[char]:
                    value -= DC_VALUE[char]
                    roman += char
                    break
        return roman


class Problem89:
    def __init__(self, data_path):
        self.problem_data = self.load_data(data_path)

    @staticmethod
    def load_data(data_path):
        with open(data_path, 'r') as f:
            problem_data = list(x.strip() for x in f.readlines())
        return problem_data

    @timeit
    def solve(self):
        tot_diff = 0
        for i, s in enumerate(self.problem_data):
            value = RomanNumeral.parse(s)
            result = RomanNumeral.construct(value)
            diff = len(s) - len(result)
            assert diff >= 0, "diff should be >= 0"
            tot_diff += diff
        return tot_diff


class Solution89(unittest.TestCase):
    def setUp(self):
        self.problem = Problem89(r'..\problem_data\p089_roman.txt')

    def test_solution(self):
        self.assertEqual(743, self.problem.solve())

    def test_roman_parse(self):
        self.assertEqual(19, RomanNumeral.parse('XIX'))
        self.assertEqual(49, RomanNumeral.parse('XXXXIIIIIIIII'))
        self.assertEqual(49, RomanNumeral.parse('XXXXVIIII'))
        self.assertEqual(49, RomanNumeral.parse('XXXXIX'))
        self.assertEqual(49, RomanNumeral.parse('XLIIIIIIIII'))
        self.assertEqual(49, RomanNumeral.parse('XLVIIII'))
        self.assertEqual(49, RomanNumeral.parse('XLIX'))
        self.assertEqual(1606, RomanNumeral.parse('MDCVI'))

    def test_roman_construct(self):
        self.assertEqual(RomanNumeral.construct(19), 'XIX')
        self.assertEqual(RomanNumeral.construct(49), 'XLIX')
        self.assertEqual(RomanNumeral.construct(1606), 'MDCVI')


if __name__ == '__main__':
    unittest.main()
