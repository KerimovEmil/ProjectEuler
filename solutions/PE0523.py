"""
PROBLEM

Consider the following algorithm for sorting a list:
1. Starting from the beginning of the list, check each pair of adjacent elements in turn.
2. If the elements are out of order:
   a. Move the smallest element of the pair at the beginning of the list.
   b. Restart the process from step 1.
3. If all pairs are in order, stop.

For example, the list { 4 1 3 2 } is sorted as follows:
- 4 1 3 2 (4 and 1 are out of order, so move 1 to the front)
- 1 4 3 2 (4 and 3 are out of order, so move 3 to the front)
- 3 1 4 2 (3 and 1 are out of order, so move 1 to the front)
- 1 3 4 2 (4 and 2 are out of order, so move 2 to the front)
- 2 1 3 4 (2 and 1 are out of order, so move 1 to the front)
- 1 2 3 4 (The list is now sorted)

Let F(L) be the number of times step 2a is executed to sort list L.
For example, F({4, 1, 3, 2}) = 5.

Let E(n) be the expected value of F(P) over all permutations P of the integers {1, 2, ..., n}.
You are given E(4) = 3.25 and E(10) = 115.725.

Find E(30). Give your answer rounded to two digits after the decimal point.

ANSWER: 37125450.44
Solve time: < 1 millisecond

---
MATHEMATICAL DERIVATION:

1. Tracking Moves by Element Value:
   By linearity of expectation:
     E(n) = sum_{v=1}^n E[X_v],
   where X_v is the total number of times the value v is moved to the front.

   - The maximum element n can never be moved to the front because whenever it is compared
     with an adjacent element, it is the larger element of the pair, so the other element is
     moved to the front. Thus X_n = 0.
   - Elements smaller than v can never cause v to move to the front: when an element u < v is
     adjacent to v, either u precedes v (in order) or v precedes u (out of order, but u moves).
   - Therefore, the movement of v depends strictly on its relative ordering among the elements
     >= v, namely {v, v + 1, ..., n}.
   - By relabeling {v, v + 1, ..., n} to {1, 2, ..., m} where m = n - v + 1, the distribution
     of X_v in a random permutation of S_n is identically distributed to the number of moves of
     the value 1 in a random permutation of S_m.

2. Expected Moves of Element 1 in S_m:
   In a permutation of {1, 2, ..., m}, the value 1 is the minimum element:
   - When 1 is moved to the front, any subsequent move of another element k > 1 places k at the
     front and displaces 1 to position 2.
   - Immediately at the start of the next scan, the pair (k, 1) is out of order, causing 1 to move
     straight back to the front.
   - Hence, every time any element > 1 moves to the front, 1 moves immediately afterward.
   - Combined with the initial move of 1 (which occurs iff 1 was not already at position 1),
     X_1 = I(pos(1) > 1) + sum_{k > 1} X_k.
   - By induction or analysis of the marginal contribution of adding the m-th element, we find:
       E[X_v] = (2^{m-1} - 1) / m,  where m = n - v + 1.

3. Summation for E(n):
   Summing over all values v from 1 to n - 1 (corresponding to m from 2 to n):
     E(n) = sum_{m=2}^n (2^{m-1} - 1) / m.

   Evaluating this closed form for n = 30:
     E(30) = 2973006070891 / 80080 = 37125450.4357...
   Rounded to 2 decimal places: 37125450.44.
"""

from fractions import Fraction
import unittest
from util.utils import timeit


class Problem523:
    def __init__(self, n: int = 30):
        self.n = n

    @staticmethod
    def expected_value(n: int) -> Fraction:
        """Compute the exact rational expected value E(n)."""
        return sum(Fraction(2 ** (m - 1) - 1, m) for m in range(2, n + 1))

    @staticmethod
    def simulate_sort(lst: list[int]) -> int:
        """Simulate the sorting algorithm on a concrete list, returning step count."""
        a = list(lst)
        steps = 0
        while True:
            moved = False
            for i in range(len(a) - 1):
                if a[i] > a[i + 1]:
                    val = a.pop(i + 1)
                    a.insert(0, val)
                    steps += 1
                    moved = True
                    break
            if not moved:
                break
        return steps

    @timeit
    def solve(self) -> float:
        return round(float(self.expected_value(self.n)), 2)


class Solution523(unittest.TestCase):
    def setUp(self):
        self.problem = Problem523()

    def test_simulate(self):
        self.assertEqual(5, self.problem.simulate_sort([4, 1, 3, 2]))

    def test_samples(self):
        self.assertEqual(3.25, float(self.problem.expected_value(4)))
        self.assertEqual(115.725, float(self.problem.expected_value(10)))

    def test_solution(self):
        self.assertEqual(37125450.44, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
