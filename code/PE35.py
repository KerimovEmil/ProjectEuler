# The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

# There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

# How many circular primes are there below one million?

# Answer = 55


def is_prime(n):
    """precondition n is a nonnegative integer
postcondition:  return True if n is prime and False otherwise."""
    if n < 2:
        return False
    if n % 2 == 0:
        # return False
        return n == 2
    k = 3
    while k * k <= n:
        if n % k == 0:
            return False
        k += 2
    return True


def is_circular(num):
    if num == 2:
        return True
    r = str(num)
    dig = []
    for i in r:
        if int(i) % 2 == 0:
            return False
        else:
            dig.append(i)
    x = num
    for i in range(len(r)):
        if not is_prime(x):
            return False
        else:
            dig.append(dig.pop(0))
            x = int(''.join(dig))
    return True


ans = 0
for i in range(1000000):
    if is_circular(i):
        ans = ans + 1
print(ans)
