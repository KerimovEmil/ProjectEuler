"""
PROBLEM

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper
 fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:
1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.
How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d ≤ 12,000?

ANSWER:
7295372
Solve time ~0.007 seconds  # easy solution in ~9.7 seconds
"""

from util.utils import timeit, len_faray_seq
import unittest


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
        index_of_half = int((len_f - 1)/2)

        index_of_one_third = self.quick_index_of_one_third(self.d)

        return index_of_half - index_of_one_third - 1

    def fastest_solve(self):  # TODO figure out exactly why this works.
        N = self.d
        K = int((N / 2) ** 0.5)
        M = int(N / (2 * K + 1))
        rsmall = [0 for _ in range(M + 1)]
        rlarge = [0 for _ in range(K)]

        def f(n):
            q = n // 6
            r = n % 6
            ans = q * (3 * q - 2 + r)
            if r == 5:
                ans += 1
            return ans

        def R(n):
            switch = int((n / 2) ** 0.5)
            count = f(n)
            count -= f(n // 2)
            m = 5
            k = (n - 5) // 10
            while k >= switch:
                k2 = ((n // (m + 1)) - 1) // 2
                count -= (k - k2) * rsmall[m]
                k = k2
                m += 1
            while k > 0:
                m = n // (2 * k + 1)
                if m <= M:
                    count -= rsmall[m]
                else:
                    count -= rlarge[((N // m) - 1) // 2]
                k -= 1
            if n <= M:
                rsmall[n] = count
            else:
                rlarge[((N // n) - 1) // 2] = count
            return

        for n in range(5, M + 1):
            R(n)

        for j in range(K - 1, -1, -1):
            R(N // (2 * j + 1))

        count = rlarge[0]
        return count


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
