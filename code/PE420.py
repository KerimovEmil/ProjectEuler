"""
PROBLEM

A positive integer matrix is a matrix whose elements are all positive integers.
Some positive integer matrices can be expressed as a square of a positive integer matrix in two different ways.
Here is an example:

(40, 12 ; 48,40)=(2, 3 ; 12, 2)^2=(6, 1 ; 4,6)^2
We define F(N) as the number of the 2x2 positive integer matrices which have a trace less than N and which can be
expressed as a square of a positive integer matrix in two different ways.
We can verify that F(50) = 7 and F(1000) = 1019.

Find F(10^7).

ANSWER:
???
Solve time ~  seconds
"""

from util.utils import timeit, sieve
import unittest


# --------------------------------------------------------
# a:28, d:76, b:24, c:72, bc:1728, det_pos:12.0, det_neg:8.0
# ai:4.0, di:8.0, bi:2.0, ci:6.0
# ai:1.0, di:7.0, bi:3.0, ci:9.0

def is_square(n):
    return abs(int(n**0.5) - n**0.5) < 1e-13


def is_int(n):
    return abs(n - int(n)) < 1e-13


class Problem420:
    def __init__(self, n, debug=False):
        self.n = n
        self.count = 0
        self.debug = debug
        # self.solution_set = set()

    @timeit
    def solve(self):
        # dc_factors = {q: [i for i in range(2, int(q**0.5) + 1) if q % i == 0] for q in range(1, (self.n//2)**2)}
        # print("Finished constructing factors")
        for a in range(2, self.n//2):  # a <= d
            for d in range(a, self.n - a):
                # for delta in range(1, int(min(a, d))):
                for delta in range(1, a):
                    det_pos = (a + d + 2*delta)**0.5
                    if not is_int(det_pos):
                        continue
                    else:
                        det_pos = int(det_pos)
                    det_neg = (a + d - 2*delta)**0.5
                    if not is_int(det_neg):
                        continue
                    else:
                        det_neg = int(det_neg)

                    if (a + delta) % det_pos != 0:
                        continue
                    if (d + delta) % det_pos != 0:
                        continue
                    if (a - delta) % det_neg != 0:
                        continue
                    if (d - delta) % det_neg != 0:
                        continue

                    bc = int(a*d - delta**2)
                    if bc % (det_pos**2) != 0:
                        continue
                    # for b in dc_factors[bc]:
                    #   c = bc // b
                    # det_pos is the bigger of det_pos and det_neg
                    for i in range(det_pos, int(bc**0.5)+1, det_pos):  # todo change this up
                        if bc % i == 0:  # c >= b
                            b = i
                            c = int(bc/i)
                        else:
                            continue

                        if b % det_pos != 0:
                            continue
                        if c % det_pos != 0:
                            continue
                        if b % det_neg != 0:
                            continue
                        if c % det_neg != 0:
                            continue

                        # self.solution_set.add(((a_pos, b_pos, c_pos, d_pos), (a_neg, b_neg, c_neg, d_neg)))
                        self.count += 1
                        if b != c:
                            # self.solution_set.add(((a_pos, c_pos, b_pos, d_pos), (a_neg, c_neg, b_neg, d_neg)))
                            self.count += 1
                        if a != d:
                            # self.solution_set.add(((d_pos, b_pos, c_pos, a_pos), (d_neg, b_neg, c_neg, a_neg)))
                            self.count += 1
                        if b != c and a != d:
                            # self.solution_set.add(((d_pos, c_pos, b_pos, a_pos), (d_neg, c_neg, b_neg, a_neg)))
                            self.count += 1
                        if self.debug:
                            a_neg = (a - delta) // det_neg
                            d_neg = (d - delta) // det_neg
                            d_pos = (d + delta) // det_pos
                            a_pos = (a + delta) // det_pos
                            b_pos = b // det_pos
                            c_pos = c // det_pos
                            b_neg = b // det_neg
                            c_neg = c // det_neg
                            print("--------------------------------------------------------")
                            print(f"a:{a}, d:{d}, b:{b}, c:{c}, bc:{bc}, det_pos:{det_pos}, det_neg:{det_neg}, delta:{delta}")
                            print(f"a_pos:{a_pos}, d_pos:{d_pos}, b_pos:{b_pos}, c_pos:{c_pos}")
                            print(f"a_neg:{a_neg}, d_neg:{d_neg}, b_neg:{b_neg}, c_neg:{c_neg}")
                            print(f"count: {self.count}")
                            # if a_pos*d_pos != b_neg*c_neg and a==d:
                            #     print("HHHHHHHH")
                            # if a_neg*d_neg != b_pos*c_pos and a==d:
                            #     print("HHHHHHHH2")
    #                     if self.count != len(self.solution_set):
    #                         print("HERE")
    #                         print(len(self.solution_set))
        # print(len(self.solution_set))
        return self.count

    @timeit
    def simple_solve(self):
        for a in range(1, self.n//2):
            for bc2 in range(1, a):
                lamb_1 = a + bc2
                lamb_2 = a - bc2
                if is_square(lamb_1) and is_square(lamb_2):
                    self.count += 1
                    print(f"a:{a}, d:{a}")

        return self.count

    @timeit
    def solve_hermitian(self):
        # Solve for cases of A = D and B = C
        for a in range(2, self.n // 2):
            for delta in range(1, a):
                det_pos = (2*a + 2 * delta) ** 0.5
                if not is_int(det_pos):
                    continue
                else:
                    det_pos = int(det_pos)
                det_neg = (2*a - 2 * delta) ** 0.5
                if not is_int(det_neg):
                    continue
                else:
                    det_neg = int(det_neg)

                if (a + delta) % det_pos != 0:
                    continue
                if (a - delta) % det_neg != 0:
                    continue

                bc = int(a * a - delta ** 2)
                if bc % (det_pos ** 2) != 0:
                    continue
                if is_int(bc**0.5):
                    b = int(bc**0.5)
                    if b % det_pos != 0:
                        continue
                    if b % det_neg != 0:
                        continue
                    self.count += 1
                    if self.debug:
                        a_neg = (a - delta) // det_neg
                        d_neg = (a - delta) // det_neg
                        d_pos = (a + delta) // det_pos
                        a_pos = (a + delta) // det_pos
                        b_pos = b // det_pos
                        c_pos = b // det_pos
                        b_neg = b // det_neg
                        c_neg = b // det_neg
                        print("--------------------------------------------------------")
                        print(
                            f"a:{a}, d:{a}, b:{b}, c:{b}, bc:{bc}, det_pos:{det_pos}, det_neg:{det_neg}, delta:{delta}")
                        print(f"a_pos:{a_pos}, d_pos:{d_pos}, b_pos:{b_pos}, c_pos:{c_pos}")
                        print(f"a_neg:{a_neg}, d_neg:{d_neg}, b_neg:{b_neg}, c_neg:{c_neg}")
                        print(f"count: {self.count}")
    #                     if self.count != len(self.solution_set):
    #                         print("HERE")
    #                         print(len(self.solution_set))
        # print(len(self.solution_set))
        return self.count


class Solution420(unittest.TestCase):
    def setUp(self):
        self.problem = Problem420(n=50)

    def test_solution(self):
        self.assertEqual(7, Problem420(n=50, debug=True).solve())

    def test_solution_herm(self):
        self.assertEqual(177, Problem420(n=1000, debug=True).solve_hermitian())

    # def test_solution_herm2(self):
    #     self.assertEqual(177, Problem420(n=10000000, debug=True).solve_hermitian())

    def test_solution2(self):
        self.assertEqual(1019, Problem420(n=1000, debug=True).solve())
    #
    # def test_solution3(self):
    #     self.assertEqual(None, Problem420(n=10000000, debug=True).solve())


if __name__ == '__main__':
    unittest.main()



# --------------------------------------------------------
# a:496, d:304, b:96, c:1440, bc:138240, det_pos:32.0, det_neg:24.0, delta:112
# ai:19.0, di:13.0, bi:3.0, ci:45.0
# ai:16.0, di:8.0, bi:4.0, ci:60.0
# count: 1523
# --------------------------------------------------------
# a:496, d:304, b:288, c:480, bc:138240, det_pos:32.0, det_neg:24.0, delta:112
# ai:19.0, di:13.0, bi:9.0, ci:15.0
# ai:16.0, di:8.0, bi:12.0, ci:20.0
# count: 1527

import sympy

correct_matrix = sympy.Matrix([[496, 96], [1440, 304]])
sympy.Matrix([[19, 3], [45, 13]])**2
sympy.Matrix([[16, 4], [60, 8]])**2

# change b and c
correct_matrix = sympy.Matrix([[496, 1440], [96, 304]])
sympy.Matrix([[19, 45], [3, 13]])**2
sympy.Matrix([[16, 60], [4, 8]])**2

# change a and d
correct_matrix = sympy.Matrix([[304, 96], [1440, 496]])
sympy.Matrix([[13, 3], [45, 19]])**2
sympy.Matrix([[8, 4], [60, 16]])**2

# change a and d and change b and c
correct_matrix = sympy.Matrix([[304, 1440], [96, 496]])
sympy.Matrix([[13, 45], [3, 19]])**2
sympy.Matrix([[8, 60], [4, 16]])**2
