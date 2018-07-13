# If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

# (20,48,52), (24,45,51),(30,40,50)

# For which value of p <= 1000, is the number of solutions maximised?

# Answer: 840

# (a,b,c) int s.t. a^2 + b^2 = c^2

# a = k(m^2 - n^2)
# b = k(2mn)
# x = k(m^2 + n^2)

# m>n, and m,n,k >0 ints
def num_p(p):
    L = []
    count = 0
    for n in range(1, 30):
        for m in range(n + 1, 30):
            for k in range(1, 100):
                a = k * (m * m - n * n)
                b = k * 2 * n * m
                c = k * (m * m + n * n)
                if a + b + c == p:
                    if {a, b, c} not in L:
                        L.append({a, b, c})
                        count += 1
    return count


max = 0
best_p = 0
for i in range(10, 1000):
    temp = num_p(i)
    if max < temp:
        max = temp
        best_p = i
print(best_p)
