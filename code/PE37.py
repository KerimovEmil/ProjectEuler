# The number 3797 has an interesting property. Being prime itself, it is possible to
# continuously remove digits from left to right, and remain prime at each stage:
# 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

# Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

# NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

# ANSWER
# 748317

from util.utils import sieve


def trunc_left(num):
    return int(str(num)[:-1])


def trunc_right(num):
    return int(str(num)[1:])


def check1(num):
    """Checks if no digit of num is divisible by 2."""
    for i in str(num):
        if int(i) % 2 == 0:
            return False
    return True


class Problem37:
    def __init__(self, max_int):
        self.max_int = max_int
        self.ans = 0
        self.count = 0

    def create_list_of_primes(self):
        ls_primes = list(sieve(self.max_int))
        ls_primes_loop = []
        for prime in ls_primes:
            if check1(prime):  # no digit will be divisible by 2
                ls_primes_loop.append(prime)
            elif len(str(prime)) == 2:  # all two digit primes are included even if they have a 2
                ls_primes_loop.append(prime)
        return ls_primes_loop, ls_primes

    def solve(self):
        ls_primes_loop, ls_primes = self.create_list_of_primes()
        for prime in ls_primes_loop:
            trunc_l = prime
            trunc_r = prime
            k = len(str(prime))

            if k > 1:
                count = 0
                for i in range(k - 1):
                    trunc_l = trunc_left(trunc_l)
                    trunc_r = trunc_right(trunc_r)
                    if trunc_l not in ls_primes:
                        break
                    if trunc_r not in ls_primes:
                        break
                    count += 1
                if count == k - 1:
                    self.ans += prime
                    self.count += 1
            if self.count == 11:  # only 11 of these primes exist
                return self.ans
        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    obj = Problem37(max_int=800000)
    sol = obj.solve()
    print(sol)
