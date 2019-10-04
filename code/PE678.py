"""
PROBLEM

If a triple of positive integers (a,b,c) satisfies a2+b2=c2, it is called a Pythagorean triple.
No triple (a,b,c) satisfies ae+be=ce when e≥3 (Fermat's Last Theorem). However, if the exponents of the left-hand side
 and right-hand side differ, this is not true. For example, 3^3+6^3=3^5.

Let a,b,c,e,f be all positive integers, 0<a<b, e≥2, f≥3 and c^f≤N.
Let F(N) be the number of (a,b,c,e,f) such that a^e+b^e=c^f. You are given F(10^3)=7, F(10^5)=53 and F(10^7)=287.

Find F(10^18).

ANSWER:
????
Solve time ~???? seconds
"""

# Problem
# a^e + b^e = c^f, for 0 < a < b, e>= 2, f>=3, c^f <= 10^18
#
# https://www.science20.com/vastness_ways_science/parcelatories_powers_equations_fermats_last_theorem
# e and f need to be co-prime

# BEAL'S CONJECTURE:  If A^x + B^y = C^z, where A, B, C, x, y and z are positive integers
# and x, y and z are all greater than 2, then A, B and C must have a common prime factor.


from util.utils import timeit, is_coprime
import unittest


class Problem678:
    def __init__(self, n):
        self.n = n

    @timeit
    def solve(self):
        answer = 0
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        for c in range(2, round(self.n**(1/3))+1):
            f = 3
            while c**f <= self.n:
                answer += self.check_if_sum_of_powers(round(c**f), c, f)
                f += 1
        return answer

    @staticmethod
    def check_if_sum_of_powers(limit, c, f):
        """Returns how many a^e + b^e = limit, for a < b. Where limit = c^f"""
        count = 0
        for a in range(1, round((limit/2)**0.5)+1):  # way too many
            for b in range(a+1, round((limit - a**2)**0.5 + 1)):  # way too many
                e = 2  # e must be either 2 or coprime to f
                fermat_sum = round(a**e + b**e)
                while fermat_sum < limit:
                    e += 1
                    fermat_sum = round(a**e + b**e)
                if fermat_sum == limit:
                    count += 1
                    print("a:{}, b:{}, e:{}, c:{}, f:{} , a^e + b^e:{}".format(a, b, e, c, f, a**e + b**e))
                    # print(primes_of_n(limit))
        return count


class Solution678(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem678(n=int(1e3))
        pass

    # def test_solution(self):
    #     # Fill this in once you've got a working solution!
    #     self.assertEqual(1, self.problem.solve())

    def test_smallest_solution(self):
        problem = Problem678(n=int(1e3))
        self.assertEqual(7, problem.solve())

    def test_small_solution(self):
        problem = Problem678(n=int(1e5))
        self.assertEqual(53, problem.solve())

    # def test_big_sample_solution(self):
    #     problem = Problem678(n=int(1e7))
    #     self.assertEqual(287, problem.solve())


if __name__ == '__main__':
    unittest.main()
