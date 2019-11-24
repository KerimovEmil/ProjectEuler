# Considering 4-digit primes containing repeated digits it is clear that they cannot all be the same:
# 1111 is divisible by 11, 2222 is divisible by 22, and so on. But there are nine 4-digit primes containing three ones:
#
# 1117, 1151, 1171, 1181, 1511, 1811, 2111, 4111, 8111
#
# We shall say that M(n, d) represents the maximum number of repeated digits for an n-digit prime where d is the
# repeated digit, N(n, d) represents the number of such primes, and S(n, d) represents the sum of these primes.
#
# So M(4, 1) = 3 is the maximum number of repeated digits for a 4-digit prime where one is the repeated digit,
#  there are N(4, 1) = 9 such primes, and the sum of these primes is S(4, 1) = 22275. It turns out that for d = 0,
# it is only possible to have M(4, 0) = 2 repeated digits, but there are N(4, 0) = 13 such cases.
#
# In the same way we obtain the following results for 4-digit primes.
#
# Digit,d	M(4, d)	N(4, d)	S(4, d)
#      0       2	   13	 67061
#      1	   3	    9	 22275
#      2	   3	    1	 2221
#      3	   3	   12	 46214
#      4	   3	    2	 8888
#      5	   3	    1	 5557
#      6	   3	    1	 6661
#      7	   3	    9	 57863
#      8	   3	    1	 8887
#      9	   3	    7	 48073
# For d = 0 to 9, the sum of all S(4, d) is 273700.
#
# Find the sum of all S(10, d).

# ANSWER
# 612407567715

import itertools
from util.utils import sieve
from util.utils import timeit


class Problem111:
    def __init__(self, n, debug):
        self.n = n
        self.debug = debug
        self.ans = 0

        self.ls_combin = [''.join(x) for x in itertools.product('0123456789', repeat=2)]

        max_int = int(10 ** (self.n / 2))
        if self.debug:
            print("Calculating Primes")
        self.sqrt_primes = list(sieve(max_int))
        if self.debug:
            print("Finished Calculating Primes")

    @timeit
    def solve(self):
        for i in range(self.n):
            if self.debug:
                print("Calculating S_{}_{}".format(self.n, i))
            self.ans += self.new_s(str(i))
        return self.ans

    def get_solution(self):
        return self.ans

    def new_s(self, d):
        base = list(d * self.n)
        if self.debug:
            print("Base: {}".format(base))
        total_sum = 0
        for j in range(self.n):
            sum_j = 0
            for i in range(len(base)):
                temp = base.copy()
                temp[i] = str(j)
                num_to_test = int(''.join(temp))
                if self.debug:
                    print("Testing Number: {}".format(num_to_test))
                if self.special_is_prime(num_to_test):
                    sum_j += num_to_test
            if sum_j > 0:
                if self.debug:
                    print("Primes found for: d={}, j={}".format(d, j))
                total_sum += sum_j
            else:
                if self.debug:
                    print("no primes found for: d={}, j={}".format(d, j))
        if total_sum == 0:
            total_sum = self.helper_s(base)
        return total_sum

    def helper_s(self, base):  # Only works for 0
        total_sum = 0
        for pair in self.ls_combin:
            for i in range(len(base) - 1):
                for j in range(i + 1, len(base)):
                    temp = base.copy()
                    temp[i] = pair[0]
                    temp[j] = pair[1]
                    num_to_test = int(''.join(temp))
                    if self.debug:
                        print("Testing Number: {}".format(num_to_test))
                    if len(str(num_to_test)) == self.n:
                        if self.special_is_prime(num_to_test):
                            total_sum += num_to_test
        return total_sum

    def special_is_prime(self, n):
        if n == 1:
            return False
        for p in self.sqrt_primes:
            if n % p == 0:
                return False
        return True


if __name__ == "__main__":
    obj = Problem111(n=10, debug=False)
    sol = obj.solve()
    print(sol)
