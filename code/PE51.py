"""
PROBLEM

By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values:
 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having
 seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773,
  and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit,
 is part of an eight prime value family.

ANSWER: 121313

Solve time ~0.8 seconds
"""

from collections import Counter
# from primesieve.numpy import primes
from primesieve import primes
from util.utils import timeit
import unittest


class Problem51:
    def __init__(self, max_dig):
        self.max_dig_num = max_dig
        self.ls_str_primes = [str(x) for x in primes(pow(10, self.max_dig_num-1), pow(10, self.max_dig_num))]
        # self.ls_str_primes = primes(pow(10, self.max_dig_num-1), pow(10, self.max_dig_num)).astype(str)

    @timeit
    def solve(self):
        max_rep_dig = 0
        location = None
        sub_string = ''

        for i in range(self.max_dig_num-1):
            num_rep = self.f1(i)
            if num_rep[1] > max_rep_dig:
                max_rep_dig = num_rep[1]
                location = i
                sub_string = num_rep[0]

            for j in range(i+1, self.max_dig_num-1):
                num_rep = self.f2(i, j)
                if num_rep[1] > max_rep_dig:
                    max_rep_dig = num_rep[1]
                    location = (i, j)
                    sub_string = num_rep[0]

                for k in range(j+1, self.max_dig_num-1):
                    num_rep = self.f3(i, j, k)
                    if num_rep[1] > max_rep_dig:
                        max_rep_dig = num_rep[1]
                        location = (i, j, k)
                        sub_string = num_rep[0]

        return self.get_prime(location, sub_string, 0)
        # return max_rep_dig, location, sub_string

    def get_prime(self, location, sub_string, fill_num):
        answer = [None] * self.max_dig_num
        i = 0
        for j in range(len(answer)):
            if j in location:
                answer[j] = str(fill_num)
            else:
                answer[j] = sub_string[i]
                i += 1
        possible_prime = int(''.join(answer))
        if str(possible_prime) in self.ls_str_primes:
            return possible_prime
        else:
            return self.get_prime(location, sub_string, fill_num+1)

    def f3(self, i, j, k):
        nums = []
        for p in self.ls_str_primes:
            if p[i] == p[j] and p[i] == p[k]:
                nums.append(p[:i] + p[i+1:j] + p[j+1:k] + p[k+1:])

        return Counter(nums).most_common()[0]

    def f2(self, i, j):
        nums = []
        for p in self.ls_str_primes:
            if p[i] == p[j]:
                nums.append(p[:i] + p[i+1:j] + p[j+1:])

        return Counter(nums).most_common()[0]

    def f1(self, i):
        nums = []
        for p in self.ls_str_primes:
            nums.append(p[:i] + p[i+1:])
        return Counter(nums).most_common()[0]


class Solution51(unittest.TestCase):
    def setUp(self):
        self.problem = Problem51(max_dig=6)

    def test_solution(self):
        self.assertEqual(121313, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
