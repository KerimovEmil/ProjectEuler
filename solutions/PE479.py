"""
PROBLEM
Let a_k, b_k and c_k represent the three solutions (real or complex numbers) to the equation
1/x = (k/x)^2 (k+x^2) -kx

For instance, for k=5, we see that {a_5, b_5, c_5} is approximately
{5.727244 , (-0.363622 + 2.057397j) , (-0.363622 - 2.057397j)}.

Let
S(n) = sum_{p=1}^n sum_{k=1}^n (a_k + b_k)^p (a_k + c_k)^p (b_k + c_k)^p

Interestingly, S(n) is always an integer. For example, S(4)=51160

Find S(10^6) modulo 1,000,000,007

ANSWER: 191541795
Solve time ~6 s
"""

# re-arrange 1/x = (k/x)^2 (k+x^2) -kx to
# x^3 - (a+b+c)x^2 + (ab+ac+bc)x - abc = 0

# therefore:
# a_k + b_k + c_k = k
# a_k * b_k + a_k * c_k + b_k * c_k = 1/k
# a_k * b_k * c_k = k^2

# observe (a_k + b_k) * (a_k + c_k) * (b_k + c_k) can be re-arranged to
# (a_k + b_k + c_k) * (a_k*b_k + a_k*c_k + b_k*c_k) - a_k*b_k*c_k
# = k(1/k) - k^2
# = 1 - k^2

# therefore S(n) = sum_{p=1}^n sum_{k=1}^n (1-k^2)^p
# by taking the sum over p first, we get:
# S(n) = sum_{k=1}^n (k^2 - 1) * ((1-k^2)^n - 1) / k^2

# expanding the binomial expansion to combine terms, we get
# S(n) = n^2 + (-1)^n sum_{k=1}^n k^{2n} + sum_{k=1}^n sum_{q=1}^{n-1} (-1)^q (n+1, q+1) k^{2q}
# re-writing in terms of expansions of n+1 we get:
# S(n) = -n + sum_{k=1}^n (1 - (1-k^2)^{n+1}) / k^2


from util.utils import timeit
import unittest


class Problem479:
    def __init__(self, m):
        self.m = m

    @timeit
    def solve(self, n):
        r = (-n) % self.m
        r += sum(
            ((1 - pow(1 - pow(k, 2, self.m), n + 1, self.m)) * pow(k, -2, self.m)) % self.m
            for k in range(1, n + 1)) % self.m
        return r % self.m


class Solution479(unittest.TestCase):
    def setUp(self):
        self.problem = Problem479(m=1_000_000_007)

    def test_solution(self):
        self.assertEqual(191541795, self.problem.solve(n=int(1e6)))


if __name__ == '__main__':
    unittest.main()

