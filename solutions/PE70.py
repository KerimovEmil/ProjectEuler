"""
PROBLEM

Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine the number of positive numbers
 less than or equal to n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine
 and relatively prime to nine, φ(9)=6.
The number 1 is considered to be relatively prime to every positive number, so φ(1)=1.

Interestingly, φ(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which φ(n) is a permutation of n and the ratio n/φ(n) produces a minimum.

ANSWER: 8319823
Solve time ~410 ms
"""

from util.utils import timeit
import unittest
from primesieve import primes

# n/phi(n) will be maximized for n = prime, which would be p/(p-1).
# however, p-1 can never be a permutation of p, so the next best thing is to try numbers which are the product of
# two primes.
# therefore, if n = p1*p1 then phi(p1*p2) = (p1-1)*(p2-1), and n/phi(n) = p1/(p1-1) * p2/(p2-1)
# also n/phi(n) = (1 - 1/p1) * (1 - 1/p2). Therefore the bigger p1 and p2, the better.


def is_permutation(a: int, b: int) -> bool:
    """Returns boolean if a and b are permutations of each other."""
    s_a, s_b = str(a), str(b)
    if set(s_a) != set(s_b):
        return False
    if len(s_a) != len(s_b):
        return False
    return sorted(list(s_a)) == sorted(list(s_b))


class Problem70:
    def __init__(self, max_n: int, debug_mode: bool = False):
        self.max_n = max_n
        self.debug_mode = debug_mode

    @timeit
    def solve(self):

        ls_p = list(primes(2*(self.max_n**0.5)))
        best_n = None
        min_ratio = 1000
        for p1 in ls_p:
            for p2 in ls_p:
                n = p1 * p2
                if n > self.max_n:
                    break
                phi = (1 - p1) * (1 - p2)
                if n / phi < min_ratio and is_permutation(n, phi):
                    min_ratio = n / phi
                    best_n = n
                    if self.debug_mode:
                        print(f'best n: {best_n}, min_ratio: {min_ratio}, phi: {phi}')

        return best_n


class Solution70(unittest.TestCase):
    def setUp(self):
        self.problem = Problem70(max_n=int(1e7))

    def test_solution(self):
        # best n: 8319823, min_ratio: 1.0007090511248113, phi: 8313928
        self.assertEqual(8319823, self.problem.solve())


if __name__ == '__main__':
    unittest.main()


