"""
PROBLEM

For a prime $p$ let $S(p) = (\sum (p-k)!) \bmod (p)$ for $1 \le k \le 5$.

For example, if $p=7$,

$(7-1)! + (7-2)! + (7-3)! + (7-4)! + (7-5)! = 6! + 5! + 4! + 3! + 2! = 720+120+24+6+2 = 872$.

As $872 \bmod (7) = 4$, $S(7) = 4$.

It can be verified that $\sum S(p) = 480$ for $5 \le p \lt 100$.

Find $\sum S(p)$ for $5 \le p \lt 10^8$.

ANSWER: 
Solve time: 
"""

import unittest
from util.utils import timeit


class Problem381:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution381(unittest.TestCase):
    def setUp(self):
        self.problem = Problem381()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
