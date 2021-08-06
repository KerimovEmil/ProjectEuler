# PROBLEM

# The prime 41, can be written as the sum of six consecutive primes:
# 41 = 2 + 3 + 5 + 7 + 11 + 13
# This is the longest sum of consecutive primes that adds to a prime
# below one-hundred.

# The longest sum of consecutive primes below one-thousand that
# adds to a prime, contains 21 terms, and is equal to 953.

# Which prime, below one-million, can be written as the sum
# of the most consecutive primes?

# ANSWER
# 997651

from util.utils import sieve
from util.utils import timeit


class Problem50:
    @timeit
    def __init__(self, max_int):
        self.max_int = max_int
        self.ls_primes = list(sieve(max_int))
        self.ans = 2
        self.max_len = 1

    @timeit
    def solve(self):
        num_primes = len(self.ls_primes)
        primes = set(self.ls_primes)  # this speeds up the prime check

        for i in range(num_primes):
            for j in range(i, num_primes - self.max_len):
                prime_sum = sum(self.ls_primes[i:j + 1 + self.max_len])
                if prime_sum < self.max_int:
                    if prime_sum in primes:
                        size = j + 1 - i
                        if size > self.max_len:
                            self.max_len = size
                            self.ans = prime_sum
                else:
                    break

        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    max_int = 1000000
    obj = Problem50(max_int=max_int)
    sol = obj.solve()
    print(sol)
