from util.utils import timeit
import unittest


class Problem1:
    def __init__(self, limit):
        self.limit = limit

    @timeit
    def solve(self):
        gen = (i for i in range(1, self.limit) if not (i % 3 and i % 5))
        return sum(gen)


class Solution1(unittest.TestCase):
    def setUp(self):
        self.problem = Problem1(1000)

    def test_solution(self):
        self.assertEqual(233168, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
