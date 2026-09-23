r"""
PROBLEM

By using each of the digits from the set, $\{1, 2, 3, 4\}$, exactly once, and making use of the four arithmetic
operations ($+, -, \times, /$) and brackets/parentheses, it is possible to form different positive integer targets.

For example,

$$\begin{align}
8 &= (4 \times (1 + 3)) / 2\\
14 &= 4 \times (3 + 1 / 2)\\
19 &= 4 \times (2 + 3) - 1\\
36 &= 3 \times 4 \times (2 + 1)
\end{align}$$

Note that concatenations of the digits, like $12 + 34$, are not allowed.

Using the set, $\{1, 2, 3, 4\}$, it is possible to obtain thirty-one different target numbers of which $36$ is the
maximum, and each of the numbers $1$ to $28$ can be obtained before encountering the first non-expressible number.

Find the set of four distinct digits, $a \lt b \lt c \lt d$, for which the longest set of consecutive positive integers,
$1$ to $n$, can be obtained, giving your answer as a string: abcd.

ANSWER: 1258
Solve time: ~0.08 seconds
"""

import unittest
from itertools import combinations

from util.utils import timeit


class Problem93:
    def __init__(self):
        pass

    @staticmethod
    def get_targets(digits):
        """Return the set of all positive integers expressible using each digit in digits exactly once."""
        dp = {1 << i: {float(d)} for i, d in enumerate(digits)}

        for mask in range(1, 16):
            if mask in dp:
                continue
            res = set()
            submask = (mask - 1) & mask
            while submask > (mask ^ submask):
                s1, s2 = submask, mask ^ submask
                for a in dp[s1]:
                    for b in dp[s2]:
                        res.add(a + b)
                        res.add(a - b)
                        res.add(b - a)
                        res.add(a * b)
                        if b != 0:
                            res.add(a / b)
                        if a != 0:
                            res.add(b / a)
                submask = (submask - 1) & mask
            dp[mask] = res

        pos_ints = {int(round(v)) for v in dp[15] if v > 0 and abs(v - round(v)) < 1e-9}
        return pos_ints

    @staticmethod
    def consecutive_length(pos_ints):
        n = 1
        while n in pos_ints:
            n += 1
        return n - 1

    @timeit
    def solve(self):
        best_len = 0
        best_digits = None

        for digits in combinations(range(1, 10), 4):
            targets = self.get_targets(digits)
            length = self.consecutive_length(targets)
            if length > best_len:
                best_len = length
                best_digits = digits

        return "".join(str(d) for d in best_digits)


class Solution93(unittest.TestCase):
    def setUp(self):
        self.problem = Problem93()

    def test_sample(self):
        targets = Problem93.get_targets((1, 2, 3, 4))
        self.assertEqual(28, Problem93.consecutive_length(targets))

    def test_solution(self):
        self.assertEqual("1258", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
