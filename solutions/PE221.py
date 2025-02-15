"""
PROBLEM

We shall call a positive integer "A" an "Alexandrian integer", if there exist integers a,b,c such that:

A = a*b*c
and
1/A = 1/a + 1/b + 1/c

For example, 630 is an Alexandrian integer (a=5, b=-7, c=-18). In fact, 630 is the
6th Alexandrian integer, the first 6 Alexandrian integers being: 6,42,120,156,420, and 630.

Find the 150000th Alexandrian integer

ANSWER: < 2134329764599620
Solve time:
"""
from util.utils import timeit, is_int, primes_of_n
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
# wlog let |a| >= |b| >= |c|
# fix k, k*b + b*c + k*c = 1
# (k+b)*(k+c) - k^2 = 1
# 1 + k^2 = p*q = (k+b)*(k+c), with b=p-k, c=q-k

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


def factor_pairs(n):
    pairs = []
    for p in range(1, int(abs(n)**0.5) + 1):
        if n % p == 0:  # p is a factor of N
            q = n // p
            pairs.append((p, q))
    return pairs


class Problem221:
    def __init__(self, n):
        self.n = n

    @timeit
    def naive_solve(self):
        ls_sol = []

        def check(x, y, z):
            if y == -z:
                return False
            return x == (1 - y*z) / (y+z)

        def add(x, y, z):
            p = x*y*z
            print(f'{p=}, {x=}, {y=}, {z=}, {len(ls_sol)=}')
            ls_sol.append(p)

        a = 1
        while len(ls_sol) < 2*self.n:
            a += 1
            for b in range(1, a + 1):
                for c in range(1, b + 1):
                    a_neg, b_neg, c_neg = -a, -b, -c
                    if check(a_neg, b, c_neg):
                        add(a_neg, b, c_neg)
                    elif check(a_neg, b_neg, c):
                        add(a_neg, b_neg, c)
                    elif check(a, b_neg, c_neg):
                        add(a, b_neg, c_neg)
        ls_sol.sort()
        print(ls_sol)
        return ls_sol[self.n - 1]

    @timeit
    def solve(self):
        set_sol_seen = set()

        def add(x, y, z):
            product = x*y*z
            a_1 = min(x, y, z)
            a_3 = max(x, y, z)
            a_2 = sum([x, y, z]) - a_1 - a_3
            if product in set_sol_seen:
                print(f'LOOK HERE (p={product}, x={a_1}, y=-{a_2}, z=-{a_3})')
                return
            else:
                print(f'p={product}, x={a_1}, y=-{a_2}, z=-{a_3}, {len(set_sol_seen)=}')
                set_sol_seen.add(product)

        a = 1
        while len(set_sol_seen) < 2*self.n:
            a += 1

            n = a**2 + 1
            for p in range(1, a):
                if n % p == 0:  # p is a factor of N
                    q = n // p

                    # note that p < a and q > a based on how p and q are found
                    print(f'{a=}, {a-p=}, {q-a=}, {p=}, {q=}')
                    add(a, a - p, q - a)

            # ls_factor_pair = factor_pairs(a**2 + 1)
            # for p, q in ls_factor_pair:
            #     # note that p < a and q > a based on how p and q are found
            #     print(f'{a=}, {a-p=}, {q-a=}')
            #     add(a, a-p, q-a)

        ls_sol = list(set_sol_seen)
        ls_sol.sort()
        print(ls_sol)
        return ls_sol[self.n - 1]

    def solve_2(self):  # fewer calls than solve
        seen = set()  # Set to track seen numbers

        k = 1
        while len(seen) < 4*self.n:
            n = k ** 2 + 1
            for p in range(1, k):
                if n % p == 0:
                    # q = n // p
                    # a, b, c = k, k - p, q - k
                    # product = a * b * c
                    product = k * (k - p) * (n // p - k)
                    if product not in seen:
                        seen.add(product)
                        # print(f'{k=}, {product=}, {len(seen)=}')
            k += 1

        return sorted(list(seen))[self.n - 1]


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem221(n=150_000)

    def test_small_solution(self):
        # self.assertEqual(630, Problem221(n=6).naive_solve())
        # self.assertEqual(630, Problem221(n=6).solve())
        self.assertEqual(630, Problem221(n=6).solve_2())

    def test_solution(self):
        self.assertEqual(2134329764599620, self.problem.solve_2())


if __name__ == '__main__':
    unittest.main()
