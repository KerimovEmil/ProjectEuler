# The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719,
# are themselves prime.
# There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
# How many circular primes are there below one million?

# Answer = 55


def is_prime(n):
    """
    precondition n is a nonnegative integer
    postcondition:  return True if n is prime and False otherwise.
    """
    if n < 2:
        return False
    if n % 2 == 0:
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


class Problem35:
    """How many circular primes are there below one million?"""
    def __init__(self, n):
        self.n = n
        self.count = 0

    def solve(self):
        for i in range(2, self.n):
            if is_circular(i):
                self.count += 1

        return self.count

    def get_solution(self):
        return self.count


if __name__ == "__main__":
    obj = Problem35(n=1000000)
    sol = obj.solve()
    print(sol)
