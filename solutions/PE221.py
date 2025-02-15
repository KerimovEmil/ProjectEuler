"""
PROBLEM

We shall call a positive integer "A" an "Alexandrian integer", if there exist integers a,b,c such that:

A = a*b*c
and
1/A = 1/a + 1/b + 1/c

For example, 630 is an Alexandrian integer (a=5, b=-7, c=-18). In fact, 630 is the
6th Alexandrian integer, the first 6 Alexandrian integers being: 6,42,120,156,420, and 630.

Find the 150000th Alexandrian integer

ANSWER:
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


def factor_pairs(n):
    pairs = []
    for p in range(1, int(abs(n)**0.5) + 1):
        if n % p == 0:  # p is a factor of N
            q = n // p
            pairs.append((p, q))
            # if p != q:  # Avoid duplicate pairs when p == q (e.g., N = 4, (2,2))
            #     pairs.append((-p, -q))  # Include negative factors as well
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
        ls_sol = []
        set_sol_seen = set()

        def add(x, y, z):
            product = x*y*z
            # print(f'{p=}, {x=}, {y=}, {z=}, {len(ls_sol)=}')
            a_1 = min(x, y, z)
            a_3 = max(x, y, z)
            a_2 = sum([x, y, z]) - a_1 - a_3
            if (a_1, a_2, a_3) in set_sol_seen:
                return
            else:
                print(f'p={product}, x={a_1}, y=-{a_2}, z=-{a_3}, {len(ls_sol)=}')
                ls_sol.append(product)
                set_sol_seen.add((a_1, a_2, a_3))

        a = 1
        while len(ls_sol) < 2*self.n:
            a += 1
            ls_factor_pair = factor_pairs(a**2 + 1)
            for p, q in ls_factor_pair:
                # note that p < a and q > a based on how p and q are found
                print(f'{a=}, {a-p=}, {q-a=}')
                add(a, a-p, q-a)

        ls_sol.sort()
        print(ls_sol)
        return ls_sol[self.n - 1]


class Solution221(unittest.TestCase):
    def setUp(self):
        self.problem = Problem221(n=150_000)

    def test_small_solution(self):
        # self.assertEqual(630, Problem221(n=6).naive_solve())
        self.assertEqual(630, Problem221(n=6).solve())

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()



# p=6, x=-3, y=-2, z=1, len(ls_sol)=0
# p=42, x=-7, y=-3, z=2, len(ls_sol)=1
# p=120, x=-8, y=-5, z=3, len(ls_sol)=2
# p=156, x=-13, y=-4, z=3, len(ls_sol)=3
# p=1428, x=-17, y=-12, z=7, len(ls_sol)=4
# p=630, x=-18, y=-7, z=5, len(ls_sol)=5
# p=420, x=-21, y=-5, z=4, len(ls_sol)=6
# p=2184, x=-21, y=-13, z=8, len(ls_sol)=7
# p=8970, x=-30, y=-23, z=13, len(ls_sol)=8
# p=930, x=-31, y=-6, z=5, len(ls_sol)=9
# p=2016, x=-32, y=-9, z=7, len(ls_sol)=10
# p=8364, x=-41, y=-17, z=12, len(ls_sol)=11
# p=1806, x=-43, y=-7, z=6, len(ls_sol)=12
# p=23994, x=-43, y=-31, z=18, len(ls_sol)=13
# p=21114, x=-46, y=-27, z=17, len(ls_sol)=14
# p=10998, x=-47, y=-18, z=13, len(ls_sol)=15
# p=37506, x=-47, y=-38, z=21, len(ls_sol)=16
# p=4950, x=-50, y=-11, z=9, len(ls_sol)=17
# p=39270, x=-55, y=-34, z=21, len(ls_sol)=18
# p=3192, x=-57, y=-8, z=7, len(ls_sol)=19
# p=120156, x=-68, y=-57, z=31, len(ls_sol)=20
# p=10296, x=-72, y=-13, z=11, len(ls_sol)=21
# p=5256, x=-73, y=-9, z=8, len(ls_sol)=22
# p=133152, x=-73, y=-57, z=32, len(ls_sol)=23
# p=28050, x=-75, y=-22, z=17, len(ls_sol)=24
# p=57684, x=-76, y=-33, z=23, len(ls_sol)=25


# p=6, x=-3, y=-2, z=1, len(ls_sol)=0
# p=42, x=-7, y=-3, z=2, len(ls_sol)=1
# p=120, x=-8, y=-5, z=3, len(ls_sol)=2
# p=156, x=-13, y=-4, z=3, len(ls_sol)=3
# p=1428, x=-17, y=-12, z=7, len(ls_sol)=4
# p=630, x=-18, y=-7, z=5, len(ls_sol)=5
# p=420, x=-21, y=-5, z=4, len(ls_sol)=6
# p=2184, x=-21, y=-13, z=8, len(ls_sol)=7
# p=8970, x=-30, y=-23, z=13, len(ls_sol)=8
# p=930, x=-31, y=-6, z=5, len(ls_sol)=9
# p=2016, x=-32, y=-9, z=7, len(ls_sol)=10