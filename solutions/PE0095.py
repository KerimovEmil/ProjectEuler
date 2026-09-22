r"""
PROBLEM

The proper divisors of a number are all the divisors excluding the number itself.
For example, the proper divisors of $28$ are $1$, $2$, $4$, $7$, and $14$.
As the sum of these divisors is equal to $28$, we call it a perfect number.

Interestingly the sum of the proper divisors of $220$ is $284$ and the sum of the proper divisors of $284$ is $220$,
forming a chain of two numbers. For this reason, $220$ and $284$ are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with $12496$, we form a chain of five numbers:
$$12496 \to 14288 \to 15472 \to 14536 \to 14264 (\to 12496 \to \cdots)$$

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element exceeding one million.

ANSWER: 14316
Solve time: ~2.6 seconds
"""

import unittest
import numpy as np

from util.utils import timeit


class Problem95:
    def __init__(self, limit=1_000_000):
        self.limit = limit

    @timeit
    def solve(self):
        # Sieve the sum of proper divisors for all numbers up to limit
        sum_div = np.ones(self.limit + 1, dtype=np.int64)
        sum_div[0] = 0
        sum_div[1] = 0

        for i in range(2, self.limit // 2 + 1):
            sum_div[2 * i::i] += i

        visited_step = [0] * (self.limit + 1)
        step_idx = [0] * (self.limit + 1)
        max_len = 0
        min_elem = 0

        for start in range(1, self.limit + 1):
            if visited_step[start] != 0:
                continue

            curr = start
            curr_step = start
            path = []
            idx = 0

            while curr <= self.limit and curr > 0 and visited_step[curr] == 0:
                visited_step[curr] = curr_step
                step_idx[curr] = idx
                path.append(curr)
                idx += 1
                curr = int(sum_div[curr])

            if curr <= self.limit and curr > 0 and visited_step[curr] == curr_step:
                cycle_len = idx - step_idx[curr]
                if cycle_len > max_len:
                    max_len = cycle_len
                    min_elem = min(path[step_idx[curr]:])

        return min_elem


class Solution95(unittest.TestCase):
    def setUp(self):
        self.problem = Problem95()

    def test_solution(self):
        self.assertEqual(14316, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
