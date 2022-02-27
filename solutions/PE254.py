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
# from itertools import combinations_with_replacement


# g(45) = 12378889
# 12378889 -> 1!+2!+3!+7!+8!+8!+8!+9! = 1+2+6+5040+40320+40320+40320+362880
# = 488889 -> 4+8+8+8+8+9 = 45
# sf(12378889) = 45

# 342 -> 3!+4!+2! = 6+24+2 = 32  -> 3+2   = 5
# 25  -> 2!+5!    = 2+120  = 122 -> 1+2+2 = 5


def gen_combos(elements, length, start_idx=0):
    # ignore elements before start_idx
    for i in range(start_idx, len(elements)):
        elem, count = elements[i]
        if count == 0:
            continue
        # base case: only one element needed
        if length == 1:
            yield elem
        else:
            # need more than one elem: mutate the list and recurse
            elements[i] = (elem, count - 1)
            # when we recurse, we ignore elements before this one
            # this ensures we find combinations, not permutations
            for combo in gen_combos(elements, length - 1, i):
                yield elem + combo
            # fix the list
            elements[i] = (elem, count)



def non_decreasing_digits_unique_factorial_sum_generator():
    """
    First few values: todo
    1! + 1! = 2! = 2  # therefore max one 1's
    2! + 2! + 2! = 6 = 3!  # therefore max two 2's
    3! * 4 = 4!  # therefore max three 3's
    ...
    8!*9 = 9!  # therefore max eight 8s
    """
    digits = 1
    # max_elements = {str(i): 1 for i in range(1, 10)}
    # yield from range(1, 10)
    # digits = 2
    max_elements = [(str(i), i) for i in range(1, 9)]
    max_elements.append(('9', digits))
    while True:
        # for i in combos(max_elements, digits):
        for i in gen_combos(elements=max_elements, length=digits):
            yield int(i)
        digits += 1
        max_elements[8] = ('9', digits)


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

        gen_candidates = non_decreasing_digits_unique_factorial_sum_generator()
        while len(s_needed) > 0:
            i = next(gen_candidates)
            v = sf(i)
            if v not in dc_g.keys():
                if v in s_needed:
                    s_needed.remove(v)
                    print(f'g({v}) = {i}')
                    # print(f'n={max_num}, i={i}, left: {s_needed}')
                else:
                    pass
                    # print(f'not needed: g({i}) = {v}')
                dc_g[v] = i
            else:
                pass
                # print(f'non-smallest g({i})=g({dc_g[v]})={v}')

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

    def test_50_solution(self):
        self.assertEqual(997, self.problem.solve(50))

    def test_100_solution(self):
        self.assertEqual(None, self.problem.solve(100))


if __name__ == '__main__':
    unittest.main()



# g(1) = 1
# g(2) = 2
# g(6) = 3
# g(3) = 5
# g(9) = 6
# g(27) = 9
# g(7) = 13
# g(4) = 15
# g(10) = 16
# g(28) = 19
# g(8) = 23
# g(5) = 25
# g(11) = 26
# g(29) = 29
# g(15) = 36
# g(33) = 39
# g(12) = 44
# g(24) = 49
# g(18) = 67
# g(30) = 129
# g(16) = 136
# g(34) = 139
# g(13) = 144
# g(25) = 149
# g(19) = 167
# g(31) = 229
# g(17) = 236
# g(35) = 239
# g(26) = 249
# g(14) = 256
# g(20) = 267
# g(21) = 349
# g(32) = 1229
# g(36) = 1239
# g(22) = 1349
# g(23) = 2349
# g(39) = 4479
# g(37) = 13339
# g(40) = 14479
# g(38) = 23599
# g(42) = 344479
# g(43) = 1344479
# g(41) = 2355679
# g(44) = 2378889
# g(45) = 12378889
# g(46) = 133378889
# g(47) = 2356888899
# g(48) = 12356888899
# g(49) = 133356888899
# g(50) = 12245677888899
# g(51) = 34446666888899
# g(52) = 134446666888899
# g(53) = 12245578899999999
# g(54) = 123345578899999999
# g(55) = 1333666799999999999
# g(56) = 12245556666799999999999
# g(57) = 123345556666799999999999
# g(58) = 1333579999999999999999999
# g(59) = 122456679999999999999999999999
# g(60) = 1233456679999999999999999999999
# g(61) = 13444667779999999999999999999999
# g(62) = 12245555588888999999999999999999999999999
# g(63) = 123345555588888999999999999999999999999999

#         122333444455555666666777777788888888



# non-smallest g(12588)=g(49)=24
# non-smallest g(12589)=g(36)=15
# non-smallest g(12599)=g(39)=33
# non-smallest g(12666)=g(44)=12
# non-smallest g(12667)=g(349)=21
# non-smallest g(12668)=g(349)=21
# non-smallest g(12669)=g(349)=21
