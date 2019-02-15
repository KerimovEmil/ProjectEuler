from util.utils import timeit
import unittest


class Problem3:
    def __init__(self, num):
        self.num = num

    @staticmethod
    def prime_factors(num):
        n = num
        factors = []
        while not n % 2:
            n /= 2
            factors.append(2)

        sqrt = int(n ** 0.5 // 1)
        for i in range(3, sqrt + 1, 2):
            while not n % i:
                n /= i
                factors.append(i)

        return factors

    @timeit
    def solve(self):
        pf = self.prime_factors(self.num)
        return max(pf)


class Solution3(unittest.TestCase):
    def setUp(self):
        self.problem = Problem3(600851475143)

    def test_solution(self):
        self.assertEqual(6857, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
