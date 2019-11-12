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
??? (145159332)
Solve time ~  seconds
"""

from util.utils import timeit, sieve
import unittest
from math import gcd

# https://en.wikipedia.org/wiki/Square_root_of_a_2_by_2_matrix
# https://projecteuler.net/problem=420

# --------------------------------------------------------
# a:28, d:76, b:24, c:72, bc:1728, det_pos:12.0, det_neg:8.0
# ai:4.0, di:8.0, bi:2.0, ci:6.0
# ai:1.0, di:7.0, bi:3.0, ci:9.0


def lcm(x, y):
    return x*y // gcd(x, y)


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
        return self.count

    @timeit
    def solve_trace(self):
        # count: 852240, trace: 148228

        # ls_possible_delta = [i ** 2 for i in range(1, int(self.n ** 0.5))]
        for trace in range(2, self.n):
            for delta in range(1, trace//2 + trace % 2):  # (trace-2del >0),  trace > 2 del, del <trace/2
                det_pos = (trace + 2 * delta) ** 0.5  # todo improve this, combine pos + neg search
                if not is_int(det_pos):
                    continue
                else:
                    det_pos = int(det_pos)
                det_neg = (trace - 2 * delta) ** 0.5
                if not is_int(det_neg):
                    continue
                else:
                    det_neg = int(det_neg)
                det_pos_neg = lcm(det_pos, det_neg)

                # a = -delta + k1*det_pos = delta + k2*det_neg
                for a in range(delta + det_neg, trace // 2 + 1, det_neg):  # a - delta > 0
                    d = trace - a  # checks on d are true automatically since (a+delta + d+delta)/det_pos = int
                    if (a + delta) % det_pos != 0:
                        # print("a_check")
                        continue
                    # if (a - delta) % det_neg != 0:
                    #     print("a_check")
                    #     continue

                    bc = int(a * d - delta ** 2)
                    # if bc % (det_pos_neg ** 2) != 0:  # bc check not needed
                    #     print("bc_hello")
                    #     continue

                    bc_prime = bc // (det_pos_neg ** 2)
                    bc_count = 0
                    bc_limit = int(bc_prime ** 0.5)
                    if is_int(bc_prime ** 0.5):  # b == c
                        bc_count += 1
                    else:
                        bc_limit += 1
                    bc_count += 2 * sum(bc_prime % i == 0 for i in range(1, bc_limit))

                    if a != d:
                        self.count += 2 * bc_count
                    else:
                        self.count += bc_count

                    if self.debug:
                        # b = i * det_pos_neg
                        b = 0
                        # c = j * det_pos_neg
                        c = 0
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
                        print(f'bc_prime:{bc_prime}, bc_limit:{bc_limit}')
                        print(f"a_pos:{a_pos}, d_pos:{d_pos}, b_pos:{b_pos}, c_pos:{c_pos}")
                        print(f"a_neg:{a_neg}, d_neg:{d_neg}, b_neg:{b_neg}, c_neg:{c_neg}")
                        print(f"count: {self.count}, trace:{trace}")
        return self.count


class Solution420(unittest.TestCase):
    def setUp(self):
        self.problem = Problem420(n=50)

    def test_solution(self):
        self.assertEqual(7, Problem420(n=50, debug=True).solve())

    # def test_solution_herm(self):
    #     self.assertEqual(177, Problem420(n=1000, debug=True).solve_hermitian())

    def test_solution_trace(self):
        self.assertEqual(1019, Problem420(n=1000, debug=True).solve_trace())

    # def test_solution2(self):
    #     self.assertEqual(1019, Problem420(n=1000, debug=True).solve())

    def test_solution_trace3(self):
        self.assertEqual(16021, Problem420(n=7000, debug=True).solve_trace())

    # def test_solution_trace4(self):
    #     self.assertEqual(None, Problem420(n=10000000, debug=True).solve_trace())


if __name__ == '__main__':
    unittest.main()
