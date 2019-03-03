"""
PROBLEM

Consider the number 3600. It is very special, because

3600 = 48^2 +   36^2
3600 = 20^2 + 2×40^2
3600 = 30^2 + 3×30^2
3600 = 45^2 + 7×15^2

Similarly, we find that 88201 = 99^2 + 280^2 = 287^2 + 2×54^2 = 283^2 + 3×52^2 = 197^2 + 7×84^2.

In 1747, Euler proved which numbers are representable as a sum of two squares.
We are interested in the numbers n which admit representations of all of the following four types:

n = a_1^2 +   b_1^2
n = a_2^2 + 2×b_2^2
n = a_3^2 + 3×b_3^2
n = a_7^2 + 7×b_7^2,
where the a_k and b_k are positive integers.

There are 75373 such numbers that do not exceed 10^7.
How many such numbers are there that do not exceed 2×10^9?

ANSWER:

Solve time ~  seconds
"""

from util.utils import timeit
import unittest


# Extending the number field of the reals with a field extension of sqrt(D), n = a + b sqrt(D)
# such that Norm(a + b sqrt(D)) = a^2 - D×b^2
# Note that there are only the following negative D for which the resulting field is a principal ideal domain (PID)
# D = −1, −2, −3, −7, −11, −19, −43, −67, −163
# However only the field extensions of D = −1, −2, −3, −7, −11 are Euclidean domains.
# The remaining fields, D = −19, −43, −67, −163 are rare examples of PID's that are not Euclidean domains

# For reference: commutative rings ⊃ integral domains ⊃ integrally closed domains ⊃ GCD domains ⊃
# unique factorization domains (UFD) ⊃ principal ideal domains (PID) ⊃ Euclidean domains ⊃ fields ⊃ finite fields

# For reference: the only D's for which the field extension is a Euclidean domain are
# D = −11, -7, -3, -2, −1, 2, 3, 5, 6, 7, 11, 13, 17, 19, 21, 29, 33, 37, 41, 57, 73

# Using the Legendre symbol (-1/p) = {1 if p==1 mod 4, -1 if p==3 mod 4}
# In other words -1 has quadratic residues iff p == 1 mod 4,
# i.e. x^2 == -1 mod p has solutions for x iff p == 1 mod 4

# we can use legendre symbol arithmetic, (a/p)*(b/p) = (ab/p) to prove a lot more of these quadratic residues.
# We get:
# -1 has quadratic residues if p == 1 mod 4
# -2 has quadratic residues if p == 1,3 mod 8
# -3 has quadratic residues if p == 1 mod 3
# -7 has quadratic residues if p == 1,2,4 mod 7

# Therefore if p == 1 mod 4 AND p == 1,3 mod 8 AND p == 1 mod 3 AND p == 1,2,4 mod 7
# then x^2 == -1, -2, -3, -7  mod p has a solution.

# Note through all of this we assumed p was an odd prime.

# Example 3600: Divide out all of the powers of 2 and we get: 3600/16 = 225.
# 225 mod 4 = 1, 225 mod 8 = 1, 225 mod 7 = 1
# 225 mod 3 = 0 is a special case since 3 divides 225, and the legendre symbol arithmetic assumes they are coprime

# Example 88201:
# 88201 % 4 = 1, 88201 % 3 = 1, 88201 % 8 = 1, 88201 % 7 = 1

class Problem229:
    def __init__(self, max_n):
        self.max_n = max_n
        self.count = 0

    @staticmethod
    def legendre_neg1(n):
        if n % 4 == 1:
            return 1
        elif n % 4 == 3:
            return -1
        else:
            return 1


    @timeit
    def solve(self):
        # for i in range(1, self.max_n + 1, 2):  # only looping odd numbers
        for i in range(1, self.max_n + 1):
            highest_multiple_of_2 = i & -i

            k = i // highest_multiple_of_2

            cond1 = k % 4 == 1  # not needed

            cond2 = k % 8 == 1
            # cond3 = (i % 3 == 1) or i % 3 == 0
            cond3 = (k % 3 == 1)
            # cond4 = (i % 7 == 1) or i % 7 == 0
            cond4 = (k % 7 == 1)
            if cond1 and cond2 and cond3 and cond4:
                self.count += 1
        return self.count


class Solution229(unittest.TestCase):
    def setUp(self):
        self.problem_small = Problem229(max_n=int(1e7))

    def test_solution(self):
        self.assertEqual(75373, self.problem_small.solve())


if __name__ == '__main__':
    unittest.main()
