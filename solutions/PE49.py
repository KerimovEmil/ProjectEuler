# The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways:
# (i) each of the three terms are prime, and,
# (ii) each of the 4-digit numbers are permutations of one another.

# There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property,
# but there is one other 4-digit increasing sequence.

# What 12-digit number do you form by concatenating the three terms in this sequence?

# Answer: 2969, 6299, 9629 : 296962999629

from util.utils import sieve
from util.utils import timeit


class Problem49:
    def __init__(self, exclude, n):
        self.exclude = exclude
        self.n = n
        self.ans = None

    @timeit
    def solve(self):
        max_prime = int(10**self.n)
        min_prime = int(10**(self.n-1))

        P = list(sieve(max_prime))  # all primes less than 10000
        P2 = list(sieve(min_prime))
        T = P[len(P2):]  # remove primes less than 1000
        Q = set(T)
        U = []
        for x in T:
            for i in range(1, int(max_prime/2)):
                if ((x + i) in Q) and ((x + 2 * i) in Q):
                    if set(str(x)) == set(str(x + i)):
                        if set(str(x)) == set(str(x + 2 * i)):
                            U.append(x)
                            U.append(x + i)
                            U.append(x + 2 * i)

        ls_sol = [str(x) for x in U if x not in self.exclude]

        self.ans = ''.join(ls_sol)

        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    exclude = {1487, 4817, 8147}
    n = 4
    obj = Problem49(exclude=exclude, n=n)
    sol = obj.solve()
    print(sol)
