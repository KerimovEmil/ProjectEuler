"""
PROBLEM

The first ten continued fraction representations of (irrational) square roots are:
sqrt(2) = [1;(2)], period=1
sqrt(3) = [1;(1,2)], period=2
sqrt(5) = [1;(4)], period=1
sqrt(6) = [1;(2,4)], period=2
sqrt(7) = [2;(1,1,1,4)], period=4
sqrt(8) = [2;(1,4)], period=2
sqrt(10) = [3;(6)], period=1
sqrt(11) = [3;(3,6)], period=2
sqrt(12) = [3;(2,6)], period=2
sqrt(13) = [3;(1,1,1,1,6)], period=5

Exactly four continued fractions, for N<=13, have an odd period.

How many continued fractions for N<=10,000 have an odd period?

ANSWER: 1322
Solve time: ~0.1 seconds

Textbook reference: Algebraic Number Theory by Frazer Jarvis, Section 8.2 Continued Fractions of Square Roots

Theorem 8.12 The continued fraction of ≥d has the form [b0; b1,..., bk ] where bk = 2b0.

Theorem 8.15 Let d > 0 be an integer, not a square. Then the equation x2−dy2 = 1 has infinitely many solutions.
The equation x2 − dy2 = −1 has infinitely many solutions if the continued fraction for ≥d has odd period.

Additional reference:
https://www.fq.math.ca/Papers1/42-2/quartrippon02_2004.pdf
If l(N) is odd then N has no prime factors of the form 4k + 3 and is not divisible by 4.
"""
from util.utils import timeit
import unittest


class Problem64:
    def __init__(self):
        pass

    @staticmethod
    def get_repeat(x) -> list:
        main_int = int(x)
        last = 2 * main_int

        output = []

        remainder = 1/(x - main_int)
        output.append(int(remainder))

        while int(remainder) != last:
            remainder = 1/(remainder - int(remainder))
            output.append(int(remainder))

        return output

    @timeit
    def solve(self, limit=13):
        count = 0
        ls_squares = [x**2 for x in range(int(limit**0.5) + 1)]
        # dc_period = {}
        # ls_good_primes = [p for p in primes(limit) if p % 4 == 3]

        for n in range(2, limit+1):
            if n in ls_squares or (n % 4 == 0):
                continue

            # continued_part = self.get_repeat(n**0.5)
            # period = len(continued_part)
            # dc_period[n] = period
            #
            # if period % 2 == 1:
            #     print(f'n={n}, {continued_part}')
            #     count += 1

            # has_p_factor = False
            # for p in ls_good_primes:
            #     if n % p == 0:
            #         has_p_factor = True
            #         continue
            #
            # count += has_p_factor

            r = limit = int(n**0.5)
            k, period = 1, 0
            while k != 1 or period == 0:
                k = (n - r * r) // k
                r = (limit + r) // k * k - r
                period += 1
            if period % 2 == 1:
                count += 1

        return count


class Solution64(unittest.TestCase):
    def setUp(self):
        self.problem = Problem64()

    def test_smaller_solution(self):
        self.assertEqual(4, self.problem.solve(limit=13))

    def test_solution(self):
        self.assertEqual(1322, self.problem.solve(limit=10000))


if __name__ == '__main__':
    unittest.main()

