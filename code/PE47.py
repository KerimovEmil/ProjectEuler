# The first two consecutive numbers to have two distinct prime factors are:

# 14 = 2 * 7
# 15 = 3 * 5

# The first three consecutive numbers to have three distinct prime factors are:

# 644 = 2*2 * 7 * 23
# 645 = 3 * 5 * 43
# 646 = 2 * 17 * 19.

# Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?

# Answer = 134043

from util.utils import sieve
from util.utils import timeit


class Problem47:
    @timeit
    def __init__(self, max_prime, consec_n, min_int, max_int):
        self.consec_n = consec_n
        self.min_int = min_int
        self.max_int = max_int
        self.P = list(sieve(max_prime))

        self.ans = None

    def div(self, num, d_primes):
        """Returns True if the input number (num) has exactly D unique prime divisors."""
        count = 0
        # if num in self.P:
        #     return False
        for prime in self.P:
            if prime > num:
                return count == d_primes
            if num % prime == 0:
                count += 1
                if count > d_primes:
                    return False
            while num % prime == 0:
                num /= prime
            if num == 1:
                return count == d_primes

        return count == d_primes

    @timeit
    def solve(self):
        counter = 0
        for num in range(self.min_int, self.max_int):
            if self.div(num, self.consec_n):
                counter += 1
                if counter == self.consec_n:
                    self.ans = num - self.consec_n + 1
                    break
            else:
                counter = 0
        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    obj = Problem47(max_prime=100000, consec_n=4, min_int=100000, max_int=150000)
    sol = obj.solve()
    print(sol)

