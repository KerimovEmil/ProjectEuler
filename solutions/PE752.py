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

from util.utils import timeit, Matrix
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
    sol = FieldExtensionD(1, 0, 7)

    for i in range(2, max_n):
        start = (start * x) % n
        if start == sol:
            return i


# a_{n} + b_{n} √7 = (1+√7)^n = (1+√7) * (1+√7)^n = (1+√7) * (a_{n-1} + b_{n-1} √7)
# a_{n} + b_{n} √7 = (1+√7) * (a_{n-1} + b_{n-1} √7) = (a_{n-1} + 7 b_{n-1}) + (a_{n-1} + b_{n-1}) √7

# a_{n} = a_{n-1} + 7 b_{n-1}
# b_{n} = a_{n-1} + b_{n-1}
# a_1 = b_1 = 1
# [a_{n}, b_{n}] = [[1,7], [1,1]] @ [a_{n-1}, b_{n-1}]
# [a_{n}, b_{n}] = [[1,7], [1,1]]^{n-1} @ [1, 1]


# initial_vec = [1, 1]
initial_vec = Matrix([[1], [1]])

q = Matrix([[1, 7], [1, 1]])
# pow(q, 5, 11) @ initial_vec
pow(q, 5) @ initial_vec

# e.g. g(23) = 176 ->
# (pow(q, 175, mod=23) @ initial_vec) % 23 == Matrix([[1], [0]])


# [[1,7], [1,1]]^2 = [[8, 14], [2, 8]]
# [[1,7], [1,1]]^3 = [[22, 70], [10, 22]]
# [[1,7], [1,1]]^4 = [[92, 224], [32, 92]]
# [[1,7], [1,1]]^5 = [[316, 868], [124, 316]]
# [[1,7], [1,1]]^6 = [[1184, 3080], [440, 1184]]
# [[1,7], [1,1]]^7 = [[4264, 11368], [1624, 4264]]
# [[1,7], [1,1]]^8 = [[15632, 41216], [5888, 15632]]

# b, a = Matrix([[0,1], [0,0]]),  Matrix([[1,0], [1,1]])

# A = [[1,x], [1,1]] = [[1,0], [1,1]] + x*[[0,1], [0,0]] = a+x*b
# [[1,0], [1,1]] * [[1,0], [1,1]] = [[1, 0], [2, 1]] = a^2
# [[0,1], [0,0]] * [[0,1], [0,0]] = [[0, 0], [0, 0]] = b^2 = 0
# [[1,0], [1,1]] * [[0,1], [0,0]] = [[0, 1], [0, 1]] = a*b

# a^n = [[1, 0], [n, 1]]
# b*a*b = b
# b*a^n*b = [[0, n], [0, 0]]
# a^n*b = [[0, 1], [0, n]]
# (a*b*a)^n = 2^{n-1} * [[1, 1], [1, 1]]
# (a*b*a)^n = 2^{n-1} * a*b*a            (eq to b*a^n*b = n*b)
# b*a^n*b = n*b = [[0, n], [0, 0]]
# a^n = a + (n-1) * b.T
# b.T * a = b.T
# a*b = b + b.T * b
# a = I + b.T
# a*b + b*a = 2*b + b.T*b + b.T*b

# A^2 = a^2 + 2*a*b*x + x^2*b^2 = a^2 + x*(a*b + b*a)
# A^3 = a^3 + x*(a*b*a + b*a*a + a*a*b) + x^2*(b)
# A^4 = a^4 + x*(a*b*a*a + b*a*a*a + a*a*b*a + a*a*a*b) + x^2*(b*a + a*b + b*a*a*b)
# A^5 = a^5 + x*(a*b*a*a*a + b*a*a*a*a + a*a*b*a*a + a*a*a*b*a + a*a*a*a*b) + x^2*(b*a*a + a*b*a + b*a*a*b*a + a*b*a*a*b
#       + b*a*a*a*b + a*a*b) + x^3*(b)
# A^6 = a^6 + x*(b*a*a*a*a*a + a*b*a*a*a*a + a*a*b*a*a*a + a*a*a*b*a*a + a*a*a*a*b*a + a*a*a*a*a*b)
#       + x^2*(b*a*a*a + a*b*a*a + a*a*b*a + a*a*a*b + 2*(b*a*a + a*b*a + a*a*b) + 3*(b*a + a*b) + 4*b)
#       + x^3*(4*b + a*b + b*a)

# s_0 = b
# s_1 = b*a + a*b -> [[1, 2], [0, 1]]
# s_2 = b*a*a + a*b*a + a*a*b -> [[3, 3], [1, 3]]
# s_3 = b*a*a*a + a*b*a*a + a*a*b*a + a*a*a*b -> [[6, 4], [4, 6]]
# s_4 = a*b*a*a*a + b*a*a*a*a + a*a*b*a*a + a*a*a*b*a + a*a*a*a*b -> [[10, 5], [10, 10]]
# s_5 = b*a*a*a*a*a + a*b*a*a*a*a + a*a*b*a*a*a + a*a*a*b*a*a + a*a*a*a*b*a + a*a*a*a*a*b -> [[15, 6], [20, 15]]

# s_n = [[(n)(n+1)/2, (n+1)], [(n-1)*n*(n+1)/6, (n)(n+1)/2]]
# s_n = (n+1) * [[n/2, 1], [(n-1)*n/6, n/2]]

# A^1 = a^1 + x*s_0
# A^2 = a^2 + x*s_1
# A^3 = a^3 + x*s_2 + x^2*(s_0)
# A^4 = a^4 + x*s_3 + x^2*(s_1 + 2*s_0)
# A^5 = a^5 + x*s_4 + x^2*(s_2 + 2*s_1 + 3*s_0) + x^3*(s_0)
# A^6 = a^6 + x*s_5 + x^2*(s_3 + 2*s_2 + 3*s_1 + 4*s_0) + x^3*(s_1 + 4*s_0)
# A^7 = a^7 + x*s_6 + x^2*(s_4 + 2*s_3 + 3*s_2 + 4*s_1 + 5*s_0) + x^3*(s_2 + 4*s_1 + 10*s_0) + x^4*(s_0)
# A^8 = a^8 + x*s_7 + x^2*(s_5 + 2*s_4 + 3*s_3 + 4*s_2 + 5*s_1 + 6*s_0) + x^3*(s_3 + 4*s_2 + 10*s_1 + 20*s_0) + x^4*(s_1 + 6*s_0)

# 1,2,3,4,5,... -> n
# 1,4,10,20,... -> n*(n+1)*(n+2)/6
# 1,6,

# s_0*a = b*a
# s_1*a = b*a*a + a*b*a
# s_2*a = b*a*a*a + a*b*a*a + a*a*b*a

# s_0*b = 0
# s_1*b = s_0
# s_1*b = b
# s_2*b = 2*b + a*b
# s_3*b = 3*b + 2*a*b + a*a*b
# s_4*b = 3*a*b + 4*b + 2*a*a*b + a*a*a*b

# dc_s = dict()
# for n in range(20):
# #     dc_s[n] = (n + 1) * Matrix([[n / 2, 1], [((n - 1) * n) / 6, n / 2]])
#     dc_s[n] = Matrix([[(n * (n + 1)) // 2, (n + 1)], [((n - 1) * n*(n + 1)) // 6, (n*(n + 1)) // 2]])

# pow(a, 6) + x * dc_s[5] + x**2 * (dc_s[3] + 2*dc_s[2] + 3*dc_s[1] + 4*dc_s[0]) + x**3 *(dc_s[1] + 4*dc_s[0])
# pow(a, 7) + x * dc_s[6] + x**2 * (dc_s[4] + 2*dc_s[3] + 3*dc_s[2] + 4*dc_s[1] + 5*dc_s[0]) + x**3 *(dc_s[2] + 4*dc_s[1] + 10*dc_s[0]) + x**4 * (dc_s[0])
# pow(a, 8) + x * dc_s[7] + x**2 * (dc_s[5] + 2*dc_s[4] + 3*dc_s[3] + 4*dc_s[2] + 5*dc_s[1] + 6*dc_s[0]) + x**3 *(dc_s[3] + 4*dc_s[2] + 10*dc_s[1] + 20*dc_s[0]) + x**4 * (dc_s[1] + 6*dc_s[0])


class Problem752:
    def __init__(self):
        pass

    def get_an_bn(self, max_n=10000):
        initial_vec = Matrix([[1], [1]])
        q = Matrix([[1, 7], [1, 1]])
        x = Matrix([[1, 7], [1, 1]])

        dc_an = {1: 1}
        dc_bn = {1: 1}
        ls_an_bn = [(1, 1)]

        for n in range(2, max_n):
            x *= q
            an_bn = (x @ initial_vec).entries
            (a,), (b,) = an_bn
            dc_an[n] = a
            dc_bn[n] = b
            ls_an_bn.append((a, b))

        self.dc_an = dc_an
        self.dc_bn = dc_bn
        self.ls_an_bn = ls_an_bn
        print(self.ls_an_bn)

    def g2(self, m):
        if m % 3 == 0:
            return 0
        if m % 2 == 0:
            return 0

        for i, tup in enumerate(self.ls_an_bn):
            a, b = tup
            if a % m == 1 and b % m == 0:
                print(f'{m=}, n={i+2}')
                return i + 2
        print(f'nothing for {m=}')
        return 0

    @timeit
    def solve(self, n, max_n=10000):
        self.get_an_bn(max_n=max_n)
        return sum(self.g2(i) for i in range(2, n + 1))

    @timeit
    def solve0(self, n, max_n=10000):
        return sum(g(i, max_n) for i in range(2, n + 1))


class Solution752(unittest.TestCase):
    def setUp(self):
        self.problem = Problem752()

    def test_solution_small_1(self):
        """G(100) = 28891"""
        self.assertEqual(28891, self.problem.solve(n=100, max_n=10000))
        # self.assertEqual(28891, self.problem.solve0(n=100, max_n=10000))

    def test_solution_small_2(self):
        """G(1000) = 13131583"""
        # self.assertEqual(13131583, self.problem.solve(n=1000, max_n=1000000))
        self.assertEqual(13131583, self.problem.solve0(n=1000, max_n=1000000))


if __name__ == '__main__':
    unittest.main()

# g(2) = 0
# g(3) = 0
# g(5) = 12
# g(7) = 7
# g(11) = 60
# g(13) = 168
# g(17) = 288
# g(19) = 18
# g(23) = 176
# g(29) = 7
# g(31) = 30
# g(37) = 12
# g(41) = 560
# g(43) = 264
# g(47) = 46
# g(53) = 52
# g(59) = 29
# g(61) = 3720
# g(67) = 4488
# g(71) = 5040
# g(73) = 2664
# g(79) = 780
# g(83) = 41
# g(89) = 7920
# g(97) = 1176

# g(5) = 12
# g(7) = 7
# g(11) = 60
# g(5*7) = g(5) * g(7) = 12 * 7 = 84

# g(5^n) = g(5) * 5^(n-1)
# g(7^n) = g(7) * 7^(n-1)
# g(5^2 * 7^2) = g(5) * g(7) * 5 * 7
# g(31^3) = g(31) * 31^2

# g(31*37*41) = 120 * g(31)*g(37)*g(41)
# g(5*7*11) = 12 * g(5)*g(7)*g(11)
# g(13*31*59) = 6 * g(13)*g(31)*g(59)
# g(13*31*59*7) = 42 * g(13)*g(31)*g(59)*g(7)


# 2|m or 3|m -> g(m)=0
# m=5, n=12
# m=7, n=7
# m=11, n=60
# m=13, n=168
# m=17, n=288
# m=19, n=18
# m=23, n=176
# m=25, n=60
# m=29, n=7
# m=31, n=30
# m=35, n=84
# m=37, n=12
# m=41, n=560
# m=43, n=264
# m=47, n=46
# m=49, n=49
# m=53, n=52
# m=55, n=60
# m=59, n=29
# m=61, n=3720
# m=65, n=168
# m=67, n=4488
# m=71, n=5040
# m=73, n=2664
# m=77, n=420
# m=79, n=780
# m=83, n=41
# m=85, n=288
# m=89, n=7920
# m=91, n=168
# m=95, n=36
# m=97, n=1176

# if b_{n} == 0 mod p then b_{n} == 0 mod pq