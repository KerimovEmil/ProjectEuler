"""
PROBLEM
By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains eighteen rectangles.

Although there exists no rectangular grid that contains exactly two million rectangles, find the area of the grid with
the nearest solution.

ANSWER: 2772
Solve time: ~2ms
"""
from util.utils import timeit
import unittest


class Problem85:
    def __init__(self):
        pass

    @staticmethod
    def num_of_rect(m, n):
        """
        Pick any 2 line from one set and any 2 line from the second set. These four will make a particular rectangle.
        therefore for (mxn) rectangle:
        number of rectangles = (m+1 choose 2) * (n+1 choose 2)
        e.g. r(3,2) = (4 choose 2) * (3 choose 2) = 4*3/2 * 3 = 2*9 = 18
        (m+1 choose 2) * (n+1 choose 2) = (m+1) * m / 2 * (n+1)*n/2 =  (m+1)*m*(n+1)*n/4
        """
        return (m+1)*m*(n+1)*n // 4

    @staticmethod
    def area(m, n):
        return m*n

    @timeit
    def solve(self, target=2000000):

        #  (m+1)*m*(n+1)*n/4 = 2,000,000
        #  r(m, n) = (m+1)*m*(n+1)*n = 8,000,000
        #  m^2 * n^2 < r(m, n) < (m+1)^2 * (n+1)^2
        #  m * n < 2828.4 < (m+1) * (n+1)

        # if m=n:
        # n^2 < 2828.4 < (n + 1)^2
        # n < 53.18 < (n + 1)
        # n = 53

        sample_n = int((target*4)**0.25)
        max_n = 2*sample_n

        min_distance = self.num_of_rect(sample_n, sample_n)
        area = sample_n**2

        for m in range(1, sample_n):
            for n in range(sample_n, max_n):
                distance = abs(self.num_of_rect(m, n) - target)
                if distance < min_distance:
                    min_distance = distance
                    area = m*n

        return area


class Solution85(unittest.TestCase):
    def setUp(self):
        self.problem = Problem85()

    def test_solution(self):
        self.assertEqual(2772, self.problem.solve(target=2000000))


if __name__ == '__main__':
    unittest.main()
