"""
PROBLEM

The prime 41, can be written as the sum of six consecutive primes:
41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime
below one-hundred.

The longest sum of consecutive primes below one-thousand that
adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum
of the most consecutive primes?

ANSWER: 997651
Solve time: ~2.397 seconds
"""

import unittest
from util.utils import primes_upto
from util.utils import timeit


class Problem50:
    def __init__(self, max_int):
        self.max_int = max_int
        self.ls_primes = primes_upto(max_int)

    @timeit
    def solve(self):
        num_primes = len(self.ls_primes)
        primes = set(self.ls_primes)  # this speeds up the prime check

        ans = 2
        max_len = 1

        for i in range(num_primes):
            for j in range(i, num_primes - max_len):
                prime_sum = sum(self.ls_primes[i:j + 1 + max_len])

                if prime_sum >= self.max_int:
                    break

                if prime_sum in primes:
                    size = j + 1 - i
                    if size > max_len:
                        max_len = size
                        ans = prime_sum

        return ans


class Solution50(unittest.TestCase):
    def setUp(self):
        self.problem = Problem50(max_int=1000000)

    def test_solution(self):
        self.assertEqual(997651, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
