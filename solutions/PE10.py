"""
PROBLEM

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
Find the sum of all the primes below two million.

ANSWER: 142913828922
Solve time: ~ 0.02 seconds
"""
import unittest
from util.utils import timeit, primes_upto


class Problem10:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        return sum(primes_upto(self.n))

    @timeit
    def lucy_algo(self):  # see comment below
        r = int(self.n ** 0.5)
        V = [self.n // i for i in range(1, r + 1)]
        V += list(range(V[-1] - 1, 0, -1))
        S = {i: i * (i + 1) // 2 - 1 for i in V}
        for p in range(2, r + 1):
            if S[p] > S[p - 1]:  # p is prime
                sp = S[p - 1]  # sum of primes smaller than p
                p2 = p * p
                for v in V:
                    if v < p2:
                        break
                    S[v] -= p * (S[v // p] - sp)
        return S[self.n]


class Solution10(unittest.TestCase):
    def setUp(self):
        self.problem = Problem10(n=2000000)

    def test_solution(self):
        self.assertEqual(142913828922, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

# Lucy_Hedgehog from https://projecteuler.net/thread=10;page=5#111677
# Here is a solution that is more efficient than the sieve of Eratosthenes.
# It is derived from similar algorithms for counting primes.
# The advantage is that there is no need to find all the primes to find their sum.
#
# The main idea is as follows: Let S(v,m) be the sum of integers in the range 2..v that remain after sieving with all
# primes smaller or equal than m. That is S(v,m) is the sum of integers up to v that are either prime or the product
# of primes larger than m.
#
# S(v, p) is equal to S(v, p-1) if p is not prime or v is smaller than p*p. Otherwise (p prime, p*p<=v) S(v,p) can be
# computed from S(v,p-1) by finding the sum of integers that are removed while sieving with p. An integer is removed in
# this step if it is the product of p with another integer that has no divisor smaller than p. This can be expressed as
#
# S(v,p)=S(v,p−1)−p(S(v/p,p−1)−S(p−1,p−1)).
#
# Dynamic programming can be used to implement this. It is sufficient to compute S(v,p) for all positive integers v
# that are representable as floor(n/k) for some integer k and all p≤√v.
