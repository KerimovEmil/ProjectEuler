# PROBLEM

# A number chain is created by continuously adding the square of the digits in a number to form a new
# number until it has been seen before.

# Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop.
# What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
# How many starting numbers below ten million will arrive at 89?

# ANSWER
# 8581146

import functools


def memoize(obj):  # todo: move to utils? or not even use his
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


@memoize
def eightynine(d):  # TODO: this is very slow, need to speed up
    if d == 89:
        return True
    elif d == 1:
        return False
    else:
        return eightynine(sum(int(c) ** 2 for c in str(d)))


class Problem92:
    def __init__(self, n):
        self.n = n
        self.count = 0

    def solve(self):
        for i in range(1, self.n):
            self.count += eightynine(i)
        return self.count


if __name__ == "__main__":
    obj = Problem92(int(1e7))
    sol = obj.solve()
    print(sol)
