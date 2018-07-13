# The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

# Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

# NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

# ANSWER
# 748317


def sieve(n):  # TODO move to utils
    "Return all primes <= n."
    np1 = n + 1
    s = list(range(np1))
    s[1] = 0
    sqrtn = int(round(n ** 0.5))
    for i in range(2, sqrtn + 1):
        if s[i]:
            s[i * i: np1: i] = [0] * len(range(i * i, np1, i))
    return filter(None, s)


def trunc_left(num):
    return int(str(num)[:-1])


def trunc_right(num):
    return int(str(num)[1:])


def check1(num):
    for i in str(num):
        if int(i) % 2 == 0:
            return False
    return True


# S = P.primes_list(800000)
S = list_of_primes = list(sieve(800000))
T = []
for prime in S:
    if check1(prime):
        T.append(prime)
    elif len(str(prime)) == 2:
        T.append(prime)
sum = 0
t = 0
for prime in T:
    temp1 = prime
    temp2 = temp1
    k = len(str(prime))

    if k > 1:
        count = 0
        for i in range(k - 1):
            temp1 = trunc_left(temp1)
            temp2 = trunc_right(temp2)
            if temp1 not in S:
                break
            if temp2 not in S:
                break
            count += 1
        if count == k - 1:
            sum += prime
            t += 1
print(sum)

