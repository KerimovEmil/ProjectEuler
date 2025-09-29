"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER: 684465067343069
Solve time: ~23 seconds

References:
  https://arxiv.org/pdf/1107.4890.pdf
  http://www.numericana.com/answer/numbers.htm#moebius
  https://arxiv.org/pdf/1107.4890.pdf
"""
from util.utils import primes_upto as primes

import unittest
from util.utils import timeit, mobius_sieve


class Problem193:
    def __init__(self, n):
        self.n = n
        self.ls_primes = None
        self.limit = None
        self.total = None
        self.ls_sq_primes = None
        self.num_primes = None

    @timeit
    def solve_mobius(self):  # 49 seconds
        self.ls_primes = primes((self.n ** 0.5) + 1)
        print("finished calculating primes")
        limit = self.n - 1
        sq_root_n = int(self.n ** 0.5) + 1
        ls_m = mobius_sieve(n=sq_root_n, ls_prime=self.ls_primes)
        print("finished calculating mobius values")
        return sum(ls_m[i] * (limit // (i ** 2)) for i in range(1, sq_root_n))

    @timeit
    def solve_count_p_square(self):  # 30 seconds
        self.ls_primes = primes((self.n ** 0.5) + 1)
        self.ls_sq_primes = [p*p for p in self.ls_primes]
        len_primes = len(self.ls_primes)
        print("finished calculating primes")
        ls = [(i, p2) for i, p2 in enumerate(self.ls_sq_primes)]
        total = self.n - 1
        limit = self.n - 1
        sig = 1
        while ls:
            sig *= -1
            new_ls = []
            for i, q in ls:
                total += (limit // q) * sig
                for j in range(i + 1, len_primes):
                    pq = self.ls_sq_primes[j] * q
                    if pq > self.n:
                        break
                    new_ls.append((j, pq))
            ls = new_ls
        return total

    @timeit
    def solve_inclusion_exclusion(self):  # 23 seconds
        self.limit = self.n - 1
        self.total = self.n - 1
        self.ls_primes = primes((self.n ** 0.5) + 1)
        self.ls_sq_primes = [p * p for p in self.ls_primes]
        self.num_primes = len(self.ls_primes)
        self.inclusion_exclusion_helper(odd_even=-1, prev_prod=1, prime_index=0, next_prod=4)
        return self.total

    def inclusion_exclusion_helper(self, odd_even, prev_prod, prime_index, next_prod):
        while next_prod <= self.n:
            self.total += (self.limit // next_prod) * odd_even
            prime_index += 1

            if prime_index >= self.num_primes:
                break

            next_prime_sq = self.ls_sq_primes[prime_index]
            self.inclusion_exclusion_helper(odd_even=-odd_even, prev_prod=next_prod, prime_index=prime_index,
                                            next_prod=next_prod*next_prime_sq)
            next_prod = prev_prod * next_prime_sq


class Solution193(unittest.TestCase):
    def setUp(self):
        self.problem = Problem193(n=int(2 ** 50))

    def test_solution(self):
        # self.assertEqual(684465067343069, self.problem.solve_mobius())
        # self.assertEqual(684465067343069, self.problem.solve_count_p_square())
        self.assertEqual(684465067343069, self.problem.solve_inclusion_exclusion())


if __name__ == '__main__':
    unittest.main()
