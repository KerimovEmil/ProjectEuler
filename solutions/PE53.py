# It is not until n = 23, that a value exceeds one-million: 23C10 = 1144066.

# How many, not necessarily distinct, values of  nCr, for 1 <= n <= 100, are greater than one-million?

# Answer = 4075

from util.utils import combin
from util.utils import timeit


class Problem53:
    def __init__(self, max_int, max_n):
        self.max_int = max_int
        self.max_n = max_n
        self.count = 0

    @timeit
    def solve(self):
        for n in range(0, self.max_n + 1):
            for r in range(0, int(n / 2 + 1)):
                if combin(n, r) > self.max_int:
                    self.count += n - 2 * r + 1
                    break

        return self.count

    def get_solution(self):
        return self.count


if __name__ == "__main__":
    max_int = 1000000
    max_n = 100
    obj = Problem53(max_int=max_int, max_n=max_n)
    sol = obj.solve()
    print(sol)
