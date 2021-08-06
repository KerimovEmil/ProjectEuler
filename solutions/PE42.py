"""
PROBLEM

The nth term of the sequence of triangle numbers is given by, tn = n(n+1)/2; so the first
ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55,

By converting each letter in a word to a number corresponding to its alphabetical position
and adding these values we form a word value. For example, the word value for
SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call
 the word a triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing
nearly two-thousand common English words, how many are triangle words?

ANSWER:
162
Solve time ~0.007 seconds
"""

import unittest
from util.utils import timeit


class Problem42:
    def __init__(self, words, max_triangle_sum):
        self.words = words
        self.max_triangle_sum = max_triangle_sum
        self.count = 0
        self.decoder = None

    def generate_set_of_triangle_numbers(self):
        return {i * (i + 1) / 2 for i in range(self.max_triangle_sum)}

    def generate_decoder(self):
        self.decoder = {let: i + 1 for (i, let) in enumerate(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))}

    def enum(self, word):
        return sum([self.decoder[letter] for letter in word])

    @timeit
    def solve(self):
        self.generate_decoder()
        triangle_nums = self.generate_set_of_triangle_numbers()
        for i in range(len(self.words)):
            word = self.words[i][1:-1]  # removing extra quotations
            if self.enum(word) in triangle_nums:
                self.count += 1
        return self.count


class Solution42(unittest.TestCase):
    def setUp(self):
        with open(r"..\problem_data\p042_words.txt", 'r+') as f:
            old_words = f.read().split(',')
        self.problem = Problem42(words=old_words, max_triangle_sum=100)

    def test_solution(self):
        self.assertEqual(162, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
