"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER:
684465067343069
Solve time ~68 seconds

References:
  https://arxiv.org/pdf/1107.4890.pdf
  http://www.numericana.com/answer/numbers.htm#moebius
"""
from util.utils import timeit
import unittest
from primesieve import primes


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


@timeit
def mobius_sieve(n):  # todo speed this up. Currently take ~ 40 seconds
    """
    Returns a list of all mobius function values.
    mobius(n) = 1 if i is square-free with even number of primes,
               -1 if odd number,
                0 if contains square
    """
    ls_m = [1]*n
    ls_p = primes(int(n**0.5) + 1)
    for p in ls_p:
        ls_m[p:n:p] = [-p * x for x in ls_m[p:n:p]]
        p2 = p ** 2
        ls_m[p2:n:p2] = [0] * len(ls_m[p2:n:p2])

    ls_m = [sign(x) if abs(x) == i else sign(-x) for i, x in enumerate(ls_m)]
    return ls_m


class Problem193:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        limit = self.n - 1
        ls_m = mobius_sieve(n=int(limit ** 0.5) + 1)
        print("finished calculating mobius numbers")
        return sum(ls_m[i] * (limit // (i ** 2)) for i in range(1, int(limit ** 0.5) + 1))


class Solution193(unittest.TestCase):
    def setUp(self):
        self.problem = Problem193(n=int(2**50))

    def test_solution(self):
        self.assertEqual(684465067343069, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
