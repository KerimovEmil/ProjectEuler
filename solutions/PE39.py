"""
PROBLEM

If p is the perimeter of a right angle triangle with integral length sides,
{a,b,c}, there are exactly three solutions for p = 120.

(20,48,52), (24,45,51), (30,40,50)

For which value of p <= 1000, is the number of solutions maximised?

ANSWER: 840
Solve time: ~0.05 seconds
"""

# (a,b,c) int s.t. a^2 + b^2 = c^2

# a = k(m^2 - n^2)
# b = k(2mn)
# c = k(m^2 + n^2)

# m>n, and m,n,k >0 ints

# perimeter = a + b + c
# perimeter = k*(m^2 - n^2 + 2mn + m^2 - n^2)
# perimeter = 2km(m + n)

# therefore perimeter must always be even.

import unittest
from util.utils import timeit


class Problem39:
    """For which value of p <= 1000, is the number of solutions maximised?"""

    def __init__(self, max_perimeter):
        self.max_perimeter = max_perimeter
        self.ans = 0
        self.max_solutions = 0
        self.ls_p_triples = []

    @timeit
    def generate_pythagorean_triples(self, max_n, max_m):
        """Generate list of pythagorean triples sets"""
        ls_p_triples = []
        for n in range(1, max_n):
            for m in range(n + 1, max_m):
                # perimeter = 2km(m + n)
                max_k = int(self.max_perimeter / (2 * m * (m + n)))
                for k in range(1, max_k + 1):
                    a = k * (m * m - n * n)
                    b = k * 2 * n * m
                    c = k * (m * m + n * n)
                    if {a, b, c} not in ls_p_triples:
                        ls_p_triples.append({a, b, c})
        return ls_p_triples

    def num_p(self, p):
        """Given a perimeter, p, return the number of Pythagorean triples."""
        return sum([sum(triple) == p for triple in self.ls_p_triples])

    @timeit
    def solve(self):
        self.ls_p_triples = self.generate_pythagorean_triples(30, 30)
        for i in range(10, self.max_perimeter, 2):  # perimeter must be even
            num_of_solutions = self.num_p(i)
            if self.max_solutions < num_of_solutions:
                self.max_solutions = num_of_solutions
                self.ans = i

        return self.ans

    def get_solution(self):
        return self.ans


class Solution39(unittest.TestCase):
    def setUp(self):
        self.problem = Problem39(max_perimeter=1000)

    def test_solution(self):
        self.assertEqual(840, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
