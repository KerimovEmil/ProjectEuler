r"""
PROBLEM

Sam and Max are asked to transform two digital clocks into two "digital root" clocks.

A digital root clock is a digital clock that calculates digital roots step by step.

When a clock is fed a number, it will show it and then it will start the calculation, showing all the intermediate values until it gets to the result.

For example, if the clock is fed the number 137, it will show: "137" → "11" → "2" and then it will go black, waiting for the next number.

Every digital number consists of some light segments: three horizontal (top, middle, bottom) and four vertical (top-left, top-right, bottom-left, bottom-right).

Number "1" is made of vertical top-right and bottom-right, number "4" is made by middle horizontal and vertical top-left, top-right and bottom-right. Number "8" lights them all.

The clocks consume energy only when segments are turned on/off.

To turn on a "2" will cost 5 transitions, while a "7" will cost only 4 transitions.

Sam and Max built two different clocks.

Sam's clock is fed e.g. number 137: the clock shows "137", then the panel is turned off, then the next number ("11") is turned on, then the panel is turned off again and finally the last number ("2") is turned on and, after some time, off.

For the example, with number 137, Sam's clock requires:

"137": (2 + 5 + 4) × 2 = 22 transitions ("137" on/off).
"11": (2 + 2) × 2 = 8 transitions ("11" on/off).
"2": (5) × 2 = 10 transitions ("2" on/off).

For a grand total of 40 transitions.

Max's clock works differently. Instead of turning off the whole panel, it is smart enough to turn off only those segments that won't be needed for the next number.

For number 137, Max's clock requires:

"137": 2 + 5 + 4 = 11 transitions ("137" on)
7 transitions (to turn off the segments that are not needed for number "11").
"11": 0 transitions (number "11" is already turned on correctly)
3 transitions (to turn off the first "1" and the bottom part of the second "1"; the top part is common with number "2").
"2": 4 transitions (to turn on the remaining segments in order to get a "2")
5 transitions (to turn off number "2").

For a grand total of 30 transitions.

Of course, Max's clock consumes less power than Sam's one.

The two clocks are fed all the prime numbers between A = 10^7 and B = 2×10^7.

Find the difference between the total number of transitions needed by Sam's clock and that needed by Max's one.

ANSWER: 13625242
Solve time: ~0.08 seconds

---
MATHEMATICAL DERIVATION:

1. Digital Transition Cost Difference:
   - Let a sequence of intermediate values for number $p$ be $X_1 \to X_2 \to \dots \to X_k$, where $X_1 = p$
     and $X_k$ is a single-digit root.
   - In Sam's clock, every number $X_i$ is turned on and then turned off completely:
     $$\text{Cost}_{\text{Sam}} = 2 \sum_{i=1}^k |X_i|$$
     where $|X_i|$ is the number of lit segments in $X_i$.
   - In Max's clock, transitions between consecutive numbers $X_i$ and $X_{i+1}$ preserve overlapping segments:
     - Turning off unneeded segments: $|X_i| - |X_i \cap X_{i+1}|$.
     - Turning on newly required segments: $|X_{i+1}| - |X_i \cap X_{i+1}|$.
     - Combined with initial turn-on of $X_1$ and final turn-off of $X_k$:
       $$\text{Cost}_{\text{Max}} = |X_1| + \sum_{i=1}^{k-1} (|X_i| + |X_{i+1}| - 2 |X_i \cap X_{i+1}|) + |X_k| = 2 \sum_{i=1}^k |X_i| - 2 \sum_{i=1}^{k-1} |X_i \cap X_{i+1}|$$
   - Subtracting the two costs yields the exact transition savings for each prime $p$:
     $$\Delta(p) = \text{Cost}_{\text{Sam}} - \text{Cost}_{\text{Max}} = 2 \sum_{i=1}^{k-1} |X_i \cap X_{i+1}|$$

2. Path Invariance & Precomputed Lookups:
   - For any prime $p \in [10^7, 2 \times 10^7]$, the first digit sum $S_1 = \text{digit\_sum}(p) \le 1 + 7 \times 9 = 64$.
   - The tail sequence $S_1 \to S_2 \to \dots \to S_k$ and its associated savings $\text{sub\_saving}(S_1) = 2 \sum_{i \ge 1} |S_i \cap S_{i+1}|$
     depend solely on $S_1$ and are precomputed in $O(1)$ for all $S_1 \in [1, 64]$.
   - The first transition savings $2 |p \cap S_1|$ depends exclusively on the lowest two digits of $p$ ($p \pmod{100}$)
     and $S_1$, because $S_1 \le 64$ occupies at most two digit positions.
   - We construct a lookup table $T[\text{last2}][S_1] = 2 |\text{last2} \cap S_1| + \text{sub\_saving}(S_1)$ and vectorize
     the evaluation across all primes using NumPy.
"""

import unittest
import numpy as np
from util.utils import timeit, prime_sieve


class Problem315:
    def __init__(self, a: int = 10**7, b: int = 2 * 10**7):
        self.a = a
        self.b = b

    @timeit
    def solve(self) -> int:
        # Bitmask representations of 7-segment digits:
        # Bits: 0: top, 1: top-left, 2: top-right, 3: middle, 4: bottom-left, 5: bottom-right, 6: bottom
        digits = [
            0b1110111,  # 0
            0b0100100,  # 1
            0b1011101,  # 2
            0b1101101,  # 3
            0b0101110,  # 4
            0b1101011,  # 5
            0b1111011,  # 6
            0b0100111,  # 7
            0b1111111,  # 8
            0b1101111,  # 9
        ]

        # Pairwise common segment count between single digits
        common_digit = [
            [(digits[i] & digits[j]).bit_count() for j in range(10)]
            for i in range(10)
        ]

        def common_segments(x: int, y: int) -> int:
            tot = 0
            while x > 0 and y > 0:
                tot += common_digit[x % 10][y % 10]
                x //= 10
                y //= 10
            return tot

        def sum_digits(n: int) -> int:
            s = 0
            while n > 0:
                s += n % 10
                n //= 10
            return s

        # Precompute subsequent savings for digital root sequence starting at S_1 in [1, 70]
        sub_saving = [0] * 71
        for s in range(1, 71):
            cur = s
            tot = 0
            while cur >= 10:
                nxt = sum_digits(cur)
                tot += 2 * common_segments(cur, nxt)
                cur = nxt
            sub_saving[s] = tot

        # Precompute transition table: table[p % 100, S_1] = 2 * common(p, S_1) + sub_saving[S_1]
        table = np.zeros((100, 71), dtype=np.int64)
        for last2 in range(100):
            d0_p = last2 % 10
            d1_p = last2 // 10
            for s1 in range(1, 71):
                d0_s = s1 % 10
                d1_s = s1 // 10
                c = common_digit[d0_p][d0_s] + (common_digit[d1_p][d1_s] if d1_s > 0 else 0)
                table[last2, s1] = 2 * c + sub_saving[s1]

        # Precompute 4-digit sum table for fast vectorized digit sum computation
        dsum_arr = np.array([sum_digits(i) for i in range(10000)], dtype=np.int64)

        # Sieve primes in [self.a, self.b]
        sieve = prime_sieve(self.b)
        primes = np.nonzero(sieve[self.a : self.b])[0] + self.a

        # Vectorized lookup across all primes in interval
        p_mod100 = primes % 100
        s1 = dsum_arr[primes // 10000] + dsum_arr[primes % 10000]

        return int(np.sum(table[p_mod100, s1]))


class Solution315(unittest.TestCase):
    def setUp(self):
        self.problem = Problem315()

    def test_sample_137(self):
        # Verify 137 from problem statement: Sam requires 40, Max requires 30, diff = 10
        digits = [
            0b1110111, 0b0100100, 0b1011101, 0b1101101, 0b0101110,
            0b1101011, 0b1111011, 0b0100111, 0b1111111, 0b1101111
        ]
        common = [[(digits[i] & digits[j]).bit_count() for j in range(10)] for i in range(10)]

        def common_segs(x: int, y: int) -> int:
            tot = 0
            while x > 0 and y > 0:
                tot += common[x % 10][y % 10]
                x //= 10
                y //= 10
            return tot

        # 137 -> 11 -> 2
        diff_137 = 2 * (common_segs(137, 11) + common_segs(11, 2))
        self.assertEqual(10, diff_137)

    def test_solution(self):
        self.assertEqual(13625242, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
