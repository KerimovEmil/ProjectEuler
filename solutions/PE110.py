# PROBLEM


# x,y > 0 and integers
# 1/x + 1/y = 1/n
# What is the least value of n for which the number of distinct solutions exceeds 4 million?

# ANSWER
# 9350130049860600

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

# Paper and pencil method of solving 110:
# Find the upper bound of n, i.e. all unique primes.
# (3^x +1)/2 >= 4e6
# 3^x >= 7,999,999
# x>=15
# Therefore n<= 2*3*5*7*11*13*17*19*23*29*31*37*41*43*47 = 614889782588491410
#
# Try replacing the biggest prime (47) with a 2
# Now compare 5*3^13 = 7,971,615 < 7,999,999 hence not good enough, next smallest choice for n has:
# Try replacing the biggest prime (47) with a 2*3
# 5^2 * 3^12 = 13,286,025 >= 7,999,999 hence we found a smaller n:
# n <= 2^2 * 3^2 * 5 * 7 * 11 * 13 *17*19*23*29*31*37*41*43= 78,496,567,990,020,180
# Try replacing the biggest prime (43) with a 2
# 7 * 5 * 3^11 = 6,200,145 < 7,999,999 hence not good enough.
# Try replacing the biggest prime (43) with a 5
# 5^3 * 3^10 = 7,381,125 < 7,999,999 hence not good enough.
# Try replacing the biggest prime (43) with a 2*3
# 7^2 * 3^11 = 8,680,203 >= 7,999,999 hence we found a smaller n:
# n <= 2^3 * 3^3 * 5*7*11*13*17*19*23*29*31*37*41= 10,953,009,486,979,560
# Try replacing the biggest prime (41) with a 2
# 9 * 7 * 3^10 = 3,720,087 < 7,999,999 hence not good enough.
# Try replacing the biggest prime (41) with a 5
# 7^2 * 5 * 3^9 = 4,822,335 < 7,999,999 hence not good enough.
# Try replacing the biggest prime (41) with a 2*3
# 9^2 * 3^10 = 4,782,969 < 7,999,999 hence not good enough.
# Try replacing the biggest prime (41) with a 5*7 = 35
# 7^2 * 5^2 * 3^8 = 8,037,225 >= 7,999,999 hence we found a smaller n:
# n <= 2^3 * 3^3 * 5^2 * 7^2 *11*13*17*19*23*29*31*37= 9,350,130,049,860,600
# N = 9,350,130,049,860,600


class Problem110:
    def __init__(self):
        pass

    def solve(self):
        return 2*2*2*3*3*3*5*5*7*7*11*13*17*19*23*29*31*37


if __name__ == "__main__":
    obj = Problem110()
    sol = obj.solve()
    print(sol)
