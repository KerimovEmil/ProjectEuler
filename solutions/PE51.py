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

Solve time ~1.7 seconds
"""

# Useful insights from project euler solutions thread

# you don't have to check the primes with two or four recurring digits. If you form 8 different numbers with them,
# at least once the sum of the digits (and the whole number) is divisible by three.

from collections import Counter
from primesieve import primes
from util.utils import timeit
import unittest


class Problem51:
    def __init__(self, max_dig):
        self.max_dig_num = max_dig
        self.ls_str_primes = [str(x) for x in primes(pow(10, self.max_dig_num-1), pow(10, self.max_dig_num))]

    @timeit
    def solve(self):
        max_rep_dig = 0  # keep track of the maximum number of primes that can be represented
        location = None
        sub_string = ''

        for i in range(self.max_dig_num-1):  # loop over number of maximum digits
            num_rep = self.get_common_prime_substring([i])  # replacing one digit
            if num_rep[1] > max_rep_dig:
                max_rep_dig = num_rep[1]
                location = i
                sub_string = num_rep[0]

            for j in range(i+1, self.max_dig_num-1):  # loop over remaining digits
                # no need to check replacing two digits, see math comment above solutions

                for k in range(j+1, self.max_dig_num-1):
                    num_rep = self.get_common_prime_substring([i, j, k])  # replacing three digits
                    if num_rep[1] > max_rep_dig:
                        max_rep_dig = num_rep[1]
                        location = (i, j, k)
                        sub_string = num_rep[0]

        return self.get_prime(location, sub_string)

    def get_prime(self, location, sub_string):
        """
        Based on the digit locations that are being swapped, and the substring that is kept constant, fill the swapped
        values with the fill_num until a prime is found. That prime will be the smallest one that has this property

        e.g.
        location = [0, 2, 4]
        sub_string = '233'

        constructs prime: '121313'
        """
        for fill_value in range(10):  # possible digits to fill the None's by
            possible_ls_primes = [None] * self.max_dig_num
            j = 0  # starting at the first sub string element
            for i in range(len(possible_ls_primes)):
                if i in location:  # common element to fill
                    possible_ls_primes[i] = str(fill_value)
                else:  # substring
                    possible_ls_primes[i] = sub_string[j]
                    j += 1
            # test if new number is prime
            possible_prime = int(''.join(possible_ls_primes))
            if str(possible_prime) in self.ls_str_primes:
                return possible_prime

    @staticmethod
    def _remove_from_sub_string(s, ls_index):
        """
        Given a string s, returns the sub string with the indices in ls_index removed.
        e.g. ls_index = [i, j, k]
        returns p[:i] + p[i+1:j] + p[j+1:k] + p[k+1:]
        """
        out = s[:ls_index[0]]
        for i in range(1, len(ls_index)):
            out += s[ls_index[i-1] + 1: ls_index[i]]
        out += s[ls_index[-1] + 1:]
        return out

    def get_common_prime_substring(self, digit_loc):
        """
        Given digit locations i,j,k,.. , for each prime removes the ith, jth, and kth digit, if they are the same,
        and returns the most common resulting substring, and how many times it came up.
        """
        nums = []
        for p in self.ls_str_primes:
            if len(set([p[index] for index in digit_loc])) == 1:  # checks the values being removes are the same
                nums.append(self._remove_from_sub_string(p, digit_loc))

        return Counter(nums).most_common()[0]


class Solution51(unittest.TestCase):
    def setUp(self):
        self.problem = Problem51(max_dig=6)  # 1,000,000 <= x < 10,000,000

    def test_solution(self):
        self.assertEqual(121313, self.problem.solve())


if __name__ == '__main__':
    unittest.main()


