"""
PROBLEM

Consider the divisors of 30: 1,2,3,5,6,10,15,30.
It can be seen that for every divisor d of 30, d+30/d is prime.

Find the sum of all positive integers n not exceeding 100,000,000
such that for every divisor d of n, d+n/d is prime.

ANSWER: 1739023853137
Solve time ~27 seconds
"""

# Since 1 is always a divisor of n, then
# 1 + n/1 = 1 + n = prime

# n must be even
# since if n is odd then every divisor d must be odd then
# d + n/30 = odd + odd = even != prime if the prime > 2. Which holds for n > 2.

# n is square free
# since if n = p_1 * p_2^2 then choose d = p_2
# p_2 + p_1*p_2 = p_2 * (1 + p_1) != prime.

# combining the last two findings we have, n%4 can only be 0 or 2 since n needs to be odd,
# however since n is squarefree, n%4 can only be equal to 2

# combining this with the fact that n + 1 must be a prime, it results in us only needing
# to loop over primes such that p%4 == 3


import unittest
from util.utils import timeit
from util.utils import primes_upto as primes


class Problem357:
    @timeit
    def __init__(self, max_int, debug=False):
        self.max_int = max_int
        self.ans = 1  # for the first number 1.
        self.debug = debug

        if self.debug:
            print("Calculating Primes")

        self.set_primes = set(primes(max_int))

        if self.debug:
            print("Finished Calculating Primes")
            print("{} is the total number of primes to check".format(len(self.set_primes)))  # under 6 million

    @timeit
    def solve(self):
        # n+1 = prime = 4k+3 (see explanation above)
        candidate_n = (p - 1 for p in self.set_primes if p % 4 == 3)

        for n in candidate_n:

            # quick initial check
            if not self.is_prime(n // 2 + 2):
                continue

            # full check
            if all(self.is_prime(i + n // i) for i in range(3, int(n**0.5)+1) if not n % i):
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
