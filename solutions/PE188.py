"""
The hyperexponentiation or tetration of a number a by a positive integer b, denoted by a↑↑b,
is recursively defined by:

a↑↑1 = a,
a↑↑(k+1) = a^(a↑↑k).

Thus we have e.g. 3↑↑2 = 3^3 = 27, hence 3↑↑3 = 3^27 = 7625597484987 and 3↑↑4 is roughly
10^(3.6383346400240996*10^12)

Find the last 8 digits of 1777↑↑1855.

ANSWER: 95962097
Solve time: ~0.001 seconds
"""
from util.utils import timeit
import unittest
from typing import Optional


def hyper_exponentiation(a: int, k: int, m: Optional[int] = None):
    """
    Compute a↑↑k mod m

    Where a↑↑k is defined recursively as
        1) a↑↑1 = a
        2) a↑↑(k+1) = a^(a↑↑k)
    """
    previous = 0
    current = 1
    while k >= 1:
        current = pow(a, current, m)
        if current == previous:  # if repeating then will repeat forever
            break
        previous = current
        k -= 1
    return current


class Problem188:
    def __init__(self):
        pass

    @timeit
    def solve(self, a, k, m):
        return hyper_exponentiation(a, k, m)


class Solution188(unittest.TestCase):
    def setUp(self):
        self.problem = Problem188()

    def test_solution(self):
        self.assertEqual(95962097, self.problem.solve(1777, 1855, int(1e8)))

    def test_hyper_exponentiation(self):
        self.assertEqual(27, hyper_exponentiation(3, 2))
        self.assertEqual(7625597484987, hyper_exponentiation(3, 3))


if __name__ == '__main__':
    unittest.main()
