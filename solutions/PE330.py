"""
PROBLEM

An infinite sequence of real numbers a(n) is defined for all integers n as follows:
a(n) = 1 if n<0
a(n) = sum_{i=1}^{inf} a(n-i)/(i!)  if n>=0

For example,
a(0) = 1/1! + 1/2! + 1/3! + ... = e-1
a(1) = (e-1)/1! + 1/2! + 1/3! + ... = 2e-3
a(2) = (2e-3)/1! + (e-1)/2! + 1/3! + ... = (7/2)e-6

with e being Euler's constant.

It can be shown that a(n) is of the form (A(n)e + B(n))/(n!)
for integers A(n) and B(n).

For example,
a(10) = (328161643 e - 652694486)/(10!)

Find A(10^9) + B(10^9) and give your answer mod 77 777 777.

ANSWER: 15955822
Solve time ~268 seconds
"""
import unittest
from util.utils import EulerNumber
from util.crt import ChineseRemainderTheorem


class Problem330:
    def __init__(self, prime_list, n):
        self.n = n
        self.prime_list = prime_list

    def solve(self):
        A_mod_list = []
        b_mod_list = []
        for prime in self.prime_list:
            print("current prime =>", prime)
            euler_number = EulerNumber(prime)
            n_mod = (self.n - prime) % (prime * (prime - 1)) + prime if self.n >= prime else self.n
            print("n_mod =>", n_mod)
            A_mod, B_mod = euler_number.get(n_mod)
            print("A(n) and B(n) mod", prime, "=>", A_mod, B_mod)
            A_mod_list.append(A_mod)
            b_mod_list.append(B_mod)
        A = ChineseRemainderTheorem(A_mod_list, self.prime_list).solve()
        B = ChineseRemainderTheorem(b_mod_list, self.prime_list).solve()
        print("A(n) mod 77777777 =>", A)
        print("B(n) mod 77777777 =>", B)
        return (A + B) % 77777777


class Solution330(unittest.TestCase):
    def setUp(self):
        # 77777777 = 7 x 11 x 73 x 101 x 137
        self.problem = Problem330(prime_list=[7, 11, 73, 101, 137], n=10**9)

    def test_solution(self):
        self.assertEqual(15955822, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
