"""
PROBLEM

We shall call a positive integer "A" an "Alexandrian integer", if there exist integers a,b,c such that:

A = a*b*c
and
1/A = 1/a + 1/b + 1/c

For example, 630 is an Alexandrian integer (a=5, b=-7, c=-18). In fact, 630 is the
6th Alexandrian integer, the first 6 Alexandrian integers being: 6,42,120,156,420, and 630.

Find the 150000th Alexandrian integer

ANSWER: = 1884161251122450
Solve time: 11 mins
"""
from util.utils import timeit
import unittest

# 1/(a*b*c) = 1/a + 1/b + 1/c
# a*b + b*c + a*c = 1

# note out of a,b,c two of them must always be negative.
# proof:
# - only one can't be negative since a*b*c > 0
# - three can't be negative since a*b*c > 0
# - 0 can't be negative since a*b + b*c + a*c > 1, since a,b,c >= 1

# The min(a,b,c) has to be the positive one.
# WLOG let a = min(a,b,c) then 1/a - 1/b - 1/c is the only combination that is positive.

# NAIVE approach
# wlog let |a| >= |b| >= |c|
# fix k, k*b + b*c + k*c = 1
# k*(b+c) = 1 - b*c
# k = (1 - b*c) / (b+c)

# PRIME FACTORIZATION APPROACH
# fix k, k*b + b*c + k*c = 1
# (k+b)*(k+c) - k^2 = 1
# 1 + k^2 = p*q = (k+b)*(k+c), with b=p-k, c=q-k
# note that k will be negative, k=-k*

# e.g. k=8,
# 8^2 + 1 = 65 = 13*5 = 65*1
# case 1: p=13-8=5, q=5-8=-3, (a,b,c) = (3,-5,-8)
# case 2: p=65-8=57, q=1-8=-7, (a,b,c) = (7,-8,-57)

# note that p-k < 0 and q-k > 0
# therefore |q-k| < |k|, so k must always be one of the negative options
# either (k-p) or (q-k) can be the smallest numbers

# note A = k*(k-p)*(q-k) = k*(kq - k^2 - pq + kp)
# A = k*(kq - k^2 - (1+k^2) + kp)
# A = k*(kq + kp - 1 - 2*k^2)
# A = k*(k*(q + p) - 1 - 2*k^2)
# A = (q + p)*k^2 - k - 2*k^3
# A = (q + p - 2k)*k^2 - k


class Problem221:
    def __init__(self, n):
        self.n = n

    def solve(self):
        #  Set to track seen numbers
        seen = set()

        k = 1
        while len(seen) < 4*self.n:
            n = k ** 2 + 1
            for p in range(1, k+1):
                if n % p == 0:
                    # a, b, c = k, k - p, n // p - k
                    product = k * (k + p) * (n // p + k)
                    if product not in seen:
                        seen.add(product)
            k += 1

        return sorted(list(seen))[self.n - 1]


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem221(n=150_000)

    def test_small_solution(self):
        self.assertEqual(630, Problem221(n=6).solve())

    def test_solution(self):
        self.assertEqual(1884161251122450, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
