# ANSWER
# 45228


def check(num, a=set()):
    s = set()
    for i in str(num):
        if int(i) in (s.union(a)):
            return 0
        else:
            if int(i) == 0:
                return 0
            else:
                s.add(int(i))
    return s.union(a)


def pandigital(a, b):
    x = check(a)
    if x == 0:
        return 0
    else:
        y = check(b, x)
        if y == 0:
            return 0
        else:
            z = check(a * b, y)
    if z == 0:
        return 0
    elif len(z) == 9:
        return 1


class Problem32:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.sum = 0

    def solve(self):
        t = []
        for i in range(self.max_x):
            for j in range(self.max_y):
                if pandigital(i, j):
                    if i * j in t:
                        pass
                    else:
                        t.append(i * j)
                        self.sum += i * j

        return self.sum


if __name__ == "__main__":
    obj = Problem32(max_x=100, max_y=10000)
    sol = obj.solve()
    print(sol)

