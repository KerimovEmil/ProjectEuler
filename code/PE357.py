# Consider the divisors of 30: 1,2,3,5,6,10,15,30.
# It can be seen that for every divisor d of 30, d+30/d is prime.
#
# Find the sum of all positive integers n not exceeding 100,000,000
# such that for every divisor d of n, d+n/d is prime.

# ANSWER
# 1739023853137

from util.utils import sieve
from util.utils import timeit


class Problem357:
    def __init__(self, max_int, debug=False):
        self.max_int = max_int
        self.ans = 0
        self.debug = debug

        if self.debug:
            print("Calculating Primes")
        self.primes = set(sieve(max_int))
        if self.debug:
            print("Finished Calculating Primes")
            print("{} is the total number of primes to check".format(len(self.primes)))

    @timeit
    def solve(self):
        for prime in self.primes:  # looping over primes since 1 is always a divisor, so d + 1 must be a prime
            n = prime - 1
            bool_are_all_primes = True
            # Simple filter
            for i in range(1, 10):
                if n % i == 0:
                    temp_sum = i + n / i
                    bool_are_all_primes = bool_are_all_primes and self.is_prime(temp_sum)
            if bool_are_all_primes:
                # Full filter
                for d in self.divisors(n):
                    temp_sum = d + n / d
                    bool_are_all_primes = bool_are_all_primes and self.is_prime(temp_sum)
                    if not bool_are_all_primes:
                        break
            if bool_are_all_primes:
                if self.debug:
                    print("{0} is a cool number".format(n))
                self.ans += n

        return self.ans

    def is_prime(self, n):
        return n in self.primes

    def divisors(self, n):
        # get factors and their counts
        factors = {}
        nn = n
        i = 2
        while i * i <= nn:
            while nn % i == 0:
                if i not in factors:
                    factors[i] = 0
                factors[i] += 1
                nn //= i
            i += 1
        if nn > 1:
            factors[nn] = 1
        primes = list(factors.keys())

        # generates factors from primes[k:] subset
        def generate(k):
            if k == len(primes):
                yield 1
            else:
                rest = generate(k + 1)
                prime = primes[k]
                for factor in rest:
                    prime_to_i = 1
                    # prime_to_i iterates prime**i values, i being all possible exponents
                    for _ in range(factors[prime] + 1):
                        yield factor * prime_to_i
                        prime_to_i *= prime

        yield from generate(0)
        # python 2
        # for factor in generate(0):
        #     yield factor


if __name__ == "__main__":
    obj = Problem357(max_int=int(1e8), debug=True)
    sol = obj.solve()
    print(sol)
