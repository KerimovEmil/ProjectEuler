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


P = list(sieve(100000))
T = set(P)


def div(num, D):
    count = 0
    for prime in P:
        if prime > num:
            return False
        if num % prime == 0:
            count += 1
        while num % prime == 0:
            num = num / prime
        if count > D:
            return False
        if count == D and num == 1:
            return True
    if count == D:
        return True
    else:
        return False


R = list(set(range(100000, 150000)).difference(T))
for num in R:
    if div(num, 4):
        if div(num + 1, 4):
            if div(num + 2, 4):
                if div(num + 3, 4):
                    print(num)
                    break
