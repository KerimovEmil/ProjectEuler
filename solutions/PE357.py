"""
PROBLEM

Consider the divisors of 30: 1,2,3,5,6,10,15,30.
It can be seen that for every divisor d of 30, d+30/d is prime.

Find the sum of all positive integers n not exceeding 100,000,000
such that for every divisor d of n, d+n/d is prime.

ANSWER: 1739023853137
Solve time ~ 73 seconds
"""

# Since 1 is always a divisor of n, then
# 1 + n/1 = 1 + n = prime

# n must be even
# since if n is odd then every divisor d must be odd then
# d + n/30 = odd + odd = even != prime if the prime > 2. Which holds for n > 2.

# n is square free
# since if n = p_1 * p_2^2 then choose d = p_2
# p_2 + p_1*p_2 = p_2 * (1 + p_1) != prime.

# combining these findings we have, n%4 can only be 0 or 2 since n needs to be odd, however since n is squarefree
# n%4 can only be equal to 2

import unittest
from util.utils import primes_of_n, timeit, divisors
from primesieve import primes


class Problem357:
    @timeit
    def __init__(self, max_int, debug=False):
        self.max_int = max_int
        self.ans = 1  # for the first number 1.
        self.debug = debug

        if self.debug:
            print("Calculating Primes")
        self.ls_primes = primes(max_int)
        self.set_primes = set(self.ls_primes)
        if self.debug:
            print("Calculating square free sieve")
        if self.debug:
            print("Finished Calculating Primes")
            print("{} is the total number of primes to check".format(len(self.set_primes)))

    @timeit
    def solve(self):
        # for p in self.set_primes:
        for p in self.ls_primes:  # faster to loop over a list than a set
            n = p - 1
            # simple filter 1
            if n % 4 != 2:  # n is even and square-free
                continue
            if n % 9 == 0:  # square free
                continue
            # simple filter 2
            if not self.is_prime(n // 2 + 2):
                continue
            # Simple filter 3
            if not all([self.is_prime(i + n // i) for i in range(3, 8) if n % i == 0]):
                continue

            # Full filter
            prime_factors = primes_of_n(n)
            if any([t[1] > 1 for t in prime_factors.items()]):  # square-free
                continue
            all_divisors = divisors(prime_factors)
            all_primes = True
            for d in all_divisors:
                if not self.is_prime(d + n / d):
                    all_primes = False
                    break
            if all_primes:
                if self.debug:
                    print("{0} is a cool number".format(n))
                self.ans += n

        return self.ans

    def is_prime(self, n):
        return n in self.set_primes


class Solution357(unittest.TestCase):
    def setUp(self):
        self.problem = Problem357(max_int=int(1e8), debug=False)

    def test_solution(self):
        self.assertEqual(1739023853137, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
