# We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

# What is the largest n-digit pandigital prime that exists?

# Answer: 7652413

import itertools


def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False
    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6
    return True


def pandigital(num):
    s = set()
    for i in str(num):
        if i in (s):
            return 0
        else:
            if int(i) == 0:
                return 0
            else:
                s.add(i)
    return 1


L = itertools.permutations(range(1, 8))
max = 0
for i in L:
    num = int(''.join(map(str, list(i))))
    if is_prime(num):
        if num > max:
            max = num

print(max)

# 0: for 9 digits
# 0 : for 8 digits
# 7652413 : for 7 digits
