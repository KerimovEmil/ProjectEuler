# PROBLEM


# x,y > 0 and integers
# 1/x + 1/y = 1/n
# What is the least value of n for which the number of distinct solutions exceeds one-thousand?

# ANSWER
# 180180

# Math proof:
# Use the fact that:
# 1/x + 1/y = 1/n for y,x,n positive integers:
#
# implies that xy/(x+y) = n.
# Notice that if we assume x<=y then we must get that
# n< x <= 2n; and y = xn/(x-n).
#
# The problem now boils down to when y is an integer for all integers of x between n+1 and 2n.
# This problem can be written as when x-n divides xn for x from n+1 to 2n.
# Notice that for x = n+i for i from 1 to n, this implies
# i divides n * (n+i) = n^2 + n * i.
# Since i divides n*i for sure, then we only need to find how many i divide n^2, for i in 1 to n.

# To find out how many i divide n^2, for i in 1 to n, if we write n = p1^a1 * p2^a2 * p3^a3
# Then the number of divisors of n^2 = (2 * a1 + 1) * (2 * a2 + 1) * (2 * a3 + 1) .
#
# By a neat symmetry argument we can show that number of those divisors that are less than or equal to n are:
# ((2 * a1 + 1) * (2 * a2 + 1) * (2 * a3 + 1) + 1) / 2
#
# Therefore we only need to find a few possible sets that equal the max number of unique solutions that we are
#  looking for, and then figure out which one of those sets correspond to the smallest number.

# Paper and pencil method of solving 108:
# Find the upper bound of n, i.e. all unique primes.
# (3^x +1)/2 >= 1000
# 3^x >= 1999
# x>=7
# Therefore n<= 2*3*5*7*11*13*17 = 510510
#
# Now start trying out values between 2^2*3*5*7*11*13 and 2*3*5*7*11*13*17
# Try replacing the biggest prime (17) with a 2
# Now compare 5*3^5 = 1215 < 1999 hence not good enough, next smallest choice for n has:
# Try replacing the biggest prime (17) with a 2*3
# 5^2 * 3^4 = 2025 >= 1999 hence we found a smaller n
# n <= 2^2 * 3^2 * 5 * 7 * 11 * 13 = 180180
# Try replacing the biggest prime (13) with a 2
# 7 * 5 * 3^3 = 945 < 1999 hence not good enough.
# Try replacing the biggest prime (13) with a 5
# 5^3 * 3^2 = 1125 < 1999 hence not good enough.
# Try replacing the biggest prime (13) with a 2*3,
# 7^2 * 3^3 = 1323 < 1999 hence not good enough.
# Hence smallest n found was 180180.

class Problem108:
    def __init__(self):
        pass

    def solve(self):
        return 2 * 2 * 3 * 3 * 5 * 7 * 11 * 13


if __name__ == "__main__":
    obj = Problem108()
    sol = obj.solve()
    print(sol)
