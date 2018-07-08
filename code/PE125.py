# ANSWER
# 2906969179


def is_palin(n):
    ls = list(str(n))
    return (ls == ls[::-1])


class Problem125:
    """
    Find the sum of all the numbers less than 10^8
    that are both palindromic and can be written as
    the sum of consecutive squares.
    """

    def __init__(self, max_value):
        self.max_value = max_value
        self.sum = 0
        self.ls_consec_sq = []
        self.list_of_is_consec_sq()

    def is_sum_of_consec_sq(self, n):
        return n in self.ls_consec_sq

    def solve(self):
        for i in self.ls_consec_sq:
            if is_palin(i):
                self.sum += i
        return self.sum

    def list_of_is_consec_sq(self):
        for n in range(2, int(self.max_value ** 0.5) + 1):
            for a in range(n - 1, 0, -1):
                value = int(n * (n + 1) * (2 * n + 1) / 6 - (a - 1) * a * (2 * a - 1) / 6)
                if value < self.max_value:
                    self.ls_consec_sq.append(value)
                else:
                    break
        self.ls_consec_sq = list(set(self.ls_consec_sq))


if __name__ == "__main__":
    a = Problem125(int(1e8))
    sol = a.solve()
    print(sol)
