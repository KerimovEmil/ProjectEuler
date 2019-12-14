"""
PROBLEM

A positive integer n is called square-free, if no square of a prime divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are
square-free, but not 4, 8, 9, 12.

How many square-free numbers are there below 2^50?

ANSWER:
684465067343069
Solve time ~67 seconds

References:
  https://arxiv.org/pdf/1107.4890.pdf
  http://www.numericana.com/answer/numbers.htm#moebius
"""
from util.utils import timeit, primes_of_n
import unittest
from primesieve import primes


def sieve(n):
    """Return all primes <= n."""
    np1 = n + 1
    s = list(range(np1))
    s[1] = 0
    sqrtn = int(round(n ** 0.5))
    for i in range(2, sqrtn + 1):
        if s[i]:
            s[i * i: np1: i] = [0] * len(range(i * i, np1, i))
    return filter(None, s)


# public static int[] GetMu(int max)
# {
#     var sqrt = (int)Math.Floor(Math.Sqrt(max));
#     var mu = new int[max + 1];
#     for (int i = 1; i <= max; i++)
#         mu[i] = 1;
#     for (int i = 2; i <= sqrt; i++)
#     {
#         if (mu[i] == 1)
#         {
#             for (int j = i; j <= max; j += i)
#                 mu[j] *= -i;
#             for (int j = i * i; j <= max; j += i * i)
#                 mu[j] = 0;
#         }
#     }
#     for (int i = 2; i <= max; i++)
#     {
#         if (mu[i] == i)
#             mu[i] = 1;
#         else if (mu[i] == -i)
#             mu[i] = -1;
#         else if (mu[i] < 0)
#             mu[i] = 1;
#         else if (mu[i] > 0)
#             mu[i] = -1;
#     }
#     return mu;
# }

def m_2_sieve(n):
    np1 = n + 1
    ls_m = [1]*np1
    ls_p = primes(int(np1**0.5))
    for p in ls_p:
        ls_m[p:np1:p] = [-p * x for x in ls_m[p:np1:p]]
        p2 = p ** 2
        ls_m[p2:np1:p2] = [0] * len(ls_m[p2:np1:p2])

    def sign(x):
        if x < 0:
            return -1
        elif x > 0:
            return 1
        else:
            return 0

    ls_m = [sign(x) if abs(x) == i else sign(-x) for i, x in enumerate(ls_m)]
    return ls_m


def m_sieve(n):
    """
    1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square.
    f(n)*f(m) = f(n*m) if n and m are coprime.
    """
    # set convention: 0 = Prime number
    #                 1 = Product of an odd number of distinct primes.
    #                 2 = Product of an even number of distinct primes.
    #                 3 = Multiple of the square of a prime.
    # idea:
    # 1) initialize array of 0's
    # 2) set m(1) = 2  (1 is the product of 0 primes)
    # 3)

    np1 = n + 1
    # m = [0] * np1
    # m[1] = 2
    # p = 2
    # I = 2*p
    # while I <= n:
    #     J = 2
    #     while I <= n:
    #         if J == p:
    #             J = 0
    sqrtn = int(round(n ** 0.5))
    for i in range(2, sqrtn + 1):
        if s[i]:
            s[i * i: np1: i] = [0] * len(range(i * i, np1, i))
    return filter(None, s)


def m2(n, ls_prime):
    """1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square"""
    if n % 4 == 0 or n % 9 == 0:
        return 0
    if n % 2 == 0:
        return -m2(n//2, ls_prime)
    i = 0
    p = ls_prime[i]
    num_prime = 0
    while p * p <= n:
        if n % p == 0:
            num_prime += 1
            n //= p
            if n % p == 0:
                return 0
        i += 1
        p = ls_prime[i]
    if n > 1:
        num_prime += 1
    if num_prime % 2 == 0:
        return 1
    else:
        return -1


def m(n, ls_primes):
    """
    μ(n) = 1 if n is square-free with an even number of prime factors.
    μ(n) = −1 if n is square-free with an odd number of prime factors.
    μ(n) = 0 if n has a squared prime factor.
    """
    dc_p = primes_of_n(n, ls_primes)
    if any(exp >= 2 for exp in dc_p.values()):
        return 0
    if len(dc_p.keys()) % 2 == 0:
        return 1
    else:
        return -1


class Problem193:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        # ls_primes = primes(self.n**0.5)
        # ls_primes = None
        limit = self.n - 1
        count = 0
        ls_m = m_2_sieve(n=int(limit ** 0.5) + 1)
        print("finished mobius numbers")
        for i in range(1, int(limit ** 0.5) + 1):
            # mobius = m(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            # mobius = m2(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            mobius = ls_m[i]
            count += mobius * (limit // (i ** 2))
        return count

    @timeit
    def solve_2(self):
        I = int((self.n/4)**(1/3))
        D = int((self.n / I)**0.5)
        s1 = self.solve_mini(D)

        ls_primes = primes(self.n ** 0.5)
        # ls_primes = None
        limit = self.n - 1
        count = 0

        for i in range(1, int(limit ** 0.5) + 1):
            # mobius = m(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            mobius = m2(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            count += mobius * (limit // (i ** 2))
        return count

    @timeit
    def solve_mini(self, D):
        ls_primes = primes(D**0.5)
        limit = self.n - 1
        count = 0
        for i in range(1, int(D ** 0.5) + 1):
            mobius = m2(i, ls_primes)  # 1 if i is square-free with even number of primes, -1 if odd number, 0 if contains square
            count += mobius * (limit // (i ** 2))
        return count


class Solution193(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem193(n=int(2**50))
        self.problem = Problem193(n=int(2**50))

    def test_solution(self):
        # self.assertEqual(83552864618, self.problem.solve())  # n = int(2**37)
        # self.assertEqual(668422917419, self.problem.solve())  # n = int(2**40)
        # self.assertEqual(21389533354934, self.problem.solve())  # n = int(2**45)
        self.assertEqual(684465067343069, self.problem.solve())  # n = int(2**50)


if __name__ == '__main__':
    unittest.main()
