"""
PROBLEM

The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719,
are themselves prime.
There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
How many circular primes are there below one million?

ANSWER: 55
Solve time: ~0.4 seconds
"""

import unittest
from util.utils import timeit, primes_upto


class Problem35:
    """How many circular primes are there below one million?"""

    def __init__(self, n):
        self.count = 0
        self.set_primes = set(primes_upto(n))

    def is_circular_prime(self, prime):
        """Given a prime, rotate the digits of the prime to see if the numbers are still prime"""
        dig = list(str(prime))

        dig.append(dig.pop(0))  # rotate
        test_prime = int(''.join(dig))

        for _ in range(len(dig) - 1):
            if test_prime not in self.set_primes:
                return False
            else:
                dig.append(dig.pop(0))  # rotate
                test_prime = int(''.join(dig))
        return True

    @timeit
    def solve(self):
        return sum(self.is_circular_prime(i) for i in self.set_primes)


class Solution35(unittest.TestCase):
    def setUp(self):
        self.problem = Problem35(n=1000000)

    def test_solution(self):
        self.assertEqual(55, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
