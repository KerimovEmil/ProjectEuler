"""
PROBLEM

You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days hath September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.

A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

ANSWER: 171
Solve time: ~0.002 seconds
"""

import unittest
from util.utils import timeit


class Problem19:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year

    @timeit
    def solve(self):
        def is_leap(year):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

        # 1 Jan 1900 was a Monday. Represent weekdays as 0 = Monday ... 6 = Sunday.
        # Count the day of the week of the 1st of each month.
        month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        sunday_count = 0
        # day-of-week of 1 Jan 1900
        dow = 0

        for year in range(1900, self.end_year + 1):
            for month in range(12):
                if year >= self.start_year and dow == 6:
                    sunday_count += 1
                days = month_lengths[month]
                if month == 1 and is_leap(year):
                    days += 1
                dow = (dow + days) % 7

        return sunday_count


class Solution19(unittest.TestCase):
    def setUp(self):
        self.problem = Problem19(1901, 2000)

    def test_solution(self):
        self.assertEqual(171, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
