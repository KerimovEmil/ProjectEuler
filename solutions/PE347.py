"""
PROBLEM

The largest integer ≤ 100 that is only divisible by both the primes 2 and 3 is 96, as 96=32*3=25*3.
For two distinct primes p and q let M(p,q,N) be the largest positive integer ≤N only divisible by both
 p and q and M(p,q,N)=0 if such a positive integer does not exist.

E.g. M(2,3,100)=96.
M(3,5,100)=75 and not 90 because 90 is divisible by 2 ,3 and 5.
Also M(2,73,100)=0 because there does not exist a positive integer ≤ 100 that is divisible by both 2 and 73.

Let S(N) be the sum of all distinct M(p,q,N). S(100)=2262.

Find S(10 000 000).

ANSWER: 11109800204052
Solve time ~6.5 seconds
"""
from util.utils import timeit
import unittest
from math import log
from primesieve import primes


class Problem347:
    def __init__(self):
        pass

    @staticmethod
    def max_multiplier(p: int, q: int, limit: int):
        """
        For primes, p,q, find the maximum n = p^x*q^y such that n <= limit
        """
        max_mult = 1
        log_limit = log(limit)
        log_p = log(p)
        log_q = log(q)
        # x log(p) + y log(q) <= log(limit)
        for x in range(int(log_limit / log_p) + 2):
            y = int((log_limit - x*log_p) / log_q)
            possible_n = pow(p, x) * pow(q, y)
            if possible_n > limit:
                break
            max_mult = max(max_mult, possible_n)

        return max_mult

    @timeit
    def solve(self, limit):
        # get relevant list of primes
        ls_primes = primes(limit // 2)

        # store unique solutions into set
        sol_set = set()

        # loop over pairs of primes p,q
        for i in range(len(ls_primes)):
            p = ls_primes[i]
            for j in range(i + 1, len(ls_primes)):
                q = ls_primes[j]

                n = p * q
                if n > limit:
                    break

                multiplier_limit = limit // n

                max_mult = self.max_multiplier(p, q, multiplier_limit)
                sol_set.add(n * max_mult)
        return sum(sol_set)


class Solution347(unittest.TestCase):
    def setUp(self):
        self.problem = Problem347()

    def test_small_solution(self):
        self.assertEqual(2262, self.problem.solve(limit=100))

    def test_solution(self):
        self.assertEqual(11109800204052, self.problem.solve(limit=10000000))


if __name__ == '__main__':
    unittest.main()
