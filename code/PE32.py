# We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once;
# for example, the 5-digit number, 15234, is 1 through 5 pandigital.

# The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product
#  is 1 through 9 pandigital.

# Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9
# pandigital.

# ANSWER
# 45228

from util.utils import timeit
# from util.utils import is_pandigital


class Problem32:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.sum = 0

    @timeit
    def solve(self):
        t = []
        for i in range(self.max_x):
            for j in range(self.max_y):
                if Problem32.pandigital(i, j):
                    if i * j in t:
                        pass
                    else:
                        t.append(i * j)
                        self.sum += i * j

        return self.sum

    @staticmethod
    def pandigital(a, b):
        x = Problem32.check(a)
        if x == False:
            return False
        else:
            y = Problem32.check(b, x)
            if y == False:
                return False
            else:
                z = Problem32.check(a * b, y)
        if z == False:
            return False
        elif len(z) == 9:
            return True

    @staticmethod
    def check(num, a=None):
        s = set() if a is None else a

        for i in str(num):
            if i in s:
                return False
            else:
                if i == '0':
                    return False
                else:
                    s.add(i)
        return s


if __name__ == "__main__":
    obj = Problem32(max_x=100, max_y=10000)
    sol = obj.solve()
    print(sol)

