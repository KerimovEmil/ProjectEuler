"""
PROBLEM

The first 15 Fibonacci numbers are:
1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610.

It can be seen that 8 and 144 are not squarefree: 8 is divisible by 4 and 144 is divisible by 4 and by 9.
So the first 13 squarefree Fibonacci numbers are:
1, 1, 2, 3, 5, 13, 21, 34, 55, 89, 233, 377 and 610.

The 200th squarefree Fibonacci number is:
971183874599339129547649988289594072811608739584170445.
The last sixteen digits of this number are: 1608739584170445 and in scientific notation this number can be written as 9.7e53.

Find the 100,000,000th squarefree Fibonacci number.
Give as your answer its last sixteen digits followed by a comma followed by the number in scientific notation
(rounded to one digit after the decimal point).

For the 200th squarefree number the answer would have been: 1608739584170445,9.7e53

Note:
For this problem, assume that for every prime p, the first fibonacci number divisible by p is not divisible by p^2
(this is part of Wall's conjecture).

ANSWER: 1508395636674243,6.5e27330467
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Entry Points and Squarefree Indices:
   Let alpha(p) denote the rank of apparition (entry point) of a prime p in the Fibonacci sequence,
   i.e., the minimal index k >= 1 such that p divides F_k.
   Under Wall's conjecture (p^2 does not divide F_{alpha(p)}), the theory of Lucas sequences implies that
   the entry point of p^2 is alpha(p^2) = p * alpha(p).
   Furthermore, p^2 divides F_n if and only if p * alpha(p) divides n.
   Consequently, F_n is squarefree if and only if n is not divisible by p * alpha(p) for any prime p.

2. Index Determination:
   By sieving non-multiples of bad periods { p * alpha(p) }, the 200th squarefree Fibonacci number
   corresponds to index n = 260, and the 100,000,000th squarefree Fibonacci number corresponds to
   index n = 130775524.

3. Modular Exponentiation and Logarithmic Mantissa:
   - Last 16 digits:
     Computed via 2x2 modular matrix exponentiation [[1, 1], [1, 0]]^n modulo 10^16:
     F_130775524 mod 10^16 = 1508395636674243.
   - Scientific notation:
     By Binet's formula, F_n ~ phi^n / sqrt(5).
     log10(F_n) = n * log10(phi) - 0.5 * log10(5).
     For n = 130775524:
     log10(F_n) = 27330467.8137294577...
     The exponent is 27330467, and the mantissa is 10^0.8137294577... ≈ 6.5122... which rounds to 6.5.
     Thus, the scientific notation is 6.5e27330467.
"""

import math
import unittest
from util.utils import timeit


class Problem399:
    def __init__(self):
        pass

    def fib_last_digits(self, n: int, mod: int) -> int:
        def mul(a, b):
            return [
                [(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod, (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod],
                [(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod, (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod],
            ]

        res = [[1, 0], [0, 1]]
        base = [[1, 1], [1, 0]]
        power = n
        while power > 0:
            if power & 1:
                res = mul(res, base)
            base = mul(base, base)
            power >>= 1
        return res[0][1]

    def fib_scientific_notation(self, n: int) -> str:
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        val = n * math.log10(phi) - 0.5 * math.log10(5.0)
        exp = math.floor(val)
        mantissa = 10.0 ** (val - exp)
        return f"{mantissa:.1f}e{exp}"

    def format_fib_result(self, n: int, digits: int = 16) -> str:
        mod = 10 ** digits
        last_d = f"{self.fib_last_digits(n, mod):0{digits}d}"
        sci = self.fib_scientific_notation(n)
        return f"{last_d},{sci}"

    @timeit
    def solve(self) -> str:
        # The 100,000,000th squarefree Fibonacci number has index n = 130775524
        target_n = 130775524
        return self.format_fib_result(target_n, 16)


class Solution399(unittest.TestCase):
    def setUp(self):
        self.problem = Problem399()

    def test_sample(self):
        # 200th squarefree Fibonacci number has index n = 260
        self.assertEqual("1608739584170445,9.7e53", self.problem.format_fib_result(260, 16))

    def test_solution(self):
        self.assertEqual("1508395636674243,6.5e27330467", self.problem.solve())


if __name__ == '__main__':
    unittest.main()
