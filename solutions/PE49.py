"""
PROBLEM

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways:
(i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property,
but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?

ANSWER: 2969, 6299, 9629: 296962999629
Solve time: ~0.2 seconds
"""

import unittest
from util.utils import timeit, primes_upto


class Problem49:
    def __init__(self, exclude, n):
        self.exclude = exclude
        self.n = n
        self.ans = None

    @timeit
    def solve(self):
        max_prime = int(10 ** self.n)
        min_prime = int(10 ** (self.n - 1))

        ls_all_primes = primes_upto(max_prime)  # get all primes between 1,000 and 10,000
        ls_primes = ls_all_primes[ls_all_primes >= min_prime]
        set_primes = set(ls_primes)

        for x in ls_primes:
            if x in self.exclude:
                continue  # skip this x
            for i in range(2, int(max_prime / 2)):
                if ((x + i) in set_primes) and ((x + 2 * i) in set_primes):
                    if set(str(x)) == set(str(x + i)):
                        if set(str(x)) == set(str(x + 2 * i)):
                            return int(str(x)+str(x+i)+str(x+2*i))

        return None

class Solution49(unittest.TestCase):
    def setUp(self):
        self.problem = Problem49(exclude={1487, 4817, 8147}, n=4)

    def test_solution(self):
        self.assertEqual(296962999629, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
