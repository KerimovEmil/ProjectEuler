r"""
PROBLEM

$(x,y)$ is called a nested radical pair if $x$ and $y$ are non-zero integers such that $\dfrac{x}{y}$ is not a cube of a rational number, and there exist integers $a$, $b$ and $c$ such that:

$$\sqrt{\sqrt[3]{x}+\sqrt[3]{y}}=\sqrt[3]{a}+\sqrt[3]{b}+\sqrt[3]{c}$$

For example, both $(-4,125)$ and $(5,5324)$ are nested radical pairs:

$$
\begin{align*}
\begin{split}
\sqrt{\sqrt[3]{-4}+\sqrt[3]{125}}	&= \sqrt[3]{-1}+\sqrt[3]{2}+\sqrt[3]{4}\\
\sqrt{\sqrt[3]{5}+\sqrt[3]{5324}}	&= \sqrt[3]{-2}+\sqrt[3]{20}+\sqrt[3]{25}\\
\end{split}
\end{align*}
$$

Let $H(N)$ be the sum of $|x|+|y|$ for all the nested radical pairs $(x, y)$ where $|x| \leq |y|\leq N$.

For example, $H(10^3)=2535$.

Find $H(10^{15})$. Give your answer modulo $1031^3+2$.

ANSWER: 522095328
Solve time: ~10 seconds

---
MATHEMATICAL DERIVATION:

1. Primitive Radical Families:
   By the algebraic classification of cubic nested radicals $\sqrt{\sqrt[3]{x} + \sqrt[3]{y}} = \sqrt[3]{a} + \sqrt[3]{b} + \sqrt[3]{c}$, all admissible integer pairs arise from two coprime parameter branches with integers $a, b > 0, \gcd(a, b) = 1$ (excluding $a = 2b$):
   
   - **Odd $b$ branch ($b$ odd):**
     $$X = b(b + 4a)^3, \qquad Y = 4a(a - 2b)^3$$
     
   - **Even $b$ branch ($b$ even, $a$ odd):**
     $$X = 2b\left(\frac{b}{2} + 2a\right)^3, \qquad Y = a(a - 2b)^3$$

2. Multipliers:
   Every valid nested radical pair $(x, y)$ is obtained from one of these primitive seeds $(X, Y)$ scaled by an arbitrary square multiplier $t^2$:
   $$(x, y) = (t^2 X, t^2 Y), \qquad 1 \le t \le \left\lfloor \sqrt{\frac{N}{\max(|X|, |Y|)}} \right\rfloor$$
   Sum of multipliers: $\sum_{t=1}^{t_{\max}} t^2 = \frac{t_{\max}(t_{\max}+1)(2t_{\max}+1)}{6}$.

3. Rational Cube Exclusion:
   $x/y$ is a cube of a rational number if and only if the cube-free kernels match:
   - For odd $b$: $\operatorname{cf}(b) = \operatorname{cf}(4a)$
   - For even $b$: $\operatorname{cf}(2b) = \operatorname{cf}(a)$
   where $\operatorname{cf}(n) = \prod_p p^{v_p(n) \bmod 3}$ is precomputed via a smallest prime factor (SPF) sieve.

4. Complexity:
   - SPF sieve up to $\max(4a, 2b) = O(N^{1/3})$.
   - $b \le (4N)^{1/4} \approx 7952$.
   - For each $b$, $a \le \frac{(N/b)^{1/3} - b}{4}$.
   - Overall time complexity is $O(N^{3/8})$, running in ~10 seconds.
"""

import math
import unittest
from util.utils import timeit


class Problem880:
    def __init__(self):
        pass

    @staticmethod
    def _icbrt(n: int) -> int:
        """Floor integer cube root for n >= 0."""
        if n <= 1:
            return n
        r = int(round(n ** (1.0 / 3.0)))
        while (r + 1) ** 3 <= n:
            r += 1
        while r**3 > n:
            r -= 1
        return r

    @staticmethod
    def _iroot4(n: int) -> int:
        """Floor integer fourth root for n >= 0."""
        r = math.isqrt(math.isqrt(n))
        while (r + 1) ** 4 <= n:
            r += 1
        while r**4 > n:
            r -= 1
        return r

    @staticmethod
    def _cube_free_table(limit: int) -> list[int]:
        """Return cf[n] = product p^(v_p(n) mod 3) for 0 <= n <= limit."""
        spf = list(range(limit + 1))
        if limit >= 1:
            spf[1] = 1

        for p in range(2, math.isqrt(limit) + 1):
            if spf[p] != p:
                continue
            for m in range(p * p, limit + 1, p):
                if spf[m] == m:
                    spf[m] = p

        cf = [1] * (limit + 1)
        for n in range(2, limit + 1):
            p = spf[n]
            m = n // p
            e = 1
            while m % p == 0:
                m //= p
                e += 1

            rem = e % 3
            if rem == 0:
                cf[n] = cf[m]
            elif rem == 1:
                cf[n] = cf[m] * p
            else:
                cf[n] = cf[m] * p * p
        return cf

    @staticmethod
    def _sumsq(k: int) -> int:
        """1^2 + 2^2 + ... + k^2."""
        return k * (k + 1) * (2 * k + 1) // 6

    @timeit
    def solve(self, N: int = 10**15, mod: int = 1031**3 + 2) -> int:
        b_limit = self._iroot4(4 * N)

        max_odd_a = max(0, (self._icbrt(N) - 1) // 4)
        max_even_a = max(0, (self._icbrt(N // 4) - 1) // 2)
        cf_limit = max(4 * max_odd_a, max_even_a, 2 * b_limit)
        cf = self._cube_free_table(cf_limit)
        cf4 = [0] * (max_odd_a + 1)
        for a in range(1, max_odd_a + 1):
            cf4[a] = cf[4 * a]

        total = 0
        gcd = math.gcd
        isqrt = math.isqrt
        icbrt_local = self._icbrt
        sumsq_local = self._sumsq

        # Branch 1: Odd b
        for b in range(1, b_limit + 1, 2):
            a_limit = (icbrt_local(N // b) - b) // 4
            cf_b = cf[b]
            for a in range(1, a_limit + 1):
                if gcd(a, b) != 1 or cf_b == cf4[a]:
                    continue

                x_base = b + 4 * a
                x = b * x_base * x_base * x_base
                y_base = a - 2 * b
                y_abs = abs(4 * a * y_base * y_base * y_base)
                max_coord = x if x >= y_abs else y_abs
                if max_coord > N:
                    continue

                tmax = isqrt(N // max_coord)
                total = (total + (x + y_abs) * sumsq_local(tmax)) % mod

        # Branch 2: Even b (a must be odd for gcd(a, b) == 1)
        for b in range(2, b_limit + 1, 2):
            half_b = b // 2
            a_limit = (icbrt_local(N // (2 * b)) - half_b) // 2
            cf_2b = cf[2 * b]
            for a in range(1, a_limit + 1, 2):
                if gcd(a, b) != 1 or cf_2b == cf[a]:
                    continue

                x_base = half_b + 2 * a
                x = 2 * b * x_base * x_base * x_base
                y_base = a - 2 * b
                y_abs = abs(a * y_base * y_base * y_base)
                max_coord = x if x >= y_abs else y_abs
                if max_coord > N:
                    continue

                tmax = isqrt(N // max_coord)
                total = (total + (x + y_abs) * sumsq_local(tmax)) % mod

        return total


class Solution880(unittest.TestCase):
    def setUp(self):
        self.problem = Problem880()

    def test_sample_1000(self):
        self.assertEqual(2535, self.problem.solve(10**3))

    def test_sample_10000(self):
        self.assertEqual(192635, self.problem.solve(10**4))

    def test_sample_100000(self):
        self.assertEqual(9899943, self.problem.solve(10**5))

    def test_solution(self):
        self.assertEqual(522095328, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
