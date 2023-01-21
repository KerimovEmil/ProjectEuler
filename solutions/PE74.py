"""
PROBLEM

The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:
1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169;
it turns out that there are only three such loops that exist:

169 → 363601 → 1454 → 169
871 → 45361 → 871
872 → 45362 → 872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,

69 → 363600 → 1454 → 169 → 363601 (→ 1454)
78 → 45360 → 871 → 45361 (→ 871)
540 → 145 (→ 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain with a starting
number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?

ANSWER: 402
Solve time: ~4.4 seconds
"""
from util.utils import timeit
import unittest


factorials_0_to_9 = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]


class Problem74:
    def __init__(self):
        self.dc = dict()

    @staticmethod
    def next_term(n: int) -> int:
        return sum(factorials_0_to_9[int(i)] for i in str(n))

    def num_of_non_repeating_terms(self, n: int) -> int:
        count = 0
        seen = set()

        while n not in seen:
            seen.add(n)
            count += 1
            n = self.next_term(n)

            if n in self.dc.keys():
                return count + self.dc[n]

        return count

    @timeit
    def solve(self, target=60, max_n=1_000_000):
        ans = 0

        for i in range(1, max_n+1):
            non_repeat = self.num_of_non_repeating_terms(i)
            self.dc[i] = non_repeat

            if non_repeat == target:
                ans += 1
        return ans


class Solution74(unittest.TestCase):
    def setUp(self):
        self.problem = Problem74()

    def test_solution(self):
        self.assertEqual(402, self.problem.solve(target=60, max_n=1_000_000))


if __name__ == '__main__':
    unittest.main()
