"""
PROBLEM

In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

It is possible to make £2 in the following way:
1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?

ANSWER: 73682
Solve time: ~7ms
Related problems: 76, 77
"""
from util.utils import timeit
import unittest


class Problem31:
    def __init__(self):
        self.ls_coin = [200, 100, 50, 20, 10, 5, 2, 1]
        self.next_coin = {c: n for c, n in zip(self.ls_coin, self.ls_coin[1:])}

    def recursive(self, remainder: int, coin: int):
        next_coin = self.next_coin[coin]
        if next_coin == 1:
            return remainder // coin + 1

        counter = 0
        for x in range(remainder // coin + 1):
            next_coin = self.next_coin[coin]
            counter += self.recursive(remainder - x * coin, next_coin)

        return counter

    @timeit
    def solve(self, target=200):
        return self.recursive(target, coin=200)


class Solution31(unittest.TestCase):
    def setUp(self):
        self.problem = Problem31()

    def test_solution(self):
        self.assertEqual(73682, self.problem.solve(target=200))


if __name__ == '__main__':
    unittest.main()
