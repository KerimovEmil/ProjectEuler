r"""
PROBLEM

By replacing each of the letters in the word CARE with $1$, $2$, $9$, and $6$ respectively,
we form a square number: $1296 = 36^2$. What is remarkable is that, by using the same digital substitutions,
the anagram, RACE, also forms a square number: $9216 = 96^2$. We shall call CARE (and RACE) a square anagram
word pair and specify further that leading zeroes are not permitted, neither may a different letter have the same
digital value as another letter.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand
common English words, find all the square anagram word pairs (a palindromic word is NOT considered to be an anagram of itself).

What is the largest square number formed by any member of such a pair?

NOTE: All anagrams formed must be contained in the given text file.

ANSWER: 18769
Solve time: ~0.03 seconds
"""

import os
import unittest
from collections import defaultdict
from math import isqrt

from util.utils import timeit


class Problem98:
    def __init__(self, words=None):
        if words is None:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p098_words.txt')
            with open(file_path, 'r') as f:
                self.words = [w.strip(' \t\n\r"') for w in f.read().split(',')]
        else:
            self.words = words

    @timeit
    def solve(self):  # noqa: C901
        # Group words by their anagram signature
        anagrams = defaultdict(list)
        for w in self.words:
            sig = ''.join(sorted(w))
            anagrams[sig].append(w)

        # Collect distinct anagram pairs
        pairs = []
        for sig, w_list in anagrams.items():
            if len(w_list) >= 2:
                for i in range(len(w_list)):
                    for j in range(i + 1, len(w_list)):
                        pairs.append((w_list[i], w_list[j]))

        if not pairs:
            return 0

        max_len = max(len(w1) for w1, _ in pairs)

        # Precompute square numbers grouped by digit length
        squares_by_len = defaultdict(list)
        for root in range(1, int((10 ** max_len) ** 0.5) + 1):
            sq = root * root
            s_sq = str(sq)
            squares_by_len[len(s_sq)].append(s_sq)

        max_square = 0

        for w1, w2 in pairs:
            L = len(w1)
            for s1 in squares_by_len[L]:
                # Test bijection between letters of w1 and digits of s1
                w_to_d = {}
                d_to_w = {}
                valid = True
                for char, digit in zip(w1, s1):
                    if char in w_to_d and w_to_d[char] != digit:
                        valid = False
                        break
                    if digit in d_to_w and d_to_w[digit] != char:
                        valid = False
                        break
                    w_to_d[char] = digit
                    d_to_w[digit] = char

                if not valid:
                    continue

                # Form the corresponding number for w2
                s2 = ''.join(w_to_d[c] for c in w2)
                if s2[0] == '0':
                    continue

                val2 = int(s2)
                r2 = isqrt(val2)
                if r2 * r2 == val2:
                    val1 = int(s1)
                    max_square = max(max_square, val1, val2)

        return max_square


class Solution98(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p098_words.txt')
        with open(file_path, 'r') as f:
            words = [w.strip(' \t\n\r"') for w in f.read().split(',')]
        self.problem = Problem98(words=words)

    def test_solution(self):
        self.assertEqual(18769, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
