# Consider the divisors of 30: 1,2,3,5,6,10,15,30.
# It can be seen that for every divisor d of 30, d+30/d is prime.
#
# Find the sum of all positive integers n not exceeding 100,000,000
# such that for every divisor d of n, d+n/d is prime.

# ANSWER
# 1739023853137

# Since 1 is always a divisor of n, then
# 1 + n/1 = 1 + n = prime

# n must be even
# since if n is odd then every divisor d must be odd then
# d + n/30 = odd + odd = even != prime if the prime > 2. Which holds for n > 2.

# n is square free
# since if n = p_1 * p_2^2 then choose d = p_2
# p_2 + p_1*p_2 = p_2 * (1 + p_1) != prime.


from util.utils import sieve
from util.utils import square_primes_sieve
from util.utils import square_free_sieve
from util.utils import primes_of_n
from util.utils import timeit


class Problem357:
    @timeit
    def __init__(self, max_int, debug=False):
        self.max_int = max_int
        self.ans = 0
        self.debug = debug

        if self.debug:
            print("Calculating Primes")
        # self.ls_primes = list(sieve(max_int))
        self.set_primes = set(sieve(max_int))
        # self.square_primes = square_primes_sieve(max_int, self.ls_primes)
        if self.debug:
            print("Calculating square free sieve")
        # self.square_free = set(square_free_sieve(int(max_int)))
        # self.primes = sieve(max_int)
        if self.debug:
            print("Finished Calculating Primes")
            print("{} is the total number of primes to check".format(len(self.set_primes)))

    @timeit
    def solve(self):
        for p in self.set_primes:
            n = p - 1
            # simple filter 1
            if n % 4 == 0 or n % 9 == 0:
                continue
            # simple filter 3
            if not self.is_prime(n / 2 + 2):
                continue
            # Simple filter 3
            if not all([self.is_prime(i + n / i) for i in range(3, 8) if n % i == 0]):
                continue

            # Full filter
            prime_factors = primes_of_n(n)
            if any([t[1] > 1 for t in prime_factors.items()]):
                continue
            all_divisors = self.divisors(prime_factors)
            all_primes = True
            for d in all_divisors:
                if not self.is_prime(d + n / d):
                    all_primes = False
                    break
            if all_primes:
                if self.debug:
                    print("{0} is a cool number".format(n))
                self.ans += n

        return self.ans

    @staticmethod
    def basic_is_prime(n):
        if int(n) & 1 == 0:
            return False  # 2 is a divisor
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False  # d is a divisor
            d = d + 2
        return True

    def is_prime(self, n):
        return n in self.set_primes

    def divisors(self, prime_factors):
        primes = list(prime_factors.keys())

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
                    for _ in range(prime_factors[prime] + 1):
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
