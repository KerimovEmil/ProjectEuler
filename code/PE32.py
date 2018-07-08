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


t = []
sum = 0
for i in range(100):
    for j in range(10000):
        if pandigital(i, j):
            if i * j in t:
                pass
            else:
                t.append(i * j)
                sum += i * j

print(sum)
