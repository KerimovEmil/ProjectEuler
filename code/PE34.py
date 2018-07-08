# PROBLEM

# Find the sum of all numbers which are equal to the sum of the factorial of their digits.

# ANSWER:
# 40730


def factorial(x):
    ans = 1
    while x:
        ans *= x
        x -= 1
    return ans


def digits(num):
    return [int(i) for i in str(num)]


def sum_f(num):
    dig = digits(num)
    ans = 0
    for d in dig:
        ans += factorial(d)
    return ans


ans = 0

for i in range(3, 200000):
    if sum_f(i) == i:
        ans += i
print(ans)
