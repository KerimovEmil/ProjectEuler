"""
PROBLEM

Take a sequence of length n. Discard the first term then make a sequence of the partial summations.
Continue to do this over and over until we are left with a single term. We define this to be f(n).

Consider the example where we start with a sequence of length 8:
1,1,1,1,1,1,1,1
1,2,3,4,5,6,7
2,5,9,14,20,27
5,14,28,48,75
14,42,90,165
42,132,297
132,429
429

Then the final number is 429, so f(8)=429.

For this problem we start with the sequence 1,3,4,7,11,18,29,47, ...
This is the Lucas sequence where two terms are added to get the next term.
Applying the same process as above we get f(8)=2663.
You are also given f(20)=742296999 modulo 1,000,000,007

Find f(10^8). Give your answer modulo 1,000,000,007.

ANSWER: 711399016
Solve time: ~85 seconds

---
MATHEMATICAL DERIVATION:

1. Lattice Path & Catalan Transform:
   Let the initial sequence of length n be (x_0, x_1, ..., x_{n-1}).
   In the first step, x_0 is discarded and partial sums are computed.
   Because the entire process of discarding and partial summation is linear, the final
   single term is a linear combination of the initial terms:
       f(n) = sum_{k=1}^{n-1} c_{n, k} x_k
   (with c_{n, 0} = 0 since x_0 is immediately discarded).

   Each step corresponds to moving in a triangular lattice where each node is the sum
   of paths reaching it without crossing the diagonal y > x.
   By André's Reflection Principle / Ballot Theorem, the coefficient c_{n, k} is:
       c_{n, k} = C(2m - k - 1, m - 1) - C(2m - k - 1, m)
                = k / m * C(2m - k - 1, m - 1)
                = k / (2m - k) * C(2m - k, m)
   where m = n - 1.
   This operation mapping an input sequence to f(n) is the Catalan transform.

2. Sequence Evolution for Lucas Numbers:
   For x_k = L_k (with x_0 = 1, x_1 = 3, x_2 = 4, x_3 = 7, ...), we can express L_k in terms
   of Fibonacci numbers: L_k = F_{k-1} + 3*F_k.
   Thus:
       f(n+1) = sum_{k=0}^{n} k/(2n-k) * C(2n-k, n-k) * (F_{k-1} + 3*F_k)
       f(n+1) = sum_{k=0}^{n} k/(2n-k) * C(2n-k, n)   * (F_{k-1} + 3*F_k)
       f(n+1) = sum_{k=0}^{n} k/(n-1)  * C(2n-k-1, n-1) * (F_{k-1} + 3*F_k)

3. Connection to OEIS A081696 & P-Recursive Recurrence:
   The Catalan transform of the Fibonacci sequence yields the sequence a(n) (OEIS A081696):
       1, 1, 3, 9, 29, 97, 333, 1165, 4135, ...
   with generating function:
       G(x) = 1 / (x + sqrt(1 - 4x)) = (sqrt(1 - 4x) - x) / (1 - 4x - x^2)

   Since the Lucas sequence satisfies L_{k+1} = 2*F_{k+1} + F_k, our target value is:
       f(n+1) = 2*a(n) + a(n-1)

   The sequence a(n) satisfies the 3rd-order holonomic (P-recursive) recurrence:
       n * a(n) = 2*(4n - 3)*a(n-1) - 3*(5n - 8)*a(n-2) - 2*(2n - 3)*a(n-3)
   which factors as:
       n * a(n) = n*(8*a(n-1) - 15*a(n-2) - 4*a(n-3)) - 6*(a(n-1) - 4*a(n-2) - a(n-3))
   with initial conditions a(0) = 1, a(1) = 1, a(2) = 3.

4. Efficient O(N) Computation with Single Modular Inversion:
   To avoid computing modular inverses at each step k in [3, n-1], we scale the state by
   (k! / 2!) and maintain the denominator den = (n-1)! / 2! mod M.
   At the end of the loop, a single modular inversion via Fermat's Little Theorem gives:
       f(n) = (2*f2 + f1) * den^{M-2} mod M
   which runs in O(N) time and O(1) memory.
"""

from typing import List
import unittest
from util.utils import timeit, cumsum, fibonacci_n_term, catalan_transform, get_all_mod_inverse_list


# 1, 3, 4, 7, 11, 18, 29, 47
# 3, 7, 14, 25, 43, 72, 119
# 7, 21, 46, 89, 161, 280
# 21, 67, 156, 317, 597
# 67, 223, 540, 1137
# 223, 763, 1900
# 763, 2663
# 2663

# f(n) = 1, 3, 7, 21, 67, 223, 763, 2663, 9435

# 1  2   3      4      5         6        7            8           9
# a, b, a+b,   a+2b, 2a+3b,     3a+5b,   5a+8b,       8a+13b    13a+21b
#    b, a+2b, 2a+4b, 4a+7b,    7a+12b,  12a+20b,     20a+33b
#       a+2b, 3a+6b, 7a+13b,  14a+25b,  26a+45b,     46a+78b
#             3a+6b, 10a+19b, 24a+44b,  50a+89b,    96a+167b
#                    10a+19b, 34a+63b,  84a+152b,  180a+319b
#                             34a+63b,  118a+215b, 298a+534b
#                                       118a+215b, 416a+749b
#                                                  416a+749b
#                                                             1485a+2650b

# 1485 = (5+8) + 20 + 46 + 96 + 180 + 298 + 416*2
# 2650 = (8+13) + 33 + 78 + 167 + 319 + 534 + 749*2

# therefore we have the following sequence for f(n):
# n   f(n)
# 1    a
# 2    b
# 3   a+2b
# 4   3a+6b
# 5   10a+19b
# 6   34a+63b
# 7   118a+215b
# 8   416a+749b
# 9   1485a+2650b

# f(n+1) = sum_{k=0}^{k=n} k/(2n-k) * C(2n-k, n-k)   (F_{k-1} + 3*F_{k})
# f(n+1) = sum_{k=0}^{k=n} k/(2n-k) * C(2n-k, n)     (F_{k-1} + 3*F_{k})
# f(n+1) = sum_{k=0}^{k=n} k/(n-1)  * C(2n-k-1, n-1) (F_{k-1} + 3*F_{k})


class Problem739:
    def __init__(self, mod_n: int = 1000000007, a: int = 1, b: int = 3, debug: bool = False):
        self.mod_n = mod_n
        self.a = a
        self.b = b
        self.debug = debug

    @timeit
    def naive_solve(self, n: int, seq: List[int]) -> int:
        """Simulate the process of dropping the first term and taking partial sums."""
        for _ in range(n - 1):
            seq = cumsum(seq[1:])
        return seq[0]

    @timeit
    def solve_catalan_transform(self, n: int) -> int:
        """
        Compute f(n) using the Catalan transform formula with precomputed modular inverses.

        f(n+1) = sum_{k=0}^{n} k/(n-1) * C(2n-k-1, n-1) * (F_{k-1} + 3*F_k)
        """
        f1, f2 = 0, 1
        s, m = 0, n - 1

        if self.debug:
            print('computing inverses')
        ls_inv = get_all_mod_inverse_list(m=self.mod_n, max_n=m - 1)
        if self.debug:
            print('finished computing inverses')

        for k in range(1, m):
            s = (s * (2 * m - k) + k * (f1 + 3 * f2)) * ls_inv[m - k] % self.mod_n
            f1, f2 = f2, (f1 + f2) % self.mod_n

        return (s + f1 + 3 * f2) % self.mod_n

    @timeit
    def solve_recursive(self, n: int) -> int:
        """
        Compute f(n) modulo mod_n in O(n) time using the 3rd-order P-recursive relation for OEIS A081696.

        Recurrence:
        n * a(n) = 2*(4*n-3)*a(n-1) - 3*(5*n-8)*a(n-2) - 2*(2*n-3)*a(n-3)
                 = n*(8*a(n-1) - 15*a(n-2) - 4*a(n-3)) + 6*(4*a(n-2) - a(n-1) + a(n-3))

        With scaled variables to defer modular division to a single inverse at the end.
        """
        m = self.mod_n
        f0, f1, f2 = 1, 1, 3
        den = 1

        k = 3
        limit = n - 8
        while k <= limit:
            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

        while k < n:
            f0, f1, f2 = (k * f1) % m, (k * f2) % m, (k * (8 * f2 - 15 * f1 - 4 * f0) - 6 * (f2 - 4 * f1 - f0)) % m
            den = (den * k) % m
            k += 1

        f = (2 * f2 + f1) * pow(den, m - 2, m) % m
        return f

    @timeit
    def solve(self, n: int = 100000000) -> int:
        """Main solver entry point."""
        return self.solve_recursive(n)


class Solution739(unittest.TestCase):
    def setUp(self):
        self.problem = Problem739(mod_n=1000000007)

    def test_sample_solution(self):
        self.assertEqual(429, self.problem.naive_solve(n=8, seq=[1, 1, 1, 1, 1, 1, 1, 1]))

    def test_sample_solution_2(self):
        self.assertEqual(2663, self.problem.naive_solve(n=8, seq=[1, 3, 4, 7, 11, 18, 29, 47]))

    def test_catalan_fib_transform(self):
        ls_fib = [fibonacci_n_term(i) for i in range(7 + 1)]
        self.assertEqual(749, catalan_transform(n=7, seq=ls_fib))
        self.assertEqual(118, catalan_transform(n=5, seq=[f - 1 for f in ls_fib][2:]))

    def test_larger_solution(self):
        """f(20)=742296999 modulo 1,000,000,007"""
        self.assertEqual(742296999, self.problem.solve_recursive(n=20))

    def test_solution_1e3(self):
        self.assertEqual(537806289, self.problem.solve_recursive(n=int(1e3)))

    def test_solution_1e4(self):
        self.assertEqual(304246173, self.problem.solve_recursive(n=int(1e4)))

    def test_solution_1e5(self):
        self.assertEqual(587213414, self.problem.solve_recursive(n=int(1e5)))

    def test_solution_final(self):
        self.assertEqual(711399016, self.problem.solve(int(1e8)))


if __name__ == '__main__':
    unittest.main()
