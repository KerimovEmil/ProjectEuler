r"""
PROBLEM

The Gauss Factorial of a number $n$ is defined as the product of all positive numbers $\leq n$ that are relatively prime to $n$.
For example $g(10) = 1 \times 3 \times 7 \times 9 = 189$.

Also we define
$$\displaystyle G(n) = \prod_{i=1}^{n} g(i)$$

You are given $G(10) = 23044331520000$.

Find $G(10^8)$. Give your answer modulo $1\,000\,000\,007$.

ANSWER: 785845900
Solve time: ~50 seconds

---
MATHEMATICAL DERIVATION:

1. Problem Definition:
   The Gauss Factorial g(n) is defined as:
     g(n) = prod_{1 <= k <= n, gcd(k, n) == 1} k

   We want to compute the cumulative product G(N):
     G(N) = prod_{n = 1..N} g(n)  (mod 10^9 + 7)
          = prod_{n = 1..N} prod_{1 <= k <= n, gcd(k, n) == 1} k  (mod 10^9 + 7)

2. Inverting the Order of Multiplication (Base-Centric Perspective):
   Instead of computing each g(n) separately and multiplying them, we determine
   how many times each integer k in {1, 2, ..., N} appears as a factor in G(N).

   An integer k is included in g(n) if and only if k <= n and gcd(k, n) == 1.
   Therefore, the exponent of k in G(N) is the count of integers n in [k, N]
   that are coprime to k:
     E(k) = count(n in [k, N] such that gcd(k, n) == 1)

   Writing n = k + j with 0 <= j <= N - k:
     gcd(k, k + j) = gcd(k, j)

   For k > 1, j = 0 gives gcd(k, 0) = k > 1, so j ranges over 1 <= j <= N - k.
   (For k = 1, base 1 contributes 1^E(1) = 1 regardless).

   By inclusion-exclusion using the Mobius function mu:
     E(k) = sum_{d | k} mu(d) * floor((N - k) / d)

3. Divisor Expansion and Factoring the Product:
   Expressing G(N) in terms of these exponents:
     G(N) = prod_{k = 1..N} k^E(k)
          = prod_{k = 1..N} prod_{d | k} k^(mu(d) * floor((N - k) / d))

   Let k = d * m. As d ranges from 1 to N, m ranges from 1 to L = floor(N / d):
     floor((N - d * m) / d) = floor(N / d) - m = L - m

   Substituting k = d * m:
     G(N) = prod_{d = 1..N} prod_{m = 1..L} (d * m)^(mu(d) * (L - m))

   Separating the base into d and m:
     - Part 1 (Base d):
       sum_{m = 1..L} (L - m) = L * (L - 1) / 2
       P1 = prod_{d = 1..N} d^(mu(d) * L * (L - 1) / 2)

     - Part 2 (Base m):
       prod_{m = 1..L} m^(L - m) = 1^(L-1) * 2^(L-2) * ... * (L-1)^1
                                 = prod_{j = 1..L-1} j!
                                 = sf(L - 1)
       P2 = prod_{d = 1..N} sf(L - 1)^mu(d)

       where sf(k) = prod_{j = 1..k} j! is the superfactorial (OEIS A000178).

   Combining both parts yields:
     G(N) = prod_{d = 1..N} [ d^(L * (L - 1) / 2) * sf(L - 1) ]^mu(d)
   where L = floor(N / d).

4. Hyperbola / Quotient-Block Grouping:
   - For d > floor(N / 2):
     L = floor(N / d) = 1, so L * (L - 1) / 2 = 0 and sf(0) = 1.
     Thus, every d > floor(N / 2) contributes d^0 * 1^mu(d) = 1.
     We only need to evaluate d up to floor(N / 2)!

   - For d = 1:
     L = N, which contributes 1^(mu(1) * N * (N - 1) / 2) * sf(N - 1)^mu(1) = sf(N - 1).

   - For 2 <= d <= floor(N / 2):
     The quotient q = floor(N / d) is constant over contiguous intervals of d.
     Within each interval where q is constant:
       * The base product factors into numbers with mu(d) = +1 and mu(d) = -1:
           (pos_product)^(q * (q - 1) / 2) * (neg_product)^(-q * (q - 1) / 2)
       * The superfactorial term sf(q - 1) is raised to the sum of mu(d) over that interval:
           sf(q - 1)^(sum mu(d))

5. Efficient Implementation:
   - Sieve & Aggregation: A linear sieve up to N / 2 = 5 * 10^7 finds primes and
     accumulates interval products in O(N) operations.
   - Superfactorial Evaluation: A single running pass computes the factorials and
     superfactorials, saving values only at the required O(sqrt(N)) ~ 20,000 block boundaries.
   - Modular Exponentiation: Performed only once per quotient block (O(sqrt(N)) calls total),
     entirely avoiding 10^8 separate exponentiations.
   - Total runtime is ~50 seconds in pure Python.
"""

import unittest

from util.utils import timeit


class Problem754:
    def __init__(self, limit: int = 10**8, mod: int = 1000000007):
        self.limit = limit
        self.mod = mod

    def compute_G(self, n: int) -> int:
        if n <= 1:
            return 1

        mod = self.mod
        exp_mod = mod - 1
        half_n = n // 2

        # Linear sieve up to half_n to compute mu and interval aggregates
        mu = bytearray(half_n + 1)
        mu[1] = 1
        composite = bytearray(half_n + 1)
        primes: list[int] = []

        aggregates: list[tuple[int, int, int, int]] = []

        lo = 2
        q = n // lo
        hi = n // q
        pos_product = 1
        neg_product = 1
        mu_sum = 0

        for x in range(2, half_n + 1):
            if not composite[x]:
                primes.append(x)
                mux = 2
                mu[x] = mux
            else:
                mux = mu[x]

            if mux == 1:
                pos_product = (pos_product * x) % mod
                mu_sum += 1
            elif mux == 2:
                neg_product = (neg_product * x) % mod
                mu_sum -= 1

            for p in primes:
                y = x * p
                if y > half_n:
                    break
                composite[y] = 1
                if x % p == 0:
                    break
                if mux:
                    mu[y] = 3 - mux

            if x == hi:
                aggregates.append((q, pos_product, neg_product, mu_sum))
                lo = hi + 1
                if lo > half_n:
                    break
                q = n // lo
                hi = n // q
                pos_product = 1
                neg_product = 1
                mu_sum = 0

        # Determine all required superfactorial keys: (q - 1) for all blocks, plus (n - 1)
        needed_keys = set(q - 1 for q, _, _, _ in aggregates)
        needed_keys.add(n - 1)
        keys = sorted(needed_keys)

        values: dict[int, int] = {}
        factorial = 1
        superfactorial = 1
        x = 0
        if keys and keys[0] == 0:
            values[0] = 1
            keys = keys[1:]

        for target in keys:
            for x in range(x + 1, target + 1):
                factorial = (factorial * x) % mod
                superfactorial = (superfactorial * factorial) % mod
            values[target] = superfactorial

        # Accumulate final product: d = 1 contributes sf(n - 1)
        result = values[n - 1]
        for q, pos_product, neg_product, mu_sum in aggregates:
            exponent = q * (q - 1) // 2 % exp_mod
            if exponent:
                result = (result * pow(pos_product, exponent, mod)) % mod
                result = (result * pow(neg_product, (-exponent) % exp_mod, mod)) % mod

            sf_power = mu_sum % exp_mod
            if sf_power:
                result = (result * pow(values[q - 1], sf_power, mod)) % mod

        return result

    @timeit
    def solve(self) -> int:
        return self.compute_G(self.limit)


class Solution754(unittest.TestCase):
    def setUp(self):
        self.problem = Problem754()

    def test_samples(self):
        self.assertEqual(331358692, self.problem.compute_G(10))
        self.assertEqual(557051244, self.problem.compute_G(10**6))

    def test_solution(self):
        self.assertEqual(785845900, self.problem.solve())


if __name__ == "__main__":
    unittest.main()
