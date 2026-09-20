"""
PROBLEM

It turns out that 12 cm is the smallest length of wire that can be bent to form an integer sided right angle triangle
in exactly one way, but there are many more examples.

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer sided right angle triangle, and
other lengths allow more than one solution to be found; for example, using 120 cm it is possible to form exactly
three different integer sided right angle triangles.

120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L ≤ 1,500,000 can exactly one integer sided right
 angle triangle be formed?

ANSWER: 161667
Solve time: ~1.1 seconds
Related problems: 39
"""
from util.utils import timeit, coprime
import unittest


# a^2 + b^2 = c^2, is primitive if and only if m and n are co-prime and one of them is even, m>n.
# a = m^2 - n^2
# b = 2mn
# c = m^2 + n^2

# p = a+b+c = 2 m^2 + 2mn = 2m(m+n)
# 12 = 2*2*(2+1) -> m=2, n=1 -> a=3, b=4, c=5


class Problem75:
    def __init__(self):
        pass

    def is_product_of_two_primes(self):
        pass

    @timeit
    def solve(self, max_p=1_500_000):
        # perimeter = 2m(m+n)

        count = 0

        dc = dict()
        for m in range(1, int((max_p//2) ** 0.5)):
            for n in range(1, m):  # 1 <= n < m

                if not coprime(m, n) or (m + n) % 2 == 0:
                    continue

                p0 = 2 * m * (m + n)
                for k in range(1, max_p // p0 + 1):
                    p = k*p0

                    prev_count = dc.get(p, 0)
                    if prev_count == 0:
                        count += 1
                    elif prev_count == 1:
                        count -= 1
                    dc[p] = prev_count + 1

        return count


class Solution75(unittest.TestCase):
    def setUp(self):
        self.problem = Problem75()

    def test_solution(self):
        self.assertEqual(161667, self.problem.solve(max_p=1_500_000))


if __name__ == '__main__':
    unittest.main()
