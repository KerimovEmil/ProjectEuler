"""
The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28.
In fact, there are exactly four numbers below fifty that can be expressed in such a way:

28 = 2^2 + 2^3 + 2^4
33 = 3^2 + 2^3 + 2^4
49 = 5^2 + 2^3 + 2^4
47 = 2^2 + 3^3 + 2^4

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and prime fourth power?

ANSWER: 1097343
Solve time: ~1 seconds
"""

from util.utils import timeit
import unittest
from primesieve import primes


class Problem87:
    def __init__(self):
        pass

    @timeit
    def solve(self, n):
        p = list(primes(int(n ** 0.5)))

        s = set()
        for p1 in p:
            t1 = p1**2
            for p2 in p:
                t2 = t1 + p2**3
                if t2 > n:
                    break

                for p3 in p:
                    t3 = t2 + p3**4

                    if t3 > n:
                        break
                    s.add(t3)

        return len(s)


class Solution87(unittest.TestCase):
    def setUp(self):
        self.problem = Problem87()

    def test_sample_solution(self):
        self.assertEqual(4, self.problem.solve(n=50))

    def test_solution(self):
        self.assertEqual(1097343, self.problem.solve(n=50000000))


if __name__ == '__main__':
    unittest.main()

