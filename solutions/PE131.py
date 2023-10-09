"""
PROBLEM

There are some prime values, p, for which there exists a positive integer, n, such that the expression
 n^3 + n^2×p is a perfect cube.

For example, when p = 19, 8^3 + 8^2×19 = 123.

What is perhaps most surprising is that for each prime with this property the value of n is unique,
and there are only four such primes below one-hundred.

How many primes below one million have this remarkable property?

ANSWER: 173
Solve time: ~1 second
"""
from util.utils import timeit
import unittest
from primesieve import primes

# n^2 * (n+p) = m^3  -> therefore n+p must be a perfect cube and n must be a perfect cube
# therefore p = perfect cube (m^3) - n (perfect cube)
# since m^3 - n^3 = (m-n)*(m^2 + mn + n^2), since p is a prime therefore m-n = 1

# n^3 + n^2×p = m^3
# n = q^3 and m = q^2 + q^3 for q integer


class Problem131:
    def __init__(self, max_p=1_000_000):
        self.max_p = max_p

    @timeit
    def solve(self):
        ls_primes = primes(self.max_p)
        count = 0
        p, q = 1, 0
        while p <= self.max_p:
            q += 1
            p = 1 + 3 * q + 3 * q * q
            if p in ls_primes:
                count += 1

        return count


class Solution131(unittest.TestCase):
    def setUp(self):
        self.problem = Problem131()

    def test_solution(self):
        self.assertEqual(173, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

