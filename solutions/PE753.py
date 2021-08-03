from util.utils import timeit
import unittest
from primesieve import primes


class Problem753:
    def __init__(self, max_p):
        self.dc = self.create_dict(max_p)
        self.max_p = max_p

    def given_p(self, p: int) -> int:
        if p % 3 != 1:
            return (p-1) * (p-2)
        else:
            return self.given_p_3(p)

    def given_p_3(self, p: int) -> int:
        """
        Only called when p%3 == 1.
        Returns (p-1)* number of solutions to (a^3 + 1 = c^3). This is equal to p + a - 8
        Where a is uniquely defined as
        4p = a^2 + 27*b^2, a==1 mod 3
        Note that this only works when p==1 mod 3
        See paper here: http://matwbn.icm.edu.pl/ksiazki/aa/aa37/aa3718.pdf
        """
        return (self.dc[p]+p-8)*(p-1)

    @staticmethod
    def create_dict(max_p):
        """
        Create dictionary of unique values of a for each p (p==1 mod 3), such that
         4p = a^2 + 27b^2, and a==1 mod 3
         """
        max_b = int((4*max_p//27)**0.5) + 10
        max_a = int(((4*max_p)**0.5)) + 10

        x = (-max_a) % 3
        if x == 2:
            max_a += 1
        if x == 0:
            max_a += 2

        assert (-max_a) % 3 == 1

        dc = {}
        for a in range(-max_a, max_a, 3):  # a == 1 mod 3
            for b in range(1, max_b):
                p4 = a ** 2 + 27 * (b ** 2)
                if p4 % 4 == 0:
                    dc[p4 // 4] = a
        return dc

    @timeit
    def solve(self, max_p: int = None) -> int:
        if max_p is None:
            max_p = self.max_p

        ans = sum((p-1)*(p-2) for p in primes(max_p) if p % 3 != 1)

        mod_3_1_primes = (p for p in primes(max_p) if p % 3 == 1)

        ans += sum(self.given_p_3(p) for p in mod_3_1_primes)
        return ans


class Solution753(unittest.TestCase):
    def setUp(self):
        self.problem = Problem753(max_p=6000000)

    def test_specific_p(self):
        with self.subTest('testing p=5'):
            self.assertEqual(12, self.problem.given_p(5))
        with self.subTest('testing p=7'):
            self.assertEqual(0, self.problem.given_p(7))

    def test_solution(self):
        self.assertEqual(4714126766770661630, self.problem.solve())
        self.assertEqual(59762, self.problem.solve(100))


if __name__ == '__main__':
    unittest.main()

