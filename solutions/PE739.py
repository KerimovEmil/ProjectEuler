"""
PROBLEM

Take a sequence of length n. Discard the first term then make a sequence of the partial summations.
Continue to do this over and over until we are left with a single term. We define this to be f(n).

Consider the example where we start with a sequence of length 8:
1,1,1,1,1,1,1,1
1,2,3,4,5,6,7
2,5,9,14,20,27
5,14,28,48,75
14,42,90,165
42,132,297
132,429
429

Then the final number is 429, so f(8)=429.

For this problem we start with the sequence 1,3,4,7,11,18,29,47, ...
This is the Lucas sequence where two terms are added to get the next term.
Applying the same process as above we get f(8)=2663.
You are also given f(20)=742296999 modulo 1,000,000,007

Find f(10^8). Give your answer modulo 1,000,000,007.

ANSWER: 711399016
Solve time ~37 minutes
"""

from util.utils import timeit, cumsum, combin, fibonacci_n_term, fibonacci_k_n_term, basic_factorial, fib, basic_falling_factorial, binomial_recursive
import unittest
from typing import List, Optional
from functools import lru_cache

# 1, 3, 4, 7, 11, 18, 29, 47
# 3, 7, 14, 25, 43, 72, 119
# 7, 21, 46, 89, 161, 280
# 21, 67, 156, 317, 597
# 67, 223, 540, 1137
# 223, 763, 1900
# 763, 2663
# 2663

# 1, 3, 7, 21, 67, 223, 763, 2663, 9435

# 1  2   3      4      5         6        7            8           9
# a, b, a+b,   a+2b, 2a+3b,     3a+5b,   5a+8b,       8a+13b    13a+21b
#    b, a+2b, 2a+4b, 4a+7b,    7a+12b,  12a+20b,     20a+33b
#       a+2b, 3a+6b, 7a+13b,  14a+25b,  26a+45b,     46a+78b
#             3a+6b, 10a+19b, 24a+44b,  50a+89b,    96a+167b
#                    10a+19b, 34a+63b,  84a+152b,  180a+319b
#                             34a+63b,  118a+215b, 298a+534b
#                                       118a+215b, 416a+749b
#                                                  416a+749b
#                                                             1485a+2650b

# 1485 = (5+8) + 20 + 46 + 96 + 180 + 298 + 416*2
# 2650 = (8+13) + 33 + 78 + 167 + 319 + 534 + 749*2

# therefore we have the following sequence for f(n):
# n   f(n)
# 1    a
# 2    b
# 3   a+2b
# 4   3a+6b
# 5   10a+19b
# 6   34a+63b
# 7   118a+215b
# 8   416a+749b
# 9   1485a+2650b

# coefficient on a: 1,3,10,34,118,416,1485
# coefficient on b: 1,2,6,19,63,215,749,2650


def catalan_transform(n: int = 1, seq: List[int] = None, mod_m: Optional[int] = None) -> int:
    if n == 0:
        return 0
    if mod_m is not None:
        return int(sum((i * combin(2*n-i, n-i) * seq[i] // (2*n-i)) % mod_m for i in range(1, n+1)))
    else:
        return int(sum(i * combin(2*n-i, n-i) * seq[i] // (2*n-i) for i in range(1, n+1)))


def inv_catalan_transform(n: int = 1, seq: List[int] = None, mod_m: Optional[int] = None) -> int:
    """http://www.kurims.kyoto-u.ac.jp/EMIS/journals/JIS/VOL8/Barry/barry84.pdf"""
    return sum(combin(i, n-i) * (-1)**(n-i) * seq[i] for i in range(n+1))


# a_n = [0, 1, 1, 2, 3, 5, 8, 13, 21]
# b_n = [catalan_transform(n=x, seq=[1, 1, 2, 3, 5, 8, 13, 21]) for x in range(8)]
# b_n = [0, 1, 2, 6, 19, 63, 215, 749]
# a_new_n = [inv_catalan_transform(n=x, seq=b_n) for x in range(8)]
# a_new_n = [0, 1, 1, 2, 3, 5, 8, 13]


# [0, 1, 2, 4, 7, 12, 20] = [1, 2, 3, 5, 8, 13, 21] - 1
# b_n = [catalan_transform(n=x, seq=[0, 1, 2, 4, 7, 12, 20]) for x in range(8)]
# [0, 1, 3, 10, 34, 118, 416]

# a_i = [0, 1, 1, 2, 3, 5, 8, 13, 21] = f_i
# b_n = sum for i from 0 to n:
#        i/(2*n-i) * combin(2*n - i, n-i) * f_i

# basic_factorial(2*n-i-1) /basic_factorial(n - i)/ basic_factorial(n) * i

# n*(n-3)*a(n) +2*(-4*n^2+15*n-10)*a(n-1) +(15*n^2-69*n+80)*a(n-2) +2*(n-2)*(2*n-5)*a(n-3)=0

# @lru_cache(maxsize=None)
# def a(n: int, mod_m: int) -> int:
#     """n*(n-3)*a(n) +2*(-4*n^2+15*n-10)*a(n-1) +(15*n^2-69*n+80)*a(n-2) +2*(n-2)*(2*n-5)*a(n-3)=0"""
#     if n == 2:
#         return 1
#     elif n == 3:
#         return 3
#     elif n == 4:
#         return 10
#     d = n*(n-3)
#     return int(-2*(-4*n**2+15*n-10)/d * a(n-1, mod_m)
#                - (15*n**2-69*n+80)/d * a(n-2, mod_m)
#                - 2*(n-2)*(2*n-5)/d * a(n-3, mod_m)) % mod_m


class Problem739:
    def __init__(self, mod_n: int = 1000000007, a=1, b=3):
        self.mod_n = mod_n
        self.a = a
        self.b = b

    @timeit
    def naive_solve(self, n: int, seq: List[int]):
        for i in range(n-1):
            seq = cumsum(seq[1:])
        return seq[0]

    @timeit
    def solve(self, n: int):
        # ls_fib = [fibonacci_n_term(i) for i in range(n+1)]
        ls_fib = [fib(i) for i in range(n+1)]
        print('finished computing fibonacci terms')
        coef_a = catalan_transform(n=n-2, seq=[f-1 for f in ls_fib[2:]], mod_m=self.mod_n)
        print('finished computing a coeff')
        coef_b = catalan_transform(n=n-1, seq=ls_fib, mod_m=self.mod_n)
        print('finished computing b coeff')

        return (coef_a * self.a + coef_b * self.b) % self.mod_n

    @timeit
    def solve_3(self, n: int):
        m = n-1

        ls_fib = [fib(i, self.mod_n) for i in range(2, n)]
        print(f'finish computing {m} fibonacci numbers')

        m_sq = pow(m, 2, self.mod_n)

        bio_coeff = 1
        total_sum_a = 0
        total_sum_b = 0
        for i in range(m-2, 0, -1):
            if (i % 10000) == 0:
                print(f'{100*(1-i/m):.2f} % complete')

            # a^-1 = a^{phi(m) - 1} mod m if gcd(m,a) = 1.  Note tht phi(prime) = prime - 1
            inv_m_i_1 = pow(m-1-i, self.mod_n - 2, self.mod_n)

            bio_coeff = (bio_coeff * (2*m-2-i) * inv_m_i_1) % self.mod_n
            common = i * bio_coeff

            inv_m_x_m_i = pow(m_sq - m*i, self.mod_n - 2, self.mod_n)
            inv_2m_i_2 = pow(2*m-i-2, self.mod_n - 2, self.mod_n)

            total_sum_b += (common * ((2*m-i-1) * inv_m_x_m_i) % self.mod_n * fib(i, self.mod_n)) % self.mod_n
            total_sum_a += (common * inv_2m_i_2 * (fib(i+2, self.mod_n) - 1)) % self.mod_n

            total_sum_b %= self.mod_n
            total_sum_a %= self.mod_n

        # i = 0
        total_sum_b += fib(m, self.mod_n)

        # i = m-1
        total_sum_a += (fib(m+1, self.mod_n) - 1)
        total_sum_b += (fib(m-1, self.mod_n) * (m-1)) % self.mod_n

        # multiply by a and b and add up
        total_sum = (total_sum_a * self.a + total_sum_b * self.b) % self.mod_n

        return total_sum


class Solution739(unittest.TestCase):
    def setUp(self):
        self.problem = Problem739()

    def test_sample_solution(self):
        self.assertEqual(429, self.problem.naive_solve(n=8, seq=[1, 1, 1, 1, 1, 1, 1, 1]))

    def test_sample_solution_2(self):
        self.assertEqual(2663, self.problem.naive_solve(n=8, seq=[1, 3, 4, 7, 11, 18, 29, 47]))

    def test_catalan_fib_transform(self):
        ls_fib = [fibonacci_n_term(i) for i in range(7 + 1)]
        self.assertEqual(749, catalan_transform(n=7, seq=ls_fib))
        self.assertEqual(118, catalan_transform(n=5, seq=[f-1 for f in ls_fib][2:]))

    def test_larger_solution(self):
        """f(20)=74229699 modulo 1,000,000,007"""
        self.assertEqual(742296999, self.problem.solve_3(n=20))

    def test_solution_1e3(self):
        self.assertEqual(537806289, self.problem.solve_3(n=int(1e3)))

    def test_solution_1e4(self):
        self.assertEqual(304246173, self.problem.solve_3(n=int(1e4)))

    def test_solution_1e5(self):
        self.assertEqual(587213414, self.problem.solve_3(n=int(1e5)))

    def test_solution_1e8(self):
        self.assertEqual(711399016, self.problem.solve_3(n=int(1e8)))


if __name__ == '__main__':
    unittest.main()
