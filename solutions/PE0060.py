"""
The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order
the result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four
primes, 792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.

ANSWER: 26033
Solve time: ~3.8 seconds
"""

from util.utils import timeit
import unittest
from util.utils import primes_upto as primes
from typing import List
from itertools import permutations


class Problem60:
    def __init__(self, max_prime):
        self.ls_primes = primes(max_prime)
        self.set_primes = set(primes(max_prime**2))
        self.num_p = len(self.ls_primes)

    def prime_combination(self, ls: List[int]) -> bool:
        boolean = True
        for new_combination in permutations(ls, 2):
            boolean = boolean and (int(''.join(map(str, new_combination))) in self.set_primes)
        return boolean

    def get_ls_of_prime_pairs(self):
        for i_1, p1 in enumerate(self.ls_primes):
            for i_2 in range(i_1 + 1, self.num_p):
                p2 = self.ls_primes[i_2]
                if self.prime_combination([p1, p2]):
                    for i_3 in range(i_2 + 1, self.num_p):
                        p3 = self.ls_primes[i_3]
                        if self.prime_combination([p1, p2, p3]):
                            for i_4 in range(i_3 + 1, self.num_p):
                                p4 = self.ls_primes[i_4]
                                if self.prime_combination([p1, p2, p3, p4]):
                                    for i_5 in range(i_4 + 1, self.num_p):
                                        p5 = self.ls_primes[i_5]
                                        if self.prime_combination([p1, p2, p3, p4, p5]):
                                            return [p1, p2, p3, p4, p5]

    @timeit
    def solve(self):
        return sum(self.get_ls_of_prime_pairs())


class Solution60(unittest.TestCase):
    def setUp(self):
        self.problem = Problem60(max_prime=10000)

    def test_solution(self):
        self.assertEqual(26033, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
