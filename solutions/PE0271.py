from util.utils import timeit
import unittest

from util.utils import euler_totient_function

# 13082761331670030 = 2*3*5*7*11*13*17*19*23*29*31*37*41*43

# https://oeis.org/A066498

# 91 = 7*13
# 91: 9, 16, 22, 29, 53, 74, 79, 81
# 7: 2, 4
# 13: 3, 9

# if x^3 = 1 mod (n*k) then x^3 = 1 mod n and x^3 = 1 mod k

# ChineseRemainderTheorem(a_list=[2, 3], n_list=[7, 13]).solve() -> 16
# ChineseRemainderTheorem(a_list=[2, 9], n_list=[7, 13]).solve() -> 9
# ChineseRemainderTheorem(a_list=[4, 3], n_list=[7, 13]).solve() -> 81
# ChineseRemainderTheorem(a_list=[4, 9], n_list=[7, 13]).solve() -> 74

# ChineseRemainderTheorem(a_list=[8, 3], n_list=[7, 13]).solve() -> 29
# ChineseRemainderTheorem(a_list=[2, 27], n_list=[7, 13]).solve() -> 79

# b * pow(p % q, -1, q) * p % (p * q)


def f(n):
    s = 0
    for x in range(max(2, int(n ** (1 / 3))), n):
        if x ** 3 % n == 1:
            s += x
            # print(f'x={x}, s={s}')
    return s


def g(r):
    for i in range(2, r + 1):
        s = f(i)
        if s != 0:
            p = euler_totient_function(i)
            if p == s:  # todo: if i is a prime of the form 6m+1, then p=s
                print(f'p=s={s} for n={i}')
            # else:
            #     print(f'p={p}, s={s} for n={i}')


class Problem271:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution271(unittest.TestCase):
    def setUp(self):
        self.problem = Problem271()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

