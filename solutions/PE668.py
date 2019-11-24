"""
PROBLEM

A positive integer is called square root smooth if all of its prime factors are strictly less than its square root.
Including the number 1, there are 29 square root smooth numbers not exceeding 100.

How many square root smooth numbers are there not exceeding 10000000000?

ANSWER: 2811077773

Solve time ~18 seconds
"""

from util.utils import timeit
import unittest
from primesieve import primes, count_primes
from math import log
# resources: https://math.dartmouth.edu/~carlp/PDF/qs08.pdf

#  primes(int(100**0.5)) = primes(10) = [2, 3, 5, 7]
# len(primes(10000000000**0.5)) = 9592

# Numbers n that are sqrt(n)-smooth: if p | n then p^2 <= n when p is prime. (33)
# 1, 4, 8, 9, 12, 16, 18, 24, 25, 27, 30, 32, 36, 40, 45, 48, 49, 50, 54, 56, 60, 63, 64, 70, 72, 75, 80, 81, 84, 90,
# 96, 98, 100,

# Numbers n that are sqrt(n)-smooth: if p | n then p^2 < n when p is prime. (29)
# 1, 8, 12, 16, 18, 24, 27, 30, 32, 36, 40, 45, 48, 50, 54, 56, 60, 63, 64, 70, 72, 75, 80, 81, 84, 90, 96, 98, 100,

# primes(10) = [2, 3, 5, 7]

# number of n<=x s.t. n is sqrt(x) smooth is x - sum_{sqrt(x)<p<=x} floor(n/p)


def str_form(dc_fac):
    if len(dc_fac) == 0:
        return '1'
    else:
        out_str = ''
    new_dc_fac = dc_fac.copy()
    while len(new_dc_fac) >= 1:
        exp = new_dc_fac.popitem()
        out_str += ' * {}^{}'.format(exp[0], exp[1])
    return out_str[3:]

# prime * product of smaller primes that are less than the prime.


class Problem668:
    def __init__(self, n):
        self.n = n
        self.ans = 0

    def multiply_recurse(self, num, max_prime, ls_primes):
        if len(ls_primes) == 0:
            return num ** 0.5 > max_prime
        else:
            output_sum = self.multiply_recurse(num, max_prime, ls_primes[1:])  # skipping this prime
            p = ls_primes[0]
            max_prime = max(p, max_prime)
            ls_nums_less_than_limit = (num * (p**exp) for exp in range(1, int(log(self.n/num, p)) + 1))
            output_sum += sum(self.multiply_recurse(n, max_prime, ls_primes[1:]) for n in ls_nums_less_than_limit)
            return output_sum

    @timeit
    def solve3(self):
        ls_p = primes(int(self.n ** 0.5))[::-1]  # [7, 5, 3, 2]
        print("Finished calculating primes")
        self.ans = self.multiply_recurse(num=1, max_prime=0, ls_primes=ls_p)
        return self.ans

    @timeit
    def solve2(self):
        # ls_p = primes(int(self.n ** 0.5))  # [2, 3, 5, 7]
        limit = self.n  # change per prime using logs
        ans = 0
        max_prime = 0
        # set_answers = {1}
        for n2 in range(limit):
            if n2 > 0:
                max_prime = 2
                # num *= 2
            num = 2 ** n2
            if num > limit:
                break
            for n3 in range(limit):
                if n3 > 0:
                    max_prime = 3
                num = 2 ** n2 * 3 ** n3
                if num > limit:
                    break
                for n5 in range(limit):
                    if n5 > 0:
                        max_prime = 5
                        # num *= 5
                    num = 2 ** n2 * 3 ** n3 * 5 ** n5
                    if num > limit:
                        break
                    for n7 in range(limit):
                        if n7 > 0:
                            max_prime = 7
                            # num *= 7
                        num = 2 ** n2 * 3 ** n3 * 5 ** n5 * 7 ** n7
                        if num > limit:
                            break
                        if num ** 0.5 > max_prime:
                            # set_answers.add(num)
                            ans += 1
        # print(ans)
        # print(set_answers)
        return ans

    @timeit
    def solve(self):
        # # ∑_{p≤N} min(p,⌊N//p⌋)
        # return self.n - sum(min(p, self.n//p) for p in primes(self.n))

        # x − ∑_{y=1}^{√x} (π(x//y)−π(y−1)).
        return self.n - sum(count_primes(self.n//y) - count_primes(y-1) for y in range(1, int(self.n**0.5) + 1))


class Solution668(unittest.TestCase):
    def setUp(self):
        pass

    def test_solution_11(self):
        self.assertEqual(29, Problem668(n=100).solve())

    def test_solution_21(self):
        self.assertEqual(26613, Problem668(n=100000).solve())

    def test_solution_31(self):
        self.assertEqual(268172, Problem668(n=1000000).solve())

    def test_solution_41(self):
        self.assertEqual(2719288, Problem668(n=10000000).solve())

    def test_solution_51(self):
        self.assertEqual(27531694, Problem668(n=100000000).solve())

    def test_solution_61(self):
        self.assertEqual(278418003, Problem668(n=1000000000).solve())

    def test_solution_71(self):
        self.assertEqual(2811077773, Problem668(n=10000000000).solve())


if __name__ == '__main__':
    unittest.main()
