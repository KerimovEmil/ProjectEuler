"""
When (1+sqrt(7)) is raised to an integral power, n, we always get a number of the form (a + b*sqrt(7)).
We write (a + b*sqrt(7))^n = a(n) + b(n) * sqrt(7)

For a given number x we define g(x) to be the smallest positive integer n such that:
a(n) == 1 mod x
b(n) == 0 mod x
and g(x) = 0 if there is no such value of n. For example, g(3) = 0, g(5) = 12.

Further define
G(N) = sum_{x=2}^{N} g(x)

You are given G(100) = 28891 and G(1000) = 13131583

Find G(1000000)

ANSWER:
Solve time: __ seconds
"""

from util.utils import timeit
import unittest


class FieldExtensionD:
    """Numbers of the form a + b*sqrt(D) for a,b integers"""

    def __init__(self, x: int, y: int, d: int):
        self.x = x
        self.y = y
        self.d = d

    def conjugate(self):
        return FieldExtensionD(x=self.x, y=-self.y, d=self.d)

    def norm(self):
        return self * self.conjugate()

    def __mul__(self, other):
        assert self.d == other.d
        f = self.x * other.x + self.y * self.d * other.y
        s = self.y * other.x + self.x * other.y
        return FieldExtensionD(x=f, y=s, d=self.d)

    def __mod__(self, other):
        return FieldExtensionD(x=self.x % other, y=self.y % other, d=self.d)

    def __pow__(self, power: int):
        # power is always greater than 0
        if power <= 0:
            raise NotImplementedError('Negative powers are not implemented.')
        result = self
        num_to_mult = power - 1
        while num_to_mult > 0:
            result *= self
            num_to_mult -= 1
        return result

    def __str__(self):
        if self.y == 0:
            return f'{self.x}'
        if abs(self.y) == 1:
            if self.y > 0:
                return f'{self.x} + sqrt({self.d})'
            else:
                return f'{self.x} - sqrt({self.d})'
        if self.y < 0:
            return f'{self.x} - {abs(self.y)}*sqrt({self.d})'
        return f'{self.x} + {self.y}*sqrt({self.d})'

    def __repr__(self):
        return str(self)

    def print_generator(self):
        soln = str(self)
        return f"({soln})^k"

    def __eq__(self, other):
        if isinstance(other, FieldExtensionD):
            return (self.x == other.x) and (self.y == other.y) and (self.d == other.d)
        elif isinstance(other, int):
            return (self.x == other) and (self.y == 0)
        else:
            raise NotImplementedError

    def __hash__(self):
        return hash((self.x, self.y, self.d))


def g(n, max_n=10000):
    if n % 3 == 0:
        return 0
    if n % 2 == 0:
        return 0
    start = FieldExtensionD(1, 1, 7)
    x = FieldExtensionD(1, 1, 7)

    for i in range(max_n):
        start = (start * x) % n
        if start.x == 1 and start.y == 0:
            return i + 2


class Problem752:
    def __init__(self):
        pass

    @timeit
    def solve(self, n, max_n=10000):
        return sum(g(i, max_n) for i in range(2, n + 1))


class Solution752(unittest.TestCase):
    def setUp(self):
        self.problem = Problem752()

    def test_solution_small_1(self):
        self.assertEqual(28891, self.problem.solve(n=100, max_n=10000))

    # def test_solution_small_2(self):
    #     self.assertEqual(13131583, self.problem.solve(n=1000, max_n=1000000))


if __name__ == '__main__':
    unittest.main()

