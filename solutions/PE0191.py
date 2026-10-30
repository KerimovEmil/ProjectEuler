"""
PROBLEM

A particular school offers cash rewards to children with good attendance and punctuality. If they are absent
for three consecutive days or late on more than one occasion then they forfeit their prize.

During an n-day period a trinary string is formed for each child consisting of L's (late), O's (on time), and
A's (absent).

Although there are eighty-one trinary strings for a 4-day period that can be formed, exactly forty-three strings
would lead to a prize:
  OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
  OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
  AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
  AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
  LAOO LAOA LAAO

How many "prize" strings exist over a 30-day period?

ANSWER: 1918080160
Solve time: ~0.0001 seconds

---
MATHEMATICAL DERIVATION:

1. Reduction to L-Free Strings (Tribonacci Numbers):
   Consider first the number T(k) of valid strings of length k over the binary alphabet {'O', 'A'} that do not
   contain three consecutive 'A's ("AAA").
   Every such string of length k >= 3 begins with one of the three prefixes:
   - "O" followed by any valid string of length k - 1: T(k - 1) ways,
   - "AO" followed by any valid string of length k - 2: T(k - 2) ways,
   - "AAO" followed by any valid string of length k - 3: T(k - 3) ways.
   Therefore, T(k) satisfies the Tribonacci recurrence:
     T(k) = T(k - 1) + T(k - 2) + T(k - 3)   for k >= 3,
   with initial values T(0) = 1, T(1) = 2 ("O", "A"), and T(2) = 4 ("OO", "OA", "AO", "AA").

2. Accounting for At Most One 'L' via Convolution:
   A valid n-day prize string has at most one 'L' and no "AAA" substring. Note that an 'L' resets any run of
   consecutive 'A's, so a string containing a single 'L' at 0-based index i (0 <= i <= n - 1) is valid if and
   only if the prefix of length i (before 'L') and the suffix of length n - 1 - i (after 'L') are both valid
   {'O', 'A'}-strings with no "AAA".
   Summing over the two disjoint cases (zero 'L's or exactly one 'L'):
     P(n) = T(n) + sum_{i=0}^{n-1} T(i) * T(n - 1 - i).
"""

import unittest
from util.utils import timeit


class Problem191:
    def __init__(self, days: int = 30):
        self.days = days

    @staticmethod
    def count_prize_strings(n: int) -> int:
        if n == 0:
            return 1
        t = [1, 2, 4]
        while len(t) <= n:
            t.append(t[-1] + t[-2] + t[-3])
        return t[n] + sum(t[i] * t[n - 1 - i] for i in range(n))

    @timeit
    def solve(self) -> int:
        return self.count_prize_strings(self.days)


class Solution191(unittest.TestCase):
    def setUp(self):
        self.problem = Problem191()

    def test_sample(self):
        self.assertEqual(43, self.problem.count_prize_strings(4))

    def test_solution(self):
        self.assertEqual(1918080160, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
