"""
PROBLEM

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
 fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:
1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.
How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d ≤ 12,000?

ANSWER: 7295372
Solve time ~0.004 seconds  # easy solution in ~9.7 seconds
"""

import unittest
from util.utils import timeit, len_faray_seq


class Problem73:
    def __init__(self, d):
        self.d = d

    @staticmethod
    def quick_index_of_one_third(n):
        a, b, c, d = 0, 1, 1, n
        ans = 0
        while c <= n:
            k = int((n + b) / d)
            a, b, c, d = c, d, k * c - a, k * d - b
            ans += 1
            if a == 1 and b == 3:
                return ans
        return ans

    @timeit
    def solve(self):
        len_f = len_faray_seq(self.d)  # very fast

        # note that the middle value will always be 1/2 for all n>1
        # therefore there are always (|F_n| - 1)/2 elements that are less than 1/2
        index_of_half = int((len_f - 1) / 2)

        index_of_one_third = self.quick_index_of_one_third(self.d)

        return index_of_half - index_of_one_third - 1

    def fastest_solve(self):
        """
        See description of why this works here: https://projecteuler.net/overview=073.
        The rough idea is to express the number of fractions between x and y as a sum of the number of reduced fractions
        between x and y. Then represent that sum in an easier form. Then use a mobius summation inversion to represent
        the number of reduced fractions between  and y as a sum of the number of fractions between x and y.
        Define F(N) = number of fractions between x and y, where the denominator <= N
        Define R(N) = number of reduced fractions between x and y, where the denominator <= N

        (EQ1) F(N) = sum_{m=1}^{N} R(floor(N/m))
        This can be seen since (the number of fractions between x,y with gcm(num, den) == m) = R(floor(N/m)

        One can also see that F(m) = sum_{n=1}^{m} (floor((n-1)/2) - floor(n/3)), for x=1/3 and y = 1/2.
        This sum can be evaluated directly, I'm not 100% sure how though, but it becomes
        (EQ2) F(m) = q*(3q - 2 + r) + (r==5)
        where q = floor(m/6), r = m%6

        Since we have an easy way to calculate F(m), we can use the mobius inversion on EQ1 to represent R(N) as a
        function of F(m). Also not 100% sure how.

        (EQ3) R(N) = sum_{m=1}^{N} mu(m) * F(floor(N/m))
        Where mu(m) is the mobius function defined as
        (EQ4) mu(m) = (-1)^r if n is the product of r distinct primes, 0 if n has a square

        This gives us
        (EQ5) R(N) = F(N) - sum_{m=2}^{N} R(floor(N/m))
        We could just stop here, but we can get a better algorithm

        (EQ6) R(N) = F(N) - F(floor(N/2)) - sum_{k=1}^{floor((N-1)/2)} R(floor(N/(2k+1)))
        Notice that floor(N/(2k+1)) will be constant for many values of k when N is large. Counting these we get:
        N/(2k-1) - N/(2k+1) > 1, implies k <= sqrt(N/2)
        therefore defined k0 = floor(sqrt(N/2))
        Using this idea, and a lot of math we get the below algorithm.
        """

        K = int((self.d / 2) ** 0.5)
        M = int(self.d / (2 * K + 1))
        ls_r_small = [0] * (M + 1)  # R(m)
        ls_r_large = [0] * K  # R(int(N/(2k-1))

        def f(d):
            """Returns the number of fractions between 1/3 and 1/2 whose denominators are less than d"""
            q, r = d // 6, d % 6
            return q * (3 * q - 2 + r) + (r == 5)

        def R(n):
            """Sets values in ls_r_small and ls_r_large"""
            switch = int((n / 2) ** 0.5)
            count = f(n) - f(n // 2)
            m = 5  # the first 5 are 0
            k = (n - 5) // 10
            while k >= switch:
                k2 = ((n // (m + 1)) - 1) // 2
                count -= (k - k2) * ls_r_small[m]  # -(k(m)-k(m+1))*R(m)
                k = k2
                m += 1
            while k > 0:
                m = n // (2 * k + 1)
                if m <= M:
                    count -= ls_r_small[m]  # -R(m)
                else:
                    count -= ls_r_large[((self.d // m) - 1) // 2]  # -R(int(N/(2k-1))
                k -= 1
            if n <= M:
                ls_r_small[n] = count
            else:
                ls_r_large[((self.d // n) - 1) // 2] = count

        # call R(5), R(6), ..., R(M)
        for i in range(5, M + 1):
            R(i)

        # call R(K-1), R(K-2), ..., R(0)
        for j in range(K - 1, -1, -1):
            R(self.d // (2 * j + 1))

        return ls_r_large[0]  # R(int(N/(2*0-1))) = R(N)


class Solution73(unittest.TestCase):
    def setUp(self):
        self.problem = Problem73(d=12000)

    def test_solution(self):
        # self.assertEqual(7295372, self.problem.solve())
        self.assertEqual(7295372, self.problem.fastest_solve())

    def test_solution_small(self):
        # self.assertEqual(3, Problem73(d=8).solve())
        self.assertEqual(3, Problem73(d=8).fastest_solve())


if __name__ == '__main__':
    unittest.main()
