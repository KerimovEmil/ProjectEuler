"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER:
684465067343069
Solve time ~49 seconds

References:
  https://arxiv.org/pdf/1107.4890.pdf
  http://www.numericana.com/answer/numbers.htm#moebius
"""
from util.utils import timeit, mobius_sieve
import unittest
from primesieve import primes


class Problem193:
    def __init__(self, n):
        self.n = n
        self.ls_primes = None

    @timeit
    def solve(self):
        self.ls_primes = primes((self.n ** 0.5) + 1)
        print("finished calculating primes")
        limit = self.n - 1
        sq_root_n = int(self.n**0.5) + 1
        ls_m = mobius_sieve(n=sq_root_n, ls_prime=self.ls_primes)
        return sum(ls_m[i] * (limit // (i ** 2)) for i in range(1, sq_root_n))

    @timeit
    def solve_inclusion_exclusion(self):  # 46 seconds
        self.total = self.n - 1
        self.ls_primes = primes((self.n**0.5) + 1)
        self.helper_adjust(True, 1, 0)
        return self.total

    def helper_adjust(self, even_bool, prev_prod, prime_index):
        # get next prime
        try:
            next_prime = self.ls_primes[prime_index]
        except:
            return

        next_prod = prev_prod * next_prime
        while next_prod <= int(self.n**0.5):
            n = (self.n - 1) // (next_prod * next_prod)
            if even_bool:
                self.total -= n
            else:
                self.total += n

            self.helper_adjust(not even_bool, next_prod, prime_index + 1)
            prime_index += 1
            try:
                next_prime = self.ls_primes[prime_index]
            except:
                break
            next_prod = prev_prod * next_prime


class Solution193(unittest.TestCase):
    def setUp(self):
        self.problem = Problem193(n=int(2**50))

    def test_solution(self):
        self.assertEqual(684465067343069, self.problem.solve())
        # self.assertEqual(684465067343069, self.problem.solve_inclusion_exclusion())


if __name__ == '__main__':
    unittest.main()
