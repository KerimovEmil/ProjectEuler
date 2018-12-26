from util.utils import timeit
import unittest


class Problem2:
    def __init__(self, max):
        self.max = max

    @staticmethod
    def fib(max):
        n1 = 1
        n2 = 2
        yield n1
        while n2 < max:
            n1, n2 = n2, n1 + n2
            yield n1

    @timeit
    def solve(self):
        gen = self.fib(self.max)
        gen_even = (x for x in gen if not x % 2)
        return sum(gen_even)


class Solution2(unittest.TestCase):
    def setUp(self):
        self.problem = Problem2(4000000)

    def test_solution(self):
        self.assertEqual(4613732, self.problem.solve())


if __name__ == '__main__':
    unittest.main()