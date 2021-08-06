# ANSWER
# 15955822

import sys

from util.utils import ChineseRemainderTheorem, EulerNumber


# 77777777 = 7 x 11 x 73 x 101 x 137


class Problem330:
    def solve(self):
        print(self.get(10 ** 9))

    def get(self, n):
        prime_list = [7, 11, 73, 101, 137]
        A_mod_list = []
        b_mod_list = []
        for prime in prime_list:
            print("curr prime =>", prime)
            euler_number = EulerNumber(prime)
            n_mod = (n - prime) % (prime * (prime - 1)) + prime if n >= prime else n
            print("n_mod =>", n_mod)
            A_mod, B_mod = euler_number.get(n_mod)
            print("A(n) and B(n) mod", prime, "=>", A_mod, B_mod)
            A_mod_list.append(A_mod)
            b_mod_list.append(B_mod)
        theorem = ChineseRemainderTheorem()
        A = theorem.solve(A_mod_list, prime_list)
        B = theorem.solve(b_mod_list, prime_list)
        print("A(n) mod 77777777 =>", A)
        print("B(n) mod 77777777 =>", B)
        return (A + B) % 77777777


def main():
    problem = Problem330()
    problem.solve()


if __name__ == '__main__':
    sys.exit(main())
