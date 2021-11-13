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
  https://arxiv.org/pdf/1107.4890.pdf  # todo implement this
"""
from primesieve import primes

import unittest
from util.utils import timeit, mobius_sieve, primes_of_n


class Problem193:
    def __init__(self, n):
        self.n = n
        self.ls_primes = None

    @timeit
    def solve(self):  # 49 seconds
        self.ls_primes = primes((self.n ** 0.5) + 1)
        print("finished calculating primes")
        limit = self.n - 1
        sq_root_n = int(self.n ** 0.5) + 1
        ls_m = mobius_sieve(n=sq_root_n, ls_prime=self.ls_primes)
        print("finished calculating mobius values")
        return sum(ls_m[i] * (limit // (i ** 2)) for i in range(1, sq_root_n))

    @timeit
    def solve_2(self):  # 31 seconds
        self.ls_primes = primes((self.n ** 0.5) + 1)
        len_primes = len(self.ls_primes)
        print("finished calculating primes")
        ls = [(i, p) for i, p in enumerate(self.ls_primes)]
        total = self.n - 1
        limit = self.n - 1
        sq_root_n = int(self.n ** 0.5)
        sig = 1
        while ls:
            sig *= -1
            new_ls = []
            for i, q in ls:
                total += limit // (q * q) * sig
                # for j, p in enumerate(self.ls_primes[i+1:]):
                #     pq = p*q
                #     if pq > sq_root_n:
                #         break
                #     new_ls.append((i+1+j, pq))
                for j in range(i + 1, len_primes):
                    pq = self.ls_primes[j] * q
                    if pq > sq_root_n:
                        break
                    new_ls.append((j, pq))
            ls = new_ls
        return total

    @timeit
    def solve_inclusion_exclusion(self):  # 25 seconds
        self.total = self.n - 1
        self.ls_primes = primes((self.n ** 0.5) + 1)
        self.ls_sq_primes = [p * p for p in self.ls_primes]
        self.num_primes = len(self.ls_primes)
        self.helper_adjust(odd_even=-1, prev_prod=1, prime_index=0)
        return self.total

    def helper_adjust(self, odd_even, prev_prod, prime_index):
        if prime_index >= self.num_primes:
            return

        # get next prime
        next_prime_sq = self.ls_sq_primes[prime_index]

        next_prod = prev_prod * next_prime_sq
        while next_prod <= self.n:
            self.total += ((self.n - 1) // next_prod) * odd_even
            prime_index += 1

            self.helper_adjust(odd_even=-odd_even, prev_prod=next_prod, prime_index=prime_index)
            # next_prime = self.ls_sq_primes[prime_index]

            if prime_index < self.num_primes:
                next_prime_sq = self.ls_sq_primes[prime_index]
            else:
                break
            next_prod = prev_prod * next_prime_sq  # 1*2, 1*3, 1*5

    def GetResult(self, Index, odd_even, sq_primes, UpperLimit):
        self.count += odd_even * UpperLimit
        i = Index

        while (i < len(sq_primes)) and (sq_primes[i] <= UpperLimit):
            self.GetResult(i + 1, -1 * odd_even, sq_primes, UpperLimit // sq_primes[i])
            i += 1

    def GetResult_2(self, odd_even, sq_primes, upper_limit):
        self.count += odd_even * upper_limit
        for j, p2 in enumerate(sq_primes):
            if p2 > upper_limit:
                print(p2, upper_limit, 'break')
                break
            self.GetResult_2(-1*odd_even, sq_primes[j+1:], upper_limit // p2)

    def weird_solve(self):
        self.count = 0

        self.ls_primes = primes((self.n ** 0.5) + 1)

        # sq_primes = [p*p for p in self.ls_primes]
        # self.GetResult_2(odd_even=1, sq_primes=sq_primes, upper_limit=self.n)

        # primes2 = [p*p for p in self.ls_primes][::-1]
        primes2 = [p*p for p in self.ls_primes]
        self.GetResult(1, 1, primes2, self.n)

        return self.count


class Solution193(unittest.TestCase):
    def setUp(self):
        self.problem = Problem193(n=int(2 ** 50))

    def test_solution(self):
        # self.assertEqual(684465067343069, self.problem.solve())
        # self.assertEqual(684465067343069, self.problem.solve_2())
        # self.assertEqual(684465067343069, self.problem.weird_solve())
        self.assertEqual(684465067343069, self.problem.solve_inclusion_exclusion())


if __name__ == '__main__':
    unittest.main()
