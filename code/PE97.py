# PROBLEM

# The first known prime found to exceed one million digits was discovered in 1999,
# and is a Mersenne prime of the form 2^6972593 − 1; it contains exactly 2,098,960 digits.
# Subsequently other Mersenne primes, of the form 2^p − 1, have been found which contain more digits.
#
# However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 28433×2^7830457 + 1.
#
# Find the last ten digits of this prime number.

# ANSWER
# 8739992577


class Problem97:
    """Find last 10 digits of 28433*2^(7830457)+ 1  (Proth Prime)"""
    def __init__(self, modN, k, exp):
        self.modN = modN
        self.k = k
        self.exp = exp

        self.ans = k

    def solve(self):
        for i in range(self.exp):
            self.ans = (self.ans * 2) % self.modN
        return self.ans + 1


if __name__ == "__main__":
    modN = int(1e10)
    k = 28433
    exp = 7830457

    obj = Problem97(modN, k, exp)
    sol = obj.solve()
    print(sol)
