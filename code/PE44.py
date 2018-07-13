# find pent nums s.t. sum and diff is pent and diff is minimized

# Answer= 5482660

P = []
for i in range(1, 100000):
    P.append(i * (3 * i - 1) / 2)

min = 100000000


def ispent(num):
    return ((1 + ((24 * num) + 1) ** 0.5) / 6).is_integer()


for m in range(1, 10000):
    for n in range(m + 1, 10000):
        temp = P[m] + P[n]
        if ispent(temp):
            temp2 = P[n] - P[m]
            # print temp2
            if ispent(temp2):
                if temp2 < min:
                    min = temp2
                    # return min

print(min)
