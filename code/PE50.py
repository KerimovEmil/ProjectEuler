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


def pe50(ls_prime, max_int):
    max_len = 1
    max_consec_prime = 2
    num_primes = len(ls_prime)
    primes = set(ls_prime)  # this speeds up the prime check

    for i in range(num_primes):
        for j in range(i, num_primes):
            prime_sum = sum(ls_prime[i:j + 1])
            if prime_sum < max_int:
                if prime_sum in primes:
                    size = len(ls_prime[i:j + 1])
                    if size > max_len:
                        max_len = size
                        max_consec_prime = prime_sum
            else:
                break

    return max_consec_prime


if __name__ == '__main__':
    max_int = 1000000
    list_of_primes = list(sieve(max_int))

    print(pe50(list_of_primes, max_int))
