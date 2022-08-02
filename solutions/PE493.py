"""
PROBLEM
Given 7 different coloured balls, 10 of each, so 70 in totol. If we pick 20 balls at random, what is the expected
number of unique colours chosen. Given your answer to the 9th decimal place.

ANSWER: 6.818741802
Solve time < 1 ms
"""

from util.utils import timeit
import unittest


# For any given colour, the probability of it being present is 1 - (60 choose 20) / (70 choose 20).
# for all the colours it is just 7 * the probability of one colour being present
# 7 * (1- (60 choose 20) / (70 choose 20))
# = 7 * (1- 60! * 50! / 40 ! / 70!)
# = 7 * (1 - 50*49*48*47*46*45*44*43*42*41 / (70*69*68*67*66*65*64*63*62*61))
# = 763700091 / 112000148
# = 6.818741802019762


class Problem493:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        # 7 * (1- (60 choose 20) / (70 choose 20))
        probability = 7 * (1 - 50*49*48*47*46*45*44*43*42*41 / (70*69*68*67*66*65*64*63*62*61))
        return round(probability, 9)


class Solution493(unittest.TestCase):
    def setUp(self):
        self.problem = Problem493()

    def test_solution(self):
        self.assertEqual(6.818741802, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
