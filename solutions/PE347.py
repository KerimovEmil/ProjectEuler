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
Solve time ~9 seconds
"""
from util.utils import timeit
import unittest
from math import log
from primesieve import primes


class Problem347:
    def __init__(self):
        pass

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
                # add all p*q*p^x*q^y <= L
                # p^x <= R
                # x logp <= logR
                # x <= logR / logp
                max_mult = 1
                for x in range(int(log(multiplier_limit) / log(p)) + 2):
                    for y in range(int(log(multiplier_limit) / log(q)) + 2):
                        possible_k = pow(p, x) * pow(q, y)
                        if possible_k > multiplier_limit:
                            break
                        max_mult = max(max_mult, possible_k)
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
