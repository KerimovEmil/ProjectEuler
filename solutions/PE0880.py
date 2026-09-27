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

ANSWER: 820774119
Solve time: ~220 seconds

---
MATHEMATICAL DERIVATION:

1. Algebraic Denesting Condition:
   Squaring both sides of $\sqrt{\sqrt[3]{x} + \sqrt[3]{y}} = \sqrt[3]{a} + \sqrt[3]{b} + \sqrt[3]{c}$:
   $$\sqrt[3]{x} + \sqrt[3]{y} = (\sqrt[3]{a} + \sqrt[3]{b} + \sqrt[3]{c})^2$$
   $$= a^{2/3} + b^{2/3} + c^{2/3} + 2(ab)^{1/3} + 2(bc)^{1/3} + 2(ca)^{1/3}$$
   For these 6 cross-terms to collapse into a two-term sum of cube roots $\sqrt[3]{x} + \sqrt[3]{y}$ without $x/y$ being a rational cube, the radicals $\sqrt[3]{a}, \sqrt[3]{b}, \sqrt[3]{c}$ must reside in a degree-9 bivariate field extension $\mathbb{Q}(u, v)$ where $u^3 = U, v^3 = V$.
   Setting $\alpha = -u, \beta = u^2 v, \gamma = v^2$:
   $$(\alpha + \beta + \gamma)^2 = u^2(1 + 2V) + u v^2(U - 2) + v(V - 2U)$$
   The cross-term $u v^2(U - 2)$ vanishes identically if and only if $U = 2$.
   When $U = 2$, this collapses to:
   $$(-u + u^2 v + v^2)^2 = 2^{2/3}(2V + 1) + V^{1/3}(V - 4) = \sqrt[3]{4(2V + 1)^3} + \sqrt[3]{V(V - 4)^3}$$

2. Coprime Rational Parametrization:
   Let $V = p/q$ with $\gcd(p, q) = 1, q \ge 1, p \ne 0$.
   To ensure $a, b, c$ are integers, we scale the basis elements by $q$:
   $$\alpha = -q \sqrt[3]{2} \implies a = \alpha^3 = -2 q^3$$
   $$\beta = 2^{2/3} p^{1/3} q^{2/3} \implies b = \beta^3 = 4 p q^2$$
   $$\gamma = p^{2/3} q^{1/3} \implies c = \gamma^3 = p^2 q$$
   The resulting squared sum yields integer components:
   $$X_0 = 4 q^3 (2p + q)^3$$
   $$Y_0 = p q^2 (p - 4q)^3$$
   Any integer scaling of $(a, b, c) \to k (a, b, c)$ scales their cube roots by $k^{1/3}$, and squaring scales the components by $k^2$:
   $$(x, y) = (k^2 X_0, k^2 Y_0)$$

3. Rational Cube Exclusion:
   $x/y$ is a cube of a rational number if and only if:
   $$\frac{X_0}{Y_0} = \frac{4 q (2p + q)^3}{p (p - 4q)^3} \iff \frac{4q}{p} \text{ is a rational cube} \iff 4 q p^2 \text{ is an integer cube}$$
   Pairs where $4 q p^2$ is a perfect cube are excluded.

4. Dual Involutive Symmetry and Primitive Bases:
   The ratio map $f(t) = \frac{Y_0}{X_0} = \frac{t}{4}\left(\frac{t-4}{2t+1}\right)^3$ satisfies the involutive dual symmetry:
   $$f(-2/t) = \frac{1}{f(t)}$$
   Thus $t = p/q \longleftrightarrow t' = -2/t = -2q/p$ swaps $X_0$ and $Y_0$.
   Let $g = \gcd(2, |p|)$ and $(p_2, q_2) = (-2q/g, p/g)$.
   The base pairs from $(p, q)$ and $(p_2, q_2)$ are multiples of a common primitive base $(X_{\text{prim}}, Y_{\text{prim}})$:
   - If $p$ is odd, $q$ is odd: $u = 2|p|, v = q$, $X_{\text{prim}} = 4q(2p+q)^3, Y_{\text{prim}} = p(p-4q)^3$.
   - If $p$ is odd, $q$ is even: $u = |p|, v = q/2$, $X_{\text{prim}} = 16q(2p+q)^3, Y_{\text{prim}} = 4p(p-4q)^3$.
   - If $p \equiv 2 \pmod 4$, $q$ is odd: $u = |p|/2, v = 2q$, $X_{\text{prim}} = q(2p+q)^3, Y_{\text{prim}} = \frac{p}{4}(p-4q)^3$.
   - If $p \equiv 0 \pmod 4$, $q$ is odd: $u = |p|/4, v = q$, $X_{\text{prim}} = 4q(2p+q)^3, Y_{\text{prim}} = p(p-4q)^3$.

   To prevent double-counting dual orbits, we choose the canonical representative satisfying:
   $$q < q_2 \quad \text{or} \quad (q = q_2 \text{ and } p \le p_2)$$

5. Multiplier Counting via Inclusion-Exclusion:
   For a primitive base with $M_{\text{prim}} = \max(|X_{\text{prim}}|, |Y_{\text{prim}}|) \le N$, the valid multipliers $k \le K = \lfloor \sqrt{N / M_{\text{prim}}} \rfloor$ are integers where $u \mid k$ or $v \mid k$.
   By the Principle of Inclusion-Exclusion, the sum of $k^2$ for valid $k \le K$ is:
   $$\Sigma(K) = u^2 S\left(\left\lfloor \frac{K}{u} \right\rfloor\right) + v^2 S\left(\left\lfloor \frac{K}{v} \right\rfloor\right) - (uv)^2 S\left(\left\lfloor \frac{K}{uv} \right\rfloor\right)$$
   where $S(m) = \sum_{j=1}^m j^2 = \frac{m(m+1)(2m+1)}{6}$.
   The contribution to $H(N)$ from this orbit is:
   $$(|X_{\text{prim}}| + |Y_{\text{prim}}|) \cdot \Sigma(K) \pmod{1031^3 + 2}$$

6. Complexity Analysis:
   - Outer loop over $q \le (4N)^{1/4} \approx 7952$.
   - Inner loop over $p$ with $|p| \le (4N / q^2)^{1/4}$.
   - Total number of candidate parameter pairs is $O(N^{3/8}) \approx 4 \times 10^6$.
   - Space Complexity: $O(1)$ auxiliary memory.
"""

import math
import unittest
from util.utils import timeit


class Problem880:
    def __init__(self):
        pass

    @staticmethod
    def _sum_sq_mod(n: int, mod: int) -> int:
        """Compute sum_{j=1}^n j^2 mod mod."""
        return (n * (n + 1) * (2 * n + 1) // 6) % mod

    @timeit
    def solve(self, N: int = 10**15, mod: int = 1031**3 + 2) -> int:
        """
        Compute H(N) mod mod using coprime parameter generation and inclusion-exclusion.
        """
        total_H = 0
        max_q = int((4 * N)**0.25) + 10

        for q in range(1, max_q + 1):
            q_is_odd = (q % 2 != 0)

            # Positive p
            p = q
            while True:
                if not q_is_odd and p % 2 == 0:
                    p += 1
                    continue
                if q_is_odd and p % 2 == 0 and p < 2 * q:
                    p += 1
                    continue
                if 2 * p + q == 0 or p - 4 * q == 0:
                    p += 1
                    continue
                if math.gcd(p, q) != 1:
                    p += 1
                    continue

                # Dual canonical check
                g = 2 if p % 2 == 0 else 1
                p2, q2 = -2 * q // g, p // g
                if q2 < 0:
                    p2, q2 = -p2, -q2

                if q > q2 or (q == q2 and p > p2):
                    p += 1
                    continue

                # Rational cube exclusion
                val = 4 * q * p * p
                cr = round(val**(1 / 3))
                if cr * cr * cr == val:
                    p += 1
                    continue

                t_2p_q = 2 * p + q
                t_2p_q_3 = t_2p_q * t_2p_q * t_2p_q
                t_p_4q = p - 4 * q
                t_p_4q_3 = t_p_4q * t_p_4q * t_p_4q

                if p % 2 != 0:
                    if q_is_odd:
                        u, v = 2 * p, q
                        X_prim = 4 * q * t_2p_q_3
                        Y_prim = p * t_p_4q_3
                    else:
                        u, v = p, q // 2
                        X_prim = 16 * q * t_2p_q_3
                        Y_prim = 4 * p * t_p_4q_3
                else:
                    if (p // 2) % 2 != 0:
                        u, v = p // 2, 2 * q
                        X_prim = q * t_2p_q_3
                        Y_prim = (p * t_p_4q_3) // 4
                    else:
                        u, v = p // 4, q
                        X_prim = 4 * q * t_2p_q_3
                        Y_prim = p * t_p_4q_3

                M_prim = max(abs(X_prim), abs(Y_prim))
                if M_prim > N:
                    if p > 4 * q:
                        break
                    p += 1
                    continue

                S_prim = (abs(X_prim) + abs(Y_prim)) % mod
                K = int(math.isqrt(N // M_prim))

                if (p, q) == (p2, q2):
                    k_sq_sum = self._sum_sq_mod(K, mod)
                else:
                    term1 = (pow(u, 2, mod) * self._sum_sq_mod(K // u, mod)) % mod
                    term2 = (pow(v, 2, mod) * self._sum_sq_mod(K // v, mod)) % mod
                    term3 = (pow(u * v, 2, mod) * self._sum_sq_mod(K // (u * v), mod)) % mod
                    k_sq_sum = (term1 + term2 - term3) % mod

                total_H = (total_H + S_prim * k_sq_sum) % mod
                p += 1

            # Negative p
            p = -q
            while True:
                abs_p = -p
                if not q_is_odd and abs_p % 2 == 0:
                    p -= 1
                    continue
                if q_is_odd and abs_p % 2 == 0 and abs_p < 2 * q:
                    p -= 1
                    continue
                if 2 * p + q == 0 or p - 4 * q == 0:
                    p -= 1
                    continue
                if math.gcd(abs_p, q) != 1:
                    p -= 1
                    continue

                g = 2 if abs_p % 2 == 0 else 1
                p2, q2 = -2 * q // g, p // g
                if q2 < 0:
                    p2, q2 = -p2, -q2

                if q > q2 or (q == q2 and p > p2):
                    p -= 1
                    continue

                val = 4 * q * abs_p * abs_p
                cr = round(val**(1 / 3))
                if cr * cr * cr == val:
                    p -= 1
                    continue

                t_2p_q = 2 * p + q
                t_2p_q_3 = t_2p_q * t_2p_q * t_2p_q
                t_p_4q = p - 4 * q
                t_p_4q_3 = t_p_4q * t_p_4q * t_p_4q

                if abs_p % 2 != 0:
                    if q_is_odd:
                        u, v = 2 * abs_p, q
                        X_prim = 4 * q * t_2p_q_3
                        Y_prim = p * t_p_4q_3
                    else:
                        u, v = abs_p, q // 2
                        X_prim = 16 * q * t_2p_q_3
                        Y_prim = 4 * p * t_p_4q_3
                else:
                    if (abs_p // 2) % 2 != 0:
                        u, v = abs_p // 2, 2 * q
                        X_prim = q * t_2p_q_3
                        Y_prim = (p * t_p_4q_3) // 4
                    else:
                        u, v = abs_p // 4, q
                        X_prim = 4 * q * t_2p_q_3
                        Y_prim = p * t_p_4q_3

                M_prim = max(abs(X_prim), abs(Y_prim))
                if M_prim > N:
                    break

                S_prim = (abs(X_prim) + abs(Y_prim)) % mod
                K = int(math.isqrt(N // M_prim))

                if (p, q) == (p2, q2):
                    k_sq_sum = self._sum_sq_mod(K, mod)
                else:
                    term1 = (pow(u, 2, mod) * self._sum_sq_mod(K // u, mod)) % mod
                    term2 = (pow(v, 2, mod) * self._sum_sq_mod(K // v, mod)) % mod
                    term3 = (pow(u * v, 2, mod) * self._sum_sq_mod(K // (u * v), mod)) % mod
                    k_sq_sum = (term1 + term2 - term3) % mod

                total_H = (total_H + S_prim * k_sq_sum) % mod
                p -= 1

        return total_H


class Solution880(unittest.TestCase):
    def setUp(self):
        self.problem = Problem880()

    def test_sample_1000(self):
        self.assertEqual(2535, self.problem.solve(10**3))

    def test_sample_10000(self):
        self.assertEqual(143227, self.problem.solve(10**4))

    def test_solution(self):
        self.assertEqual(820774119, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
