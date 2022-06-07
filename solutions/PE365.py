"""
PROBLEM

The binomial coefficient (10^18 choose 10^9) is a number with more than 9 billion digits.

Let M(n,k,m) denote the binomial coefficient (n choose k) mod m.

Calculate sum of M(10^18, 10^9, p*q*r) for 1000 < p < q < r < 5000 and p, q, r prime.

ANSWER: 162619462356610313
Solve time: ~4 minutes 30 seconds

References:
    https://en.wikipedia.org/wiki/Lucas%27s_theorem
"""

from util.utils import timeit, combin
import unittest
from primesieve import primes
from util.crt import simple_crt_all_primes


def number_base_rep(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits


class Problem365:
    def __init__(self, n=pow(10, 18), k=pow(10, 9), min_prime=1000, max_prime=5000):
        self.n = n
        self.k = k
        self.min_prime = min_prime
        self.max_prime = max_prime

        self.ls_p = list(primes(min_prime, max_prime))

    def get_combin_mod_p(self, p):
        """Return (self.n choose self.k) mod p"""
        n_tuple = number_base_rep(self.n, p)
        k_tuple = number_base_rep(self.k, p)

        mult = 1
        for n, k in zip(n_tuple, k_tuple):
            mult *= combin(n, k)
        return mult

    @timeit
    def solve(self):
        # get mod p for each p in self.ls_p
        ls_p_mod_p = [(p, self.get_combin_mod_p(p)) for p in self.ls_p]
        ans = 0

        for p, mod_p in ls_p_mod_p:
            print(p)
            for q, mod_q in ls_p_mod_p:
                if p < q:
                    for r, mod_r in ls_p_mod_p:
                        if q < r:
                            # ans += ChineseRemainderTheorem([mod_p, mod_q, mod_r], [p, q, r]).solve()
                            ans += simple_crt_all_primes([mod_p, mod_q, mod_r], [p, q, r])
        return ans


class Solution365(unittest.TestCase):
    def setUp(self):
        self.problem = Problem365()

    def test_solution(self):
        self.assertEqual(162619462356610313, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
