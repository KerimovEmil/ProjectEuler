# ANSWER
# 1739023853137

from util.utils import sieve

max_int = int(1e8)


def divisors(n):
    # get factors and their counts
    factors = {}
    nn = n
    i = 2
    while i * i <= nn:
        while nn % i == 0:
            if not i in factors:
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

    # in python3, `yield from generate(0)` would also work
    for factor in generate(0):
        yield factor


print("Calculating Primes")
primes = set(sieve(max_int))
print("Finished Calculating Primes")


def is_prime(n):
    return n in primes


def f(max_n):
    sum = 0
    for n in range(1, max_n + 1):
        bool_are_all_primes = True
        # Simple filter
        for i in range(1, 10):
            if n % i == 0:
                temp_sum = i + n / i
                bool_are_all_primes = bool_are_all_primes and is_prime(temp_sum)
        if bool_are_all_primes:
            # Full filter
            for d in divisors(n):
                temp_sum = d + n / d
                bool_are_all_primes = bool_are_all_primes and is_prime(temp_sum)
                if not bool_are_all_primes:
                    break
        if bool_are_all_primes:
            print("{0} is a cool number".format(n))
            sum += n

    return sum


def f():
    sum = 0
    for prime in primes:
        n = prime - 1
        bool_are_all_primes = True
        # Simple filter
        for i in range(1, 10):
            if n % i == 0:
                temp_sum = i + n / i
                bool_are_all_primes = bool_are_all_primes and is_prime(temp_sum)
        if bool_are_all_primes:
            # Full filter
            for d in divisors(n):
                temp_sum = d + n / d
                bool_are_all_primes = bool_are_all_primes and is_prime(temp_sum)
                if not bool_are_all_primes:
                    break
        if bool_are_all_primes:
            print("{0} is a cool number".format(n))
            sum += n

    return sum


print("{} is the total number of primes to check".format(len(primes)))
print(f())
