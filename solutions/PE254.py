"""
PROBLEM

Define f(n) as the sum of the factorials of the digits of n. For example, f(342) = 3! + 4! + 2! = 32.
Define sf(n) as the sum of the digits of f(n). So sf(342) = 3 + 2 = 5.
Define g(i) to be the smallest positive integer n such that sf(n) = i.
Though sf(342) is 5, sf(25) is also 5, and it can be verified that g(5) is 25.

Define sg(i) as the sum of the digits of g(i). So sg(5) = 2 + 5 = 7.
Further, it can be verified that g(20) is 267 and ∑sg(i) for 1 ≤ i ≤ 20 is 156.

What is ∑sg(i) for 1 ≤ i ≤ 150?

ANSWER:
Solve time ~ seconds
"""

from util.utils import timeit
import unittest
from math import factorial


class Problem254:
    def __init__(self):
        pass

    @timeit
    def solve(self, max_num: int = 20) -> int:
        dc_factorial = {i: factorial(i) for i in range(10)}

        def f(n: int) -> int:
            return sum(dc_factorial[int(i)] for i in str(n))

        def sf(n: int) -> int:
            return sum(int(i) for i in str(f(n)))

        dc_g = {}
        s_needed = {i for i in range(1, max_num + 1)}

        i = 0
        while len(s_needed) > 0:
            i += 1  # todo replace this with only looping over ordered numbers, i.e smaller digits first
            v = sf(i)
            if v not in dc_g.keys():
                if v in s_needed:
                    s_needed.remove(v)
                    print(f'n={max_num}, i={i}, left: {s_needed}')
                dc_g[v] = i

        def sg(n: int) -> int:
            return sum(int(i) for i in str(dc_g[n]))

        ans = sum(sg(i) for i in range(1, max_num + 1))
        return ans


class Solution254(unittest.TestCase):
    def setUp(self):
        self.problem = Problem254()

    def test_20_solution(self):
        self.assertEqual(156, self.problem.solve(20))

    def test_40_solution(self):
        self.assertEqual(468, self.problem.solve(40))


if __name__ == '__main__':
    unittest.main()


# g(45) = 12378889
# 12378889 -> 1!+2!+3!+7!+8!+8!+8!+9! = 1+2+6+5040+40320+40320+40320+362880
# = 488889 -> 4+8+8+8+8+9 = 45
# sf(12378889) = 45

# 342 -> 3!+4!+2! = 6+24+2 = 32  -> 3+2   = 5
# 25  -> 2!+5!    = 2+120  = 122 -> 1+2+2 = 5

# {
# 1: 1,
# 2: 2,
# 3: 5,
# 4: 15,
# 5: 25,
# 6: 3,
# 7: 13,
# 8: 23,
# 9: 6,
# 10: 16,
# 11: 26,
# 12: 44,
# 13: 144,
# 14: 256,
# 15: 36,
# 16: 136,
# 17: 236,
# 18: 67,
# 19: 167}

