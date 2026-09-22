"""
EXPERIMENTAL / ALTERNATIVE SOLUTION

Project Euler Problem 345: Matrix Sum
Variant: Recursive Search with Subproblem Memoization (Bitmask / Tuple State DP)

Description:
  Solves Matrix Sum by assigning elements row-by-row, memoizing the maximum
  subproblem score for any remaining tuple of unused column indices.

ANSWER: 13938
"""

import functools
import unittest
from typing import Tuple


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]

    return memoizer


class Problem345Recursive:
    def __init__(self, matrix_str: str = None):
        if matrix_str is None:
            raw = """7  53 183 439 863 497 383 563  79 973 287  63 343 169 583
627 343 773 959 943 767 473 103 699 303 957 703 583 639 913
447 283 463  29  23 487 463 993 119 883 327 493 423 159 743
217 623   3 399 853 407 103 983  89 463 290 516 212 462 350
960 376 682 962 300 780 486 502 912 800 250 346 172 812 350
870 456 192 162 593 473 915  45 989 873 823 965 425 329 803
973 965 905 919 133 673 665 235 509 613 673 815 165 992 326
322 148 972 962 286 255 941 541 265 323 925 281 601  95 973
445 721  11 525 473  65 511 164 138 672  18 428 154 448 848
414 456 310 312 798 104 566 520 302 248 694 976 430 392 198
184 829 373 181 631 101 969 613 840 740 778 458 284 760 390
821 461 843 513  17 901 711 993 293 157 274  94 192 156 574
 34 124   4 878 450 476 712 914 838 669 875 299 823 329 699
815 559 813 459 522 788 168 586 966 232 308 833 251 631 107
813 883 451 509 615  77 281 613 459 205 380 274 302  35 805"""
        else:
            raw = matrix_str
        self.matrix = [list(map(int, line.split())) for line in raw.strip().splitlines()]

    def solve(self) -> int:
        grid = self.matrix
        num_rows = len(grid)
        num_cols = len(grid[0])

        @memoize
        def search(rows: Tuple[int, ...], cols: Tuple[int, ...]) -> int:
            if not rows:
                return 0
            curr_row = rows[0]
            remaining_rows = rows[1:]
            return max(
                grid[curr_row][c] + search(remaining_rows, cols[:idx] + cols[idx + 1:])
                for idx, c in enumerate(cols)
            )

        return search(tuple(range(num_rows)), tuple(range(num_cols)))


class Solution345Recursive(unittest.TestCase):
    def test_solution(self):
        solver = Problem345Recursive()
        self.assertEqual(13938, solver.solve())


if __name__ == "__main__":
    unittest.main()
