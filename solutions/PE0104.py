r"""
PROBLEM

The Fibonacci sequence is defined by the recurrence relation:

$F_n = F_{n - 1} + F_{n - 2}$, where $F_1 = 1$ and $F_2 = 1$.

It turns out that $F_{541}$, which contains $113$ digits, is the first
Fibonacci number for which the last nine digits are $1$-$9$ pandigital
(contain all the digits $1$ to $9$, but not necessarily in order).
And $F_{2749}$, which contains $575$ digits, is the first Fibonacci number
for which the first nine digits are $1$-$9$ pandigital.

Given that $F_k$ is the first Fibonacci number for which the first nine
digits AND the last nine digits are $1$-$9$ pandigital, find $k$.

ANSWER: 329468
Solve time: ~0.10 seconds

---
MATHEMATICAL DERIVATION:

1. Modular Arithmetic for the Tail (Last 9 Digits):
   We maintain $F_k \pmod{10^9}$ iteratively using the standard Fibonacci recurrence:
   $$F_k \equiv (F_{k-1} + F_{k-2}) \pmod{10^9}$$
   Because $10^9$ fits easily in standard 64-bit integer arithmetic, each step
   requires $O(1)$ operations and avoids arbitrary-precision big-integer arithmetic
   during the search loop.

2. Fast Pandigital Screening:
   A number is $1$-$9$ pandigital if and only if it consists of digits $1$ through $9$
   each appearing exactly once. We apply tiered fast-rejection filters:
   - Modulo 9 filter: The sum of digits of any $1$-$9$ pandigital number is
     $1 + 2 + \dots + 9 = 45 \equiv 0 \pmod 9$. Thus, any pandigital tail must
     satisfy $F_k \equiv 0 \pmod 9$. This filters out $\approx 89\%$ of candidates immediately.
   - Range filter: The smallest $1$-$9$ pandigital number is $123456789$ and
     the largest is $987654321$. Values outside $[123456789, 987654321]$ are rejected.
   - Character / set check: Converting to string, checking `'0' not in s` and `len(set(s)) == 9`.

   The probability that a random 9-digit suffix forms a $1$-$9$ pandigital permutation
   is $9! / 10^9 \approx 3.63 \times 10^{-4}$.
   Consequently, the trailing 9 digits are pandigital only $\sim 120$ times across
   the first $330,000$ Fibonacci numbers.

3. Logarithmic Approximation for the Head (First 9 Digits):
   By Binet's formula:
   $$F_k = \frac{\phi^k - \psi^k}{\sqrt{5}}$$
   where $\phi = \frac{1 + \sqrt{5}}{2} \approx 1.6180339887\dots$ and
   $\psi = \frac{1 - \sqrt{5}}{2} \approx -0.6180339887\dots$.
   For $k > 50$, $|\psi|^k / \sqrt{5} < 10^{-10}$, which is completely negligible.
   Taking base-10 logarithm:
   $$\log_{10}(F_k) \approx k \log_{10}(\phi) - \frac{1}{2} \log_{10}(5)$$
   Let $t = k \log_{10}(\phi) - \log_{10}(\sqrt{5})$ and let $\{t\} = t - \lfloor t \rfloor$
   denote its fractional part. The leading 9 digits of $F_k$ are given by:
   $$\lfloor 10^{\{t\} + 8} \rfloor$$
   Since we only evaluate this closed form when the last 9 digits are already verified pandigital,
   this high-precision $O(1)$ calculation is executed only $\sim 120$ times in total, providing
   exceptional performance (< 0.15s overall runtime).
"""

import decimal
import unittest
from decimal import Decimal
from util.utils import timeit


def is_1_to_9_pandigital(n: int) -> bool:
    """
    Checks if an integer has exactly 9 digits and contains all digits 1-9.
    """
    if n % 9 != 0 or n < 123456789 or n > 987654321:
        return False
    s = str(n)
    return '0' not in s and len(set(s)) == 9


class Problem104:
    def __init__(self):
        # Precompute Decimal constants within a local context to avoid polluting global state
        with decimal.localcontext() as ctx:
            ctx.prec = 50
            phi = (Decimal(5).sqrt() + 1) / 2
            self.log10_phi = phi.log10()
            self.log10_sqrt5 = Decimal(5).sqrt().log10()

    def get_leading_nine_digits(self, k: int) -> int:
        """
        Computes the first 9 digits of F_k using Binet's logarithmic approximation.
        """
        with decimal.localcontext() as ctx:
            ctx.prec = 50
            t = k * self.log10_phi - self.log10_sqrt5
            frac = t - int(t)
            return int(10 ** (frac + 8))

    @timeit
    def solve(self) -> int:
        a, b = 1, 1
        k = 2
        mod = 10**9

        while True:
            k += 1
            a, b = b, (a + b) % mod
            if is_1_to_9_pandigital(b):
                lead = self.get_leading_nine_digits(k)
                if is_1_to_9_pandigital(lead):
                    return k


class Solution104(unittest.TestCase):
    def setUp(self):
        self.problem = Problem104()

    def test_sample_last_nine_digits(self):
        # F_541 is the first Fibonacci number whose last nine digits are 1-9 pandigital
        a, b = 1, 1
        k = 2
        mod = 10**9
        while True:
            k += 1
            a, b = b, (a + b) % mod
            if is_1_to_9_pandigital(b):
                break
        self.assertEqual(541, k)
        self.assertEqual(839725641, b)

    def test_sample_first_nine_digits(self):
        # F_2749 is the first Fibonacci number whose first nine digits are 1-9 pandigital
        lead_2749 = self.problem.get_leading_nine_digits(2749)
        self.assertEqual(143726895, lead_2749)
        self.assertTrue(is_1_to_9_pandigital(lead_2749))

    def test_solution(self):
        self.assertEqual(329468, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
