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

# 1+2+6+5040+40320+40320+40320+362880 = 488889 -> 4+8+8+8+8+9 = 45
# 1+2+6+9+9+9+9+27 = 72

def gen_combos(elements, length, start_idx=0):
    # ignore elements before start_idx
    for i in range(start_idx, len(elements)):
        elem, count = elements[i]  # todo add case for i=len(elements)
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

        for i in gen_combos(elements=max_elements, length=digits):
            yield int(i)
        digits += 1
        max_elements[8] = ('9', digits)

        # forced_nine = 0
        # end = ''
        # if digits > 36:
        #     forced_nine = digits - 36
        #     end = '9'*forced_nine
        # for i in gen_combos(elements=max_elements, length=digits-forced_nine):
        #     yield int(i + end)
        # # max_elements[8] = ('9', digits-forced_nine)
        # digits += 1
        # max_elements[8] = ('9', digits - forced_nine)


class Problem254:
    def __init__(self):
        pass

    @timeit
    def solve(self, max_num: int = 20) -> int:
        dc_factorial = {i: factorial(i) for i in range(1, 10)}

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

    # def test_100_solution(self):
    #     self.assertEqual(None, self.problem.solve(100))


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
# g(64) = 134445555689999999999999999999999999999999999999999999999999999999

#         122333444455555666666777777788888888 = 36 digits

# g(150) = 1233456666668888888899999... {in total: 192,901,234,567 nines}


# the reason it only works for values over 63 is because when it is less than g(63) the smallest value is not
# necessarily the smallest value for the inverse of s(n) followed by the inverse of f(n). for example for g(27)
# the smallest value possible for the inverse of s(n) is 999 however if we complete the calculation by doing the
# inverse of f(n) we would find g(27) to be 12334556 however 3+6+2+8+8+0 is also 27 and if we find the inverse of f(n)
# for 362880 we simply get g(27) to be 9 even though 362880 is much larger than 999

# def f(n:int):
#     a = sum(dc_factorial[int(i)] for i in str(n))
#     return sum(int(i) for i in str(a))


# f(9) = 1*362880 = 362880 = 27 = 9*3
# f(99) = 2*362880 = 725760 = 27 = 9*3
# f(999) = 3*362880 = 1088640 = 27 = 9*3
# f(9999) = 4*362880 = 1451520 = 18 = 9*2
# f(99999) = 5*362880 = 1814400 = 18 = 9*2
# f(999999) = 6*362880 = 2177280 = 27 = 9*3
# f(9999999) = 7*362880 = 2540160 = 18 = 9*2
# f(99999999) = 8*362880 = 2903040 = 18 = 9*2
# f(999999999) = 9*362880 = 3265920 = 27 = 9*3
# f(9999999999) = 10*362880 = 3628800 = 27 = 9*3
# f(99999999999) = 11*362880 = 3991680 = 36 = 9*4
# f(999999999999) = 12*362880 = 4354560 = 27 = 9*3
# f(9999999999999) = 13*362880 = 4717440 = 27 = 9*3
# f(99999999999999) = 14*362880 = 5080320 = 18 = 9*2
# f(999999999999999) = 15*362880 = 5443200 = 18 = 9*2
# f(9999999999999999) = 16*362880 = 5806080 = 27 = 9*3
# f(99999999999999999) = 17*362880 = 6168960 = 36 = 9*4
# f(999999999999999999) = 18*362880 = 6531840 = 27 = 9*3
# f(9999999999999999999) = 19*362880 = 6894720 = 36 = 9*4
# f(99999999999999999999) = 20*362880 = 7257600 = 27 = 9*3
# f(999999999999999999999) = 21*362880 = 7620480 = 27 = 9*3
# f(9999999999999999999999) = 22*362880 = 7983360 = 36 = 9*4
# f(99999999999999999999999) = 23*362880 = 8346240 = 27 = 9*3
# f(999999999999999999999999) = 24*362880 = 8709120 = 27 = 9*3
# f(9999999999999999999999999) = 25*362880 = 9072000 = 18 = 9*2
# f(99999999999999999999999999) = 26*362880 = 9434880 = 36 = 9*4
# f(999999999999999999999999999) = 27*362880 = 9797760 = 45 = 9*5
# f(9999999999999999999999999999) = 28*362880 = 10160640 = 18 = 9*2
# f(99999999999999999999999999999) = 29*362880 = 10523520 = 18 = 9*2

# def f9(n:int):
#     return n * dc_factorial[9]

# def s(n:int):
#     return sum(int(i) for i in str(n))

# for i in range(1, 30):
#     print(f'f({int("".join("9"*i))}) = {i}*{dc_factorial[9]} = {f9(i)} -> {s(f9(i))} = 9*{s(f9(i))//9}')
