# Take the number 192 and multiply it by each of 1, 2, and # 3:
# 192 * 1 = 192
# 192 * 2 = 384
# 192 * 3 = 576
# By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

# The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

# What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?

# Answer = 932718654

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


def pandigital(a):
    x = check(a)
    if x == 0:
        return 0
    for i in range(2, 9):
        x = check(a * i, x)
        if x == 0:
            break
        if len(x) == 9:
            r = str(a)
            i = 2
            while len(r) < 9:
                r += str(a * i)
                i += 1
            return int(r)
    return 0


max = 0
for i in range(1, 10000):
    temp = pandigital(i)
    if temp > max:
        max = temp
print(max)
