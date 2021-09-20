"""
The function  is defined for all positive integers as follows:
f(1) = 1
f(2n) = 2f(n)
f(2n + 1) = 2n + 1 + 2f(n) + f(n)/n

It can be proven that f(n) is integer for all values of n.

The function S(n) is defined as S(n) = sum_{i=1 to n} f(i)^2

For example, S(10)=1530 and S(10^2) = 4798445

Find S(10^16). Give your answer modulo 1,000,000,007

ANSWER:

Solve time ~ seconds.
"""

from util.utils import timeit
import unittest
import math

# define h(x) = f(x)/x
# h(2n) = h(n)
# h(2n + 1) = 1 + h(n)

# S(2n) = sum_{i=1 to n} (2i)^2 * h(2i)^2 + sum_{i=0 to n-1} (2i + 1)^2 * h(2i + 1)^2
# S(2n) = 4 * sum_{i=1 to n} i^2 * h(i)^2 + sum_{i=0 to n-1} (2i + 1)^2 * (1 + h(i))^2
# S(2n) = 4 * S(n) + sum_{i=1 to n} (2i + 1)^2 * (1 + h(i))^2 + 1 - (2n + 1)^2 * (1 + h(n))^2
# S(2n) = 1 - (2n + 1)^2 * (1 + h(n))^2 + 4 * S(n) + sum_{i=1 to n} (2i + 1)^2 * (1 + h(i))^2
# S(2n) = 1 - (2n + 1)^2 * (1 + h(n))^2 + 4 * S(n) + sum_{i=1 to n} (4i^2 + 4i + 1) * (1 + 2h(i) + h(i)^2)
# t(n) = 1 - (2n + 1)^2 * (1 + h(n))^2 + sum_{i=1 to n} (4i^2 + 4i + 1)
# S(2n) = t(n) + 4*S(n) + sum_{i=1 to n} (4i^2 + 4i + 1) * (2h(i) + h(i)^2)
# S(2n) = t(n) + 4*S(n) + sum_{i=1 to n} (2i + 1)^2 * h(i)^2 + sum_{i=1 to n} (2i + 1)^2 * 2h(i)

# 10^16 = 2^16 * 5^16


def s3(n, m=1000000007):  # up to 10^6 is fast
    """S(2n) = 1 - (2n + 1)^2 * (1 + h(n))^2 + 4 * S(n) + sum_{i=1 to n} (2i + 1)^2 * (1 + h(i))^2"""

    ans = 1
    if n == 2:
        return 5
    if n == 1:
        return 1

    q = n // 2  # n = 2q + 1

    if n % 2 == 1:  # if n is odd
        pass
    else:  # n is even
        ans -= ((1 + hamming_weight(q)) * (n + 1)) ** 2 % m

    ans += 4 * s3(q) + sum(((2*i + 1) * (1+hamming_weight(i)))**2 for i in range(1, q+1))
    return ans % m

# Even arguments of S
# S(2n) = sum_{i=1 to 2n} f(i)^2
# S(2n) = sum_{i=1 to n} f(2i)^2 + sum_{i=0 to n-1} f(2i + 1)^2
# using f(2n) = 2f(n) and f(2n + 1) = 2n + 1 + 2f(n) + f(n)/n
# S(2n) = sum_{i=1 to n} 4 * f(i)^2 + sum_{i=0 to n-1} (2n + 1 + 2f(n) + f(n)/n)^2
# S(2n) = 4S(n) + sum_{i=0 to n-1} (2n + 1 + 2f(n) + f(n)/n)^2

# note that
# (2n + 1 + 2f(n) + f(n)/n)^2 = (2n + 1 + 2f(n) + f(n)/n) * (2n + 1 + 2f(n) + f(n)/n)
# (2n + 1 + 2f(n) + f(n)/n)^2 = (4n^2 + 2n + 4nf(n) + 2f(n)) + (2n + 1 + 2f(n) + f(n)/n) + ...
# (4nf(n) + 2f(n) + 4f^2(n) + 2f^2(n)/n) + (2f(n) + f(n)/n + 2f(n)^2/n + f(n)^2/n^2)

# (2n + 1 + 2f(n) + f(n)/n)^2 = 4n^2 + 4n + 1 + 8f(n) + 8nf(n) + 2f(n)/n + 4f(n)^2/n + 4f^2(n) + f(n)^2/n^2

# S(2n) = 4S(n) + sum_{i=0 to n-1} (4i^2 + 4i + 1 + 8f(i) + 8if(i) + 2f(i)/i + 4f(i)^2/i + 4f(i)^2 + f(i)^2/i^2)
# S(2n) = 4S(n) + n(4n^2 -1)/3 + sum_{i=0 to n-1} (8f(i) + 8if(i) + 2f(i)/i + 4f(i)^2/i + 4f^2(i) + f(i)^2/i^2)
# S(2n) = 8S(n) - 4f(n)^2 + n(4n^2 -1)/3 + 8 sum_{i=0 to n-1} (f(i)) + 2 sum_{i=0 to n-1} (f(i)/i) ...
#         sum_{i=0 to n-1} (8if(i) + 4f(i)^2/i + f(i)^2/i^2))
# using h(x) = f(x)/x
# S(2n) = 8S(n) - 4f(n)^2 + n(4n^2 -1)/3 + 8sum_{i=0 to n-1} f(i) + 2sum_{i=0 to n-1} h(i) + sum_{i=0 to n-1} h(i)^2 ...
#         sum_{i=0 to n-1} (8if(i) + 4f(i)^2/i)

# Odd arguments of S
# S(2n + 1) = sum_{i=1 to 2n+1} f(i)^2
# S(2n + 1) = sum_{i=1 to n} f(2i)^2 + sum_{i=0 to n} f(2i + 1)^2
# S(2n + 1) = 4S(n) + sum_{i=0 to n} (2i + 1 + 2f(i) + f(i)/i)^2
# S(2n + 1) = 8S(n) + (n+1)(2n+1)(2n+3)/3 + 8sum_{i=0 to n} f(i) + 2sum_{i=0 to n} h(i) + sum_{i=0 to n} h(i)^2 ...
#         sum_{i=0 to n} (8if(i) + 4f(i)^2/i)


def f(n: int) -> int:
    if n < 1:
        raise NotImplementedError
    if n == 1:
        return 1
    if n % 2 == 0:
        return 2*f(n//2)
    else:
        q = n//2  # n = 2q + 1
        return int(n + 2*f(q) + 1/q * f(q))


def s1(n):
    ans = 0
    for i in range(1, n+1):
        ans += f(i)**2
    return ans


def hamming_weight(n: int) -> int:
    """compute the number of 1'st in the binary representation of n"""
    return bin(n).count('1')


def g(n: int) -> int:
    """replicate f(n) but more efficiently"""
    return n*hamming_weight(n)


def s2(n, m=1000000007):  # up to 10^6 is fast
    ans = 0
    for i in range(1, n+1):
        ans += g(i)**2 % m
        ans = ans % m
    return ans


# 01 * 1
# 10 * 1 = 2 * 1
# 11 * 2 = 3 * 2
# 1

class Problem759:
    def __init__(self):
        pass

    @timeit
    def solve(self, n):
        # return s2(n)
        return s3(n)


class Solution759(unittest.TestCase):
    def setUp(self):
        self.problem = Problem759()

    def test_solution_very_small(self):
        self.assertEqual(1530, self.problem.solve(n=10))

    def test_solution_small(self):
        self.assertEqual(4798445, self.problem.solve(n=100))

    def test_solution_1e5(self):
        self.assertEqual(405942229, self.problem.solve(n=int(1e5)))

    # def test_solution_1e6(self):
    #     self.assertEqual(309701254, self.problem.solve(n=int(999999)))


if __name__ == '__main__':
    unittest.main()

# f(n) = sum([i for i in range(int(2**6)) if hamming_weight(i)==n])
# f(1) = 63
# f(2) = 315
# f(3) = 630
# f(4) = 630 = 315 * 2
# f(5) = 315 = 63 * 5
# f(6) = 63

# f(n) = sum([i for i in range(int(2**7)) if hamming_weight(i)==n])
# f(1) = 127
# f(2) = 762
# f(3) = 1905
# f(4) = 2540 = 1905 * 4/3
# f(5) = 1905 = 762 * 5/2
# f(6) = 762 = 127 * 6
# f(7) = 127

# f(n) = sum([i for i in range(int(2**8)) if hamming_weight(i)==n])
# f(1) = 255
# f(2) = 1785
# f(3) = 5355
# f(4) = 8925
# f(5) = 8925 = 5355 * 5/3
# f(6) = 5355 = 1785 * 3
# f(7) = 1785 = 255 * 7
# f(8) = 255

# f(n) = sum([i for i in range(int(2**10)) if hamming_weight(i)==n])
# f(1) = 1023
# f(2) = 9207
# f(3) = 36828
# f(4) = 85932
# f(5) = 128898
# f(6) = 128898
# f(7) = 85932
# f(8) = 36828
# f(9) = 9207
# f(10) = 1023

# general for sum of numbers with a particular hamming weight, less then 2^x
# f(n) = sum([i for i in range(int(2**x)) if hamming_weight(i)==n])
# f(1) = f(x) = 2^x - 1
# f(2) = f(x-1) = f(1) * (x-1)/1
# f(3) = f(x-2) = f(2) * (x-2)/2
# f(4) = f(x-3) = f(3) * (x-3)/3
# f(5) = f(x-4) = f(4) * (x-4)/4


# f2(n) = sum([i**2 for i in range(int(2**10)) if hamming_weight(i)==n])
# f2(1) = 349525 = 1/3 * (4^10 - 1) = 1/3 * (4^x - 1)
# f2(2) = 3842729
# f2(3) = 18158932
# f2(4) = 48876212
# f2(5) = 83072374
# f2(6) = 92830430
# f2(7) = 68392324
# f2(8) = 32099012
# f2(9) = 8721757
# f2(10) = 1046529 = 1023^2 = f(10)^2 = f(1)^2 = (2^10 - 1)^2 = (2^x - 1)^2

# # sum of numbers of hamming weight 2
# sum([i for i in range(16) if hamming_weight(i)==2])
# # def g(n): return n*(2**(n+1) - 1)
# def g(n): return (n-1)*(2**n - 1)  # this equals h(n) defined below
#
# # get sum of numbers of hamming weight 2, s.t. < 2^n
# def h(n):
#     ans = 0
#     for i in range(n):
#         for j in range(i):
#             ans += 2**i + 2**j
#     return ans


# sum of numbers of hamming weight 3

# math.log2(10**16) = 53.150849518197795, therefore 54 bits


# n = 100000//2
# print(s2(n*2))
# print((4*s2(n) + n*(4*n**2 -1)/3  + sum(8*g(i) + 8*i*g(i) + 2*hamming_weight(i) + 4*g(i)*hamming_weight(i) + 4*g(i)**2 + hamming_weight(i)**2
#                for i in range(n))) % 1000000007)


# n = 100000//2
# print(s2(n*2))
# print((8*s2(n) - 4*g(n)**2 + n*(4*n**2 -1)/3  + sum(8*g(i) + 8*i*g(i) + 2*hamming_weight(i) + 4*g(i)*hamming_weight(i) + hamming_weight(i)**2
#                for i in range(n))) % 1000000007)



# sum(f(i) for i in 0 to n-1)
# n, sum(f), sum(f)/n
# 1, 0     , 0
# 2, 1     ,
# 3, 1     ,
# 4, 9     ,
# 5, 13    , 2.6 = 13//5 + 3/5
# 6, 23    , 3.833, 23//6 + 5/6
# 7, 35    , 5, + 0
# 8, 56    , 7, + 0
# 9, 64    , 7.111, + 1/9
# 10, 82    , 8.2, + 2/10
# 11, 102    , 9.2727, + 3/11
# 12, 135    , 11.25, + 3/12
# 13, 159    , 12.2307692307692, + 3/13
# 14, 198    , 14.142857142857142, + 2/14


# n2 = 100001
# n = n2//2
# print(s2(n2))
# print((8*s2(n) + (n+1)*(2*n+1)*(2*n+3)/3  + sum(8*g(i) + 8*i*g(i) + 2*hamming_weight(i) + 4*g(i)*hamming_weight(i) + hamming_weight(i)**2
#                for i in range(n+1))) % 1000000007)


# n2 = 100001
# n = n2//2
# print(s2(n2))
# print((8*s2(n) + (n+1)*(2*n+1)*(2*n+3)/3  + sum(hamming_weight(i)*(8*i + 8*i**2 + 2 + 4*i*hamming_weight(i) + hamming_weight(i))
#                for i in range(n+1))) % 1000000007)

# n2 = 100001
# n = n2//2
# print(s2(n2))
#
# base = 8*s2(n) + (n+1)*(2*n+1)*(2*n+3)/3
# new_s = base
# new_s += sum(2*hamming_weight(i)*(2*i+1)**2 for i in range(n+1))
# new_s += sum(hamming_weight(i)**2*(4*i + 1) for i in range(n+1))
# print(new_s % 1000000007)


def p(q):
    ans = 0
    for i in range(1, q+1):
        ham = hamming_weight(i)
        ans += 2*(2*i + 1)**2*ham
        ans += (4*i + 1) * ham**2
    return ans


def new_s2(n, m=1000000007):  # up to 10^6 is fast
    ans = 0
    if n == 2:
        return 5
    if n == 1:
        return 1

    if n % 2 == 1:  # if n is odd
        pass
    else:  # n is even
        ans -= (hamming_weight(n + 1)*(n+1))**2 % m
    q = n // 2  # n = 2q + 1
    ans += 8 * new_s2(q) + (q+1)*(2*q+1)*(2*q+3)/3 % m
    ans += p(q) % m
    return ans % m





# general for sum of numbers with a particular hamming weight, less then 2^x
# f(n) = sum([i for i in range(int(2**x)) if hamming_weight(i)==n])
# f(1) = f(x) = 2^x - 1
# f(2) = f(x-1) = f(1) * (x-1)/1
# f(3) = f(x-2) = f(2) * (x-2)/2
# f(4) = f(x-3) = f(3) * (x-3)/3
# f(5) = f(x-4) = f(4) * (x-4)/4

"""https://oeis.org/A231500"""


# f(2n) = 2f(n)
# f(2n + 1) = 2n + 1 + 2f(n) + f(n)/n

# f(n) = n*h(n)
# 2nh(2n) = f(2n) = 2f(n) = 2nh(n)
# h(2n) = h(n)

# (2n + 1)*h(2n + 1) = f(2n + 1) = 2n + 1 + 2f(n) + f(n)/n = (2n+1) + 2nh(n) + h(n)
# (2n + 1)*h(2n + 1)= (2n + 1) + (2n + 1)h(n)
# h(2n + 1) = 1 + h(n)
