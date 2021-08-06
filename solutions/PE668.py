"""
PROBLEM

A positive integer is called square root smooth if all of its prime factors are strictly less than its square root.
Including the number 1, there are 29 square root smooth numbers not exceeding 100.

How many square root smooth numbers are there not exceeding 10000000000?

ANSWER: 2811077773

Solve time ~6 seconds
"""

import unittest
from util.utils import timeit


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

    @timeit
    def solve(self):
        # # ∑_{p≤N} min(p,⌊N//p⌋), # too slow
        # return self.n - sum(min(p, self.n//p) for p in primes(self.n))

        # x − ∑_{y=1}^{√x} (π(x//y)−π(y−1)).
        # return self.n - sum(count_primes(self.n//y) - count_primes(y-1) for y in range(1, int(self.n**0.5) + 1))

        return self.first_solution()

    def first_solution(self):
        """
        from user: shs.10978 in https://projecteuler.net/thread=668,
        which is a variant of Lucy's algo found here: https://projecteuler.net/thread=10;page=5#111677
        """
        sq_rt_n = int(self.n ** 0.5)

        lo = [i - 1 for i in range(sq_rt_n + 1)]
        hi = [0] + [self.n // i - 1 for i in range(1, sq_rt_n + 1)]

        tot = self.n
        for p in range(2, sq_rt_n + 1):
            if lo[p] == lo[p - 1]:
                continue

            tot -= p  # all multiples of p less than p * p is not

            p_cnt = lo[p - 1]
            q = p * p
            end = min(sq_rt_n, self.n // q)
            for i in range(1, end + 1):
                d = i * p
                if d <= sq_rt_n:
                    hi[i] -= hi[d] - p_cnt
                else:
                    hi[i] -= lo[self.n // d] - p_cnt
            for i in range(sq_rt_n, q - 1, -1):
                lo[i] -= lo[i // p] - p_cnt

        for k in range(1, sq_rt_n):
            tot -= k * (hi[k] - hi[k + 1])

        tot -= sq_rt_n * (hi[sq_rt_n] - lo[sq_rt_n])  # correction: for primes in (sq_rt_n, N // sq_rt_n]
        return tot


class Solution668(unittest.TestCase):
    def test_solution_1(self):
        self.assertEqual(29, Problem668(n=100).solve())

    def test_solution_2(self):
        self.assertEqual(26613, Problem668(n=100000).solve())

    def test_solution_3(self):
        self.assertEqual(268172, Problem668(n=1000000).solve())

    def test_solution_4(self):
        self.assertEqual(2719288, Problem668(n=10000000).solve())

    def test_solution_5(self):
        self.assertEqual(27531694, Problem668(n=100000000).solve())

    def test_solution_6(self):
        self.assertEqual(278418003, Problem668(n=1000000000).solve())

    def test_solution_7(self):
        self.assertEqual(2811077773, Problem668(n=10000000000).solve())


if __name__ == '__main__':
    unittest.main()
