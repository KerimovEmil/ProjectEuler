"""
PROBLEM

Anton and Bertrand love to play three pile Nim.
However, after a lot of games of Nim they got bored and changed the rules somewhat.
They may only take a number of stones from a pile that is a proper divisor of the number of stones present in the pile.
E.g. if a pile at a certain moment contains 24 stones they may take only 1, 2, 3, 4, 6, 8 or 12 stones from that pile.
So if a pile contains one stone they can't take the last stone from it as 1 isn't a proper divisor of 1.
The first player that can't make a valid move loses the game.
Of course both Anton and Bertrand play optimally.

The triple (a, b, c) indicates the number of stones in the three piles.
Let S(n) be the number of winning positions for the next player for 1 <= a, b, c <= n.
S(10) = 692 and S(100) = 735494.

Find S(123456787654321) modulo 1234567890.

ANSWER: 151725678
Solve time: ~0.0001 seconds

---
MATHEMATICAL & ALGEBRAIC DERIVATION:

1. Sprague-Grundy Value of a Single Pile (g(k) = v_2(k)):
   Let v_2(k) denote the 2-adic valuation of k (the exponent of the highest power of 2 dividing k).
   We prove by induction on k >= 1 that the Grundy value g(k) equals v_2(k):
   - Base case k = 1: 1 has no proper divisors, so there are no valid moves and g(1) = 0 = v_2(1).
   - Inductive step: Write k = 2^e * m where e = v_2(k) and m >= 1 is odd.
     Any proper divisor d of k has the form d = 2^j * u where 0 <= j <= e, u | m (so u is odd), and d < k.
     * Case A (0 <= j < e):
       k - d = 2^e * m - 2^j * u = 2^j * (2^(e - j) * m - u).
       Since 2^(e - j) * m is even and u is odd, their difference (2^(e - j) * m - u) is odd.
       Thus, v_2(k - d) = j < e.
       Conversely, for every j in {0, 1, ..., e - 1}, choosing d = 2^j (which is a proper divisor of k since
       2^j < 2^e <= k) transitions to k - 2^j with v_2(k - 2^j) = j.
     * Case B (j = e):
       Here d = 2^e * u with u | m and u < m (since d < k).
       Because both m and u are odd, m - u is a positive even integer, so v_2(m - u) >= 1.
       Thus, v_2(k - d) = v_2(2^e * (m - u)) = e + v_2(m - u) >= e + 1 > e.
     Combining Cases A and B: from a pile with v_2(k) = e, we can reach every valuation j in {0, ..., e - 1},
     and we can never transition to another state with valuation e.
     By the inductive hypothesis, g(k) = mex{g(k - d) : d | k, d < k} = e = v_2(k).

2. Frequency of Each Grundy Value in {1, ..., n}:
   An integer x in {1, ..., n} satisfies v_2(x) = e if and only if x is a multiple of 2^e but not a multiple of 2^(e + 1).
   Therefore, the count c_e of integers in {1, ..., n} with Grundy value e is:
     c_e = floor(n / 2^e) - floor(n / 2^(e + 1))   for 0 <= e <= floor(log_2(n)).

3. Counting Winning Triples (a, b, c):
   By the Sprague-Grundy theorem, a 3-pile game (a, b, c) is a losing position (P-position) if and only if:
     g(a) ^ g(b) ^ g(c) = 0   <=>   g(c) = g(a) ^ g(b).
   Summing over all pairs of Grundy values (e_1, e_2), the total number of losing positions is:
     L(n) = sum_{e_1 = 0}^K sum_{e_2 = 0}^K c_{e_1} * c_{e_2} * c_{e_1 ^ e_2},
   where K = floor(log_2(n)) and c_e = 0 for e > K.
   Subtracting L(n) from the total number of triples n^3 gives the number of winning positions:
     S(n) = n^3 - L(n).
   For n = 123,456,787,654,321, K = 46, so evaluating S(n) requires only 47^2 = 2,209 loop iterations (~0.0001s).
"""

import unittest
from util.utils import timeit


class Problem509:
    def __init__(self):
        pass

    @staticmethod
    def compute_s(n: int, mod: int | None = None) -> int:
        counts = []
        e = 0
        while (1 << e) <= n:
            counts.append((n >> e) - (n >> (e + 1)))
            e += 1

        num_states = len(counts)
        losing = 0
        for e1 in range(num_states):
            c1 = counts[e1]
            for e2 in range(num_states):
                e3 = e1 ^ e2
                if e3 < num_states:
                    losing += c1 * counts[e2] * counts[e3]

        winning = n**3 - losing
        return winning % mod if mod is not None else winning

    @timeit
    def solve(self) -> int:
        return self.compute_s(123456787654321, mod=1234567890)


class Solution509(unittest.TestCase):
    def setUp(self):
        self.problem = Problem509()

    def test_sample(self):
        self.assertEqual(692, self.problem.compute_s(10))
        self.assertEqual(735494, self.problem.compute_s(100))

    def test_solution(self):
        self.assertEqual(151725678, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
