"""
A number is p-smooth if it has no prime factors larger than p.
Let T be the sequence of triangular numbers, i.e. T(n) = n(n+1)/2

Find the sum of all indices n such that T(n) is 47-smooth.

ANSWER: 2,227,616,372,734
Solve time: ~38 seconds
"""
from util.utils import timeit
import unittest
from typing import List
import heapq
from math import log


def generate_prime_min_heap(ls_p: List[int] = [2, 3, 5], max_n=20):
    """
    Given a list of prime numbers, generate a list of increasing numbers such that numbers only have the inputted
    list of prime factors.
    """
    heap = [1]
    generated_numbers = set([1])

    while len(generated_numbers) < max_n:  # Set the desired number of generated values
        num = heapq.heappop(heap)

        for factor in ls_p:
            multiplied = num * factor

            if multiplied not in generated_numbers:
                generated_numbers.add(multiplied)
                heapq.heappush(heap, multiplied)

    return generated_numbers


def k_smooth_numbers(primes, limit):
    k_s_n = [1]
    p = primes

    while len(p) != 0:
        temp_k_s_n = []
        curr_p = p.pop(0)
        power_limit = int(log(limit, curr_p)) + 1
        curr_multiples = [curr_p ** x for x in range(1, power_limit + 1)]
        for x in curr_multiples:
            for y in k_s_n:
                temp = x * y
                if temp <= limit:
                    temp_k_s_n.append(temp)
        k_s_n += temp_k_s_n
    return sorted(k_s_n)


class Problem581:
    def __init__(self):
        # self.ls_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
        self.ls_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    @timeit
    def solve(self):
        # ls_47_smooth = generate_prime_min_heap(ls_p=self.ls_prime, max_n=10_000_000)
        # 1,109,496,723,126 taken from https://oeis.org/A117581
        ls_47_smooth = k_smooth_numbers(primes=self.ls_prime, limit=1_109_496_723_127)

        ans = 0
        prev = -1
        for n in ls_47_smooth:
            # 2 consecutive smooth numbers implies that t(prev) was also smooth, since n and n-1 are smooth
            if n == prev+1:
                ans += prev
            prev = n
        return ans


class Solution581(unittest.TestCase):
    def setUp(self):
        self.problem = Problem581()

    def test_solution(self):
        self.assertEqual(2_227_616_372_734, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
