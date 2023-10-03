"""
PROBLEM

Define f(n) as the sum of the factorials of the digits of n. For example, f(342) = 3! + 4! + 2! = 32.
Define sf(n) as the sum of the digits of f(n). So sf(342) = 3 + 2 = 5.
Define g(i) to be the smallest positive integer n such that sf(n) = i.
Though sf(342) is 5, sf(25) is also 5, and it can be verified that g(5) is 25.

Define sg(i) as the sum of the digits of g(i). So sg(5) = 2 + 5 = 7.
Further, it can be verified that g(20) is 267 and ∑sg(i) for 1 ≤ i ≤ 20 is 156.

What is ∑sg(i) for 1 ≤ i ≤ 150?

ANSWER: 8184523820510
Solve time: ~2 seconds
"""

from util.utils import timeit
import unittest
from math import factorial
from typing import List, Tuple

# example:
# g(45) = 12378889
# 12378889 -> 1!+2!+3!+7!+8!+8!+8!+9! = 1+2+6+5040+40320+40320+40320+362880
# = 488889 -> 4+8+8+8+8+9 = 45
# sf(12378889) = 45

# 342 -> 3!+4!+2! = 6+24+2 = 32  -> 3+2   = 5
# 25  -> 2!+5!    = 2+120  = 122 -> 1+2+2 = 5

# 1+2+6+5040+40320+40320+40320+362880 = 488889 -> 4+8+8+8+8+9 = 45
# 1+2+6+9+9+9+9+27 = 72


def gen_combos(elements: List[Tuple[str, int]], length: int):
    if length == 0:
        yield ''
        return

    if len(elements) == 1:  # last element, aka '9'
        elem, count = elements[0]
        yield elem * length
        return

    elem, count = elements[0]
    for j in range(count, -1, -1):
        if j <= length:
            for c in gen_combos(elements[1:], length=length-j):
                yield elem * j + c


def non_decreasing_digits_unique_factorial_sum_generator():
    """
    First few values: 1,2,3,4,5,6,7,8,9,12,13,14,15,16,17,18,19,22,23,...
    1! + 1! = 2! = 2  # therefore max one 1's
    2! + 2! + 2! = 6 = 3!  # therefore max two 2's
    3! * 4 = 4!  # therefore max three 3's
    ...
    8!*9 = 9!  # therefore max eight 8s
    """
    digits = 1
    max_elements = [(str(i), i) for i in range(1, 9)]
    max_elements.append(('9', digits))
    while True:

        for i in gen_combos(elements=max_elements, length=digits):
            yield int(i)
        digits += 1
        max_elements[8] = ('9', digits)


class Problem254:
    def __init__(self):
        self.dc_factorial = {i: factorial(i) for i in range(1, 10)}

    def g_large_digit_sum(self, n: int) -> int:
        """
        Examples
            n = 67 -> 67%9==4 -> '4','9'*7
            solution = (1,0,1,3,2,4,0,7,137)
            x = 1!*a + 2!*b + 3!*c + 4!*d + 5!*e + 6!*f + 7!*g + 8!*h + 9!*i = 49999999
            a<=1, b<=2, c<=3, d<=4, e<=5, f<=6, g<=7, h<=9
            49999999==1 mod 2 -> a = 1
            49999999==1 mod 3! = 1 + 2b -> b=0
            49999999==7 mod 4! = 1 + 6c -> c=1
            49999999==79 mod 5! = 7 + d*24 -> d=3
            49999999==319 mod 6! = 79 + e*120 -> e=2
            49999999==3199 mod 7! = 319 + f*720 -> f=4
            49999999==3199 mod 8! = 3199 + g*7! -> g=0
            49999999==285439 mod 9! = 3199 + h*40320 -> h=7
            49999999=285439 + i*362880 -> i=137
        """
        if n < 63:
            raise NotImplementedError
        nine, other = divmod(n, 9)
        n = int(str(other) + nine * '9')
        dc_out = {}
        explained = 0
        for i in range(1, 9):
            new_explained = n % self.dc_factorial[i + 1]
            dc_out[i] = (new_explained - explained) // self.dc_factorial[i]
            explained = new_explained
        dc_out[9] = (n - explained) // self.dc_factorial[9]
        return sum(v * k for k, v in dc_out.items())

    @staticmethod
    def solve_above_50_under_63(max_num: int) -> int:
        """for 51 <= max_num < 63, just use hard-coded values"""
        assert 51 <= max_num
        assert max_num < 63

        dc_g = {
            51: 34446666888899,
            52: 134446666888899,
            53: 12245578899999999,
            54: 123345578899999999,
            55: 1333666799999999999,
            56: 12245556666799999999999,
            57: 123345556666799999999999,
            58: 1333579999999999999999999,
            59: 122456679999999999999999999999,
            60: 1233456679999999999999999999999,
            61: 13444667779999999999999999999999,
            62: 12245555588888999999999999999999999999999,
        }

        def s(n: int) -> int:
            return sum(int(i) for i in str(n))

        ans = sum(s(dc_g[i]) for i in range(51, max_num + 1))
        return ans

    def solve_under_63(self, max_num: int) -> int:
        """for max_num < 63, no quick solutions, must run through all cases"""
        assert max_num < 63

        dc_factorial = self.dc_factorial

        def f(n: int) -> int:
            return sum(dc_factorial[int(i)] for i in str(n))

        def s(n: int) -> int:
            return sum(int(i) for i in str(n))

        dc_g = {}
        s_needed = {i for i in range(1, max_num + 1)}

        gen_candidates = non_decreasing_digits_unique_factorial_sum_generator()
        while len(s_needed) > 0:
            i = next(gen_candidates)
            v = s(f(i))
            if v not in dc_g.keys():
                if v in s_needed:
                    s_needed.remove(v)
                    # print(f'g({v}) = {i}')
                dc_g[v] = i

        ans = sum(s(dc_g[i]) for i in range(1, max_num + 1))
        return ans

    @timeit
    def solve(self, max_num) -> int:
        if max_num < 63:
            if max_num <= 50:
                return self.solve_under_63(max_num)
            else:
                ans = self.solve_under_63(50)
                ans += self.solve_above_50_under_63(max_num)
            return ans
        ans = self.solve_under_63(50)
        ans += self.solve_above_50_under_63(62)
        ans += sum(self.g_large_digit_sum(i) for i in range(63, max_num + 1))
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
        self.assertEqual(19846950, self.problem.solve(100))

    def test_150_solution(self):
        self.assertEqual(8184523820510, self.problem.solve(150))


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
# g(56) = 12245556666799999999999 -> 11 nine's
# g(57) = 123345556666799999999999 -> 11 nine's
# g(58) = 1333579999999999999999999  -> 19 nine's
# g(59) = 122456679999999999999999999999  -> 22 nine's
# g(60) = 1233456679999999999999999999999  -> 22 nine's
# g(61) = 13444667779999999999999999999999  -> 22 nine's
# g(62) = 12245555588888999999999999999999999999999  -> 27 nine's
# g(63) = 123345555588888999999999999999999999999999  -> 27 nine's
# g(64) = 134445555689999999999999999999999999999999999999999999999999999999  -> 55 nine's
# g(65) = 1223334444555668888889999999999999999999999999999999999999999999999999999999999999999999999999999999999 -> 82 nine's
# g(66) = 123345556668899999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
# g(67) = 13444556666888888899999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
# g(68) = 1223334444566666888999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
# ...
# g(150) = 1233456666668888888899999... {in total: 192,901,234,567 nines}
