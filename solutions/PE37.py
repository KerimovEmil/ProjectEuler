"""
PROBLEM

The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left
to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left:
3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.
NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

ANSWER:
748317
Solve time ~0.3 seconds
"""

import unittest
from util.utils import timeit, sieve


def trunc_left(num):
    return int(str(num)[:-1])


def trunc_right(num):
    return int(str(num)[1:])


class Problem37:
    def __init__(self, max_int):
        self.max_int = max_int
        self.ans = 0

    @timeit
    def solve(self):
        set_primes = set(sieve(self.max_int))
        for prime in set_primes:
            if prime in {2, 3, 5, 7}:  # problem statement
                continue

            trunc_l = prime
            trunc_r = prime

            is_truncatable = True
            for i in range(len(str(prime)) - 1):
                trunc_l = trunc_left(trunc_l)
                trunc_r = trunc_right(trunc_r)
                if trunc_l not in set_primes:
                    is_truncatable = False
                    break
                if trunc_r not in set_primes:
                    is_truncatable = False
                    break

            if is_truncatable:
                self.ans += prime

        return self.ans


class Solution37(unittest.TestCase):
    def setUp(self):
        self.problem = Problem37(max_int=800000)

    def test_solution(self):
        self.assertEqual(748317, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
