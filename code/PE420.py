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
145159332
Solve time ~  seconds
"""

from util.utils import timeit
import unittest
from math import gcd

# https://en.wikipedia.org/wiki/Square_root_of_a_2_by_2_matrix
# https://projecteuler.net/problem=420


def lcm(x, y):
    return x*y // gcd(x, y)


def is_int(n):
    return abs(n - int(n)) < 1e-13


class Problem420:
    def __init__(self, n, debug=False):
        self.n = n
        self.count = 0
        self.debug = debug

    @timeit
    def solve(self):
        # det_neg < det_pos
        # det_neg^2 + det_pos^2 = 2*trace < 2*n
        # det_neg < sqrt(2*n)
        # det_pos < sqrt(2*n - det_neg^2)
        for det_neg in range(1, int((2*self.n) ** 0.5)):
            d_pos_limit = (2*self.n - det_neg ** 2)**0.5
            if is_int(d_pos_limit):
                d_pos_limit = int(d_pos_limit)
            else:
                d_pos_limit = int(d_pos_limit) + 1

            for det_pos in range(det_neg+2, d_pos_limit, 2):
                trace = (det_pos**2 + det_neg**2)//2
                # delta = (det_pos**2 - det_neg**2)//2
                delta = int((trace - det_neg**2)/2)

                det_pos_neg = lcm(det_pos, det_neg)

                # a = -delta + k1*det_pos = delta + k2*det_neg
                for a in range(delta + det_neg, trace // 2 + 1, det_neg):  # a - delta > 0
                    if (a + delta) % det_pos != 0:
                        continue

                    d = trace - a  # checks on d are true automatically since (a+delta + d+delta)/det_pos = int
                    bc = int(a * d - delta ** 2)  # bc check not needed

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
                        a_neg = (a - delta) // det_neg
                        d_neg = (d - delta) // det_neg
                        d_pos = (d + delta) // det_pos
                        a_pos = (a + delta) // det_pos
                        print("--------------------------------------------------------")
                        print(f"a:{a}, d:{d}, bc:{bc}, det_pos:{det_pos}, det_neg:{det_neg}, delta:{delta}")
                        print(f'bc_prime:{bc_prime}, bc_limit:{bc_limit}')
                        print(f"a_pos:{a_pos}, d_pos:{d_pos}")
                        print(f"a_neg:{a_neg}, d_neg:{d_neg}")
                        print(f"count: {self.count}, trace:{trace}")
        return self.count

    @timeit
    def solve_trace(self):
        for trace in range(2, self.n):  # 2*trace = det_neg^2 + det_pos^2
            # if trace is even then deg_neg must be even
            # if trace is off then deg_neg must be odd
            trace_even = 1 - trace % 2
            for det_neg in range(1 + trace_even, int((trace - 2) ** 0.5)+1, 2):
                delta = int((trace - det_neg**2)/2)

                det_pos = (trace + 2 * delta) ** 0.5
                if not is_int(det_pos):
                    continue
                else:
                    det_pos = int(det_pos)

                det_pos_neg = lcm(det_pos, det_neg)

                # a = -delta + k1*det_pos = delta + k2*det_neg
                for a in range(delta + det_neg, trace // 2 + 1, det_neg):  # a - delta > 0
                    if (a + delta) % det_pos != 0:
                        continue

                    d = trace - a  # checks on d are true automatically since (a+delta + d+delta)/det_pos = int
                    bc = int(a * d - delta ** 2)  # bc check not needed

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
                        a_neg = (a - delta) // det_neg
                        d_neg = (d - delta) // det_neg
                        d_pos = (d + delta) // det_pos
                        a_pos = (a + delta) // det_pos
                        print("--------------------------------------------------------")
                        print(f"a:{a}, d:{d}, bc:{bc}, det_pos:{det_pos}, det_neg:{det_neg}, delta:{delta}")
                        print(f'bc_prime:{bc_prime}, bc_limit:{bc_limit}')
                        print(f"a_pos:{a_pos}, d_pos:{d_pos}")
                        print(f"a_neg:{a_neg}, d_neg:{d_neg}")
                        print(f"count: {self.count}, trace:{trace}")
        return self.count


class Solution420(unittest.TestCase):
    def setUp(self):
        self.problem = Problem420(n=50)

    def test_solution(self):
        # self.assertEqual(7, Problem420(n=50, debug=True).solve_trace())
        self.assertEqual(7, Problem420(n=50, debug=True).solve())

    def test_solution_2(self):
        # self.assertEqual(1019, Problem420(n=1000, debug=True).solve_trace())
        self.assertEqual(1019, Problem420(n=1000, debug=True).solve())

    def test_solution_3(self):
        # self.assertEqual(16021, Problem420(n=7000, debug=True).solve_trace())
        self.assertEqual(16021, Problem420(n=7000, debug=True).solve())

    def test_solution_4(self):
        # self.assertEqual(145159332, Problem420(n=10000000, debug=True).solve_trace())
        self.assertEqual(145159332, Problem420(n=10000000, debug=True).solve())


if __name__ == '__main__':
    unittest.main()
