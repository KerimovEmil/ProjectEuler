# ANSWER
# 612407567715

import itertools
from util.utils import sieve


# Only valid if 1 < n <= 10^DIGITS.
def is_prime(n, sqrt_primes):
    end = int(n ** 0.5)
    for p in sqrt_primes:
        if p > end:
            break
        if n % p == 0:
            return False
    return True


def special_is_prime(n, sqrt_primes):
    if n == 1:
        return False
    for p in sqrt_primes:
        if n % p == 0:
            return False
    return True


# FOR n=10 too many possible primes!

def helper_s(n, sqrt_primes, base, debug=True):  # Only works for 0
    ls_combin = [''.join(x) for x in itertools.product('0123456789', repeat=2)]
    total_sum = 0
    for pair in ls_combin:
        for i in range(len(base) - 1):
            for j in range(i + 1, len(base)):
                temp = base.copy()
                temp[i] = pair[0]
                temp[j] = pair[1]
                num_to_test = int(''.join(temp))
                if debug:
                    print("Testing Number: {}".format(num_to_test))
                if len(str(num_to_test)) == n:
                    if special_is_prime(num_to_test, sqrt_primes):
                        total_sum += num_to_test
    return total_sum


def new_s(n, d, sqrt_primes, debug=True):
    base = list(d * n)
    if debug:
        print("Base: {}".format(base))
    total_sum = 0
    for j in range(10):
        sum_j = 0
        for i in range(len(base)):
            temp = base.copy()
            temp[i] = str(j)
            num_to_test = int(''.join(temp))
            if debug:
                print("Testing Number: {}".format(num_to_test))
            if special_is_prime(num_to_test, sqrt_primes):
                sum_j += num_to_test
        if sum_j > 0:
            print("Primes found for: d={}, j={}".format(d, j))
            total_sum += sum_j
        else:
            print("no primes found for: d={}, j={}".format(d, j))
    if total_sum == 0:
        total_sum = helper_s(n, sqrt_primes, base, debug=debug)
    return total_sum


def new_sum_s_n(n, debug=True):
    max_int = int(10 ** (n / 2))
    print("Calculating Primes")
    sqrt_primes = list(sieve(max_int))
    print("Finished Calculating Primes")
    ans = 0
    for i in range(10):
        print("Calculating S_{}_{}".format(n, i))
        ans += new_s(n, str(i), sqrt_primes, debug=debug)
    return ans


if __name__ == '__main__':
    print(new_sum_s_n(10, debug=False))


