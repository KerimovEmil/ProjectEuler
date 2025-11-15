# The divisors of 12 are: 1,2,3,4,6 and 12.
# The largest divisor of 12 that does not exceed the square root of 12 is 3.
# We shall call the largest divisor of an integer n that does not exceed the square root of n the pseudo square
# root (PSR) of n.
# It can be seen that PSR(3102)=47.
#
# Let p be the product of the primes below 190.
# Find PSR(p) mod 10^16.

# ANSWER  # TODO: finish this code
# 1096883702440585

# e.g.
# prime_prod = 2*3*5*7*11 = 2310
# sqrt(2310) = 48.06... < 49
# 48 < sqrt(2310) < 49
# divisors of 2310: 1 | 2 | 3 | 5 | 6 | 7 | 10 | 11 | 14 | 15 | 21 | 22 | 30 | 33 | 35 | 42
# | 55 | 66 | 70 | 77 | 105 | 110 | 154 | 165 | 210 | 231 | 330 | 385 | 462 | 770 | 1155 | 2310 (32 divisors)

# therefore the PSR(2310) = 42 = 2*3*7

# 11*7 = 77 > 48
# 11*5 = 55 > 48
# 11*3 = 33 < 48 (pass)
# 11*3*2 = 66 > 48
# 7*5 = 35 < 48 (pass)
# 7*5*3 = 105 > 48
# 7*5*2 = 70 > 48
# 7*3*2 = 42 < 48 (pass)

import itertools
from util.utils import timeit, primes_upto


class Problem266:
    def __init__(self, prime_max, digits, debug):
        self.prime_max = prime_max
        self.digits = digits
        self.debug = debug
        self.ans = 0

        self.ls_primes = primes_upto(prime_max)
        if self.debug:
            print("Primes are:{}".format(self.ls_primes))
        self.num_total_primes = len(self.ls_primes)

    @staticmethod
    def get_list_prod(ls):
        prod = 1
        for prime in ls:
            prod *= prime
        return prod

    @staticmethod
    def testing_removal_of_small_prime(num_iter, ls_test_iter, max_int, divisor_must=1, debug=True):
        # Testing if removing small prime p, will next smallest divisor still be less than the max_int?
        # Given we use n divisors.
        # If not then small prime p, must be in the divisors.

        ls_test = ls_test_iter.copy()

        for p in ls_test_iter[:-num_iter]:
            if debug:
                print("Testing the removal of small prime {}".format(p))
            # Smallest combination if removing prime p
            smallest = divisor_must * Problem266.get_list_prod(ls_test[1:num_iter + 1])

            if smallest > max_int:
                # if smallest combination after removing prime p is too big, then p must be in the final combination
                divisor_must *= p
                ls_test.remove(p)
                num_iter -= 1
                if debug:
                    print("{} must be in the divisor, otherwise divisor is too big."
                          " {} choices left out of {} primes.".format(p, num_iter, len(ls_test)))
            else:
                if debug:
                    print("The removal of {}, does not result in the next smallest product being too big,".format(p))
                break
        return divisor_must, ls_test, num_iter

    @staticmethod
    def testing_inclusion_of_big_prime(num_iter, ls_test_iter, max_int, divisor_must, debug=True):
        # Testing the inclusion of big prime p, will the smallest possible divisor including p, still be less than the
        # max_int?
        # Given we use n divisors.
        # If not then big prime p must not be in the divisors.

        ls_test = ls_test_iter.copy()
        for p in ls_test_iter[:num_iter:-1]:
            if debug:
                print("Testing the inclusion of big prime {}".format(p))
            # Smallest combination if using prime p
            assert len(ls_test[:num_iter - 1]) == num_iter - 1
            smallest = divisor_must * p * Problem266.get_list_prod(ls_test[:num_iter - 1])

            if smallest > max_int:
                # if smallest combination still too large
                ls_test.remove(p)
                if debug:
                    print("{} cannot be in the divisor, otherwise the divisor would be too big."
                          " {} choices left out of {} primes.".format(p, num_iter, len(ls_test)))
            else:
                if debug:
                    print("{} can be in the divisor, since smallest still bigger than max "
                          "int.".format(p))
                break
        return ls_test

    @staticmethod
    def testing_inclusion_of_small_prime(num_iter, ls_test_iter, prev_max, divisor_must, debug=True):
        # Testing the inclusion of small prime p, will the largest possible divisor including p, still be greater than \
        # the previous max divisor?
        # Given we use n divisors.
        # If not then small prime p must not be in the divisors.

        ls_test = ls_test_iter.copy()
        for p in ls_test_iter[:-num_iter + 1]:
            if debug:
                print("Testing inclusion of small prime: {}.".format(p))
            # Largest combination if using prime p
            assert len(ls_test[-num_iter + 1:]) == num_iter - 1
            largest = divisor_must * p * Problem266.get_list_prod(ls_test[-num_iter + 1:])

            if largest < prev_max:
                # if largest combination still too small
                ls_test.remove(p)
                if debug:
                    print("{} cannot be in the divisor, otherwise the divisor would be too small compared to the "
                          "previous max."
                          " {} choices left out of {} primes.".format(p, num_iter, len(ls_test)))
            else:
                if debug:
                    print(
                        "{} can be in the divisor, since without it the largest is still bigger than the previous max."
                        "".format(p))
                break
        return ls_test

    @staticmethod
    def testing_removal_of_big_prime(num_iter, ls_test_iter, prev_max, divisor_must, debug=True):
        # Testing the removal of large prime p, will the largest possible divisor not including p, still be greater
        # than the previous max divisor?
        # Given we use n divisors.
        # If not then large prime p must be in the divisors.

        ls_test = ls_test_iter.copy()
        for p in ls_test_iter[num_iter:][::-1]:
            if debug:
                print("Testing removal of large prime: {}.".format(p))
            # Largest combination without using prime p
            assert len(ls_test[-num_iter - 1:-1]) == num_iter
            largest = divisor_must * Problem266.get_list_prod(ls_test[-num_iter - 1:-1])

            if largest < prev_max:
                # if largest combination still too small that mean this prime must be in the divisor
                divisor_must *= p
                ls_test.remove(p)
                num_iter -= 1
                if debug:
                    print("{} must be in the divisor, otherwise the divisor would be too small."
                          " {} choices left out of {} primes.".format(p, num_iter, len(ls_test)))
            else:
                if debug:
                    print("{} does not NEED to be in the divisor.".format(p))
                break
        return divisor_must, ls_test, num_iter

    def sub_product(self, n, max_int, previous_max_divisor):
        """Taking n elements of the list of primes"""
        smallest = Problem266.get_list_prod(self.ls_primes[:n])  # Smallest combination possible
        largest = Problem266.get_list_prod(self.ls_primes[-n:])  # Largest combination possible
        if smallest > max_int:
            if self.debug:
                print("Smallest possible divisor is larger than max_int.")
            return previous_max_divisor
        elif largest < previous_max_divisor:
            if self.debug:
                print("Largest possible divisor is smaller than the previous largest divisor.")
            return previous_max_divisor
        else:
            pass

        divisor_must, ls_test, num_iter = Problem266.testing_removal_of_small_prime(num_iter=n,
                                                                                    ls_test_iter=self.ls_primes.copy(),
                                                                                    max_int=max_int, divisor_must=1,
                                                                                    debug=self.debug)

        ls_test = Problem266.testing_inclusion_of_big_prime(num_iter=num_iter,
                                                            ls_test_iter=ls_test,
                                                            max_int=max_int,
                                                            divisor_must=divisor_must,
                                                            debug=self.debug)

        ls_test = Problem266.testing_inclusion_of_small_prime(num_iter=num_iter,
                                                              ls_test_iter=ls_test,
                                                              prev_max=previous_max_divisor,
                                                              divisor_must=divisor_must,
                                                              debug=self.debug)

        divisor_must, ls_test, num_iter = Problem266.testing_removal_of_big_prime(num_iter=num_iter,
                                                                                  ls_test_iter=ls_test,
                                                                                  prev_max=previous_max_divisor,
                                                                                  divisor_must=divisor_must,
                                                                                  debug=self.debug)
        if self.debug:
            print('Looping over all combinations of {} choices left out of {} primes.'.format(num_iter, len(ls_test)))
        # print('Compressing by product less than max_int')
        # x = itertools.combinations(ls_test, r=num_iter)
        # y = itertools.combinations(ls_test, r=num_iter)
        # print('Starting the compressing')
        # iterate_over = itertools.compress(x, [Problem266.get_list_prod(k) < max_int/divisor_must for k in y])
        # print('Finished compressing')
        # for k in iterate_over:
        for k in itertools.combinations(ls_test, r=num_iter):
            temp_max = divisor_must * Problem266.get_list_prod(k)
            if previous_max_divisor < temp_max < max_int:
                if self.debug:
                    temp_sol = temp_max % 10 ** (self.digits)
                    print('NEW MAX:{}, DIFF: {}, SOL: {}, Primes: {}'.format(temp_max, max_int - temp_max, temp_sol, k))
                previous_max_divisor = temp_max
        return previous_max_divisor

    @timeit
    def solve(self):
        prime_prod = Problem266.get_list_prod(self.ls_primes)
        sqrt_prod = int(prime_prod ** 0.5)
        # max_divisor = 2323218950482697766641170378640119830
        max_divisor = 0
        for num_primes in range(self.num_total_primes, 1, -1):
            if self.debug:
                print('TESTING: {} primes out of {}'.format(num_primes, self.num_total_primes))
            max_divisor = self.sub_product(n=num_primes, max_int=sqrt_prod, previous_max_divisor=max_divisor)
            self.ans = max_divisor % 10 ** (self.digits)
            print('Answer so far is: {}'.format(self.ans))

        return self.ans

    def get_solution(self):
        return self.ans


if __name__ == "__main__":
    obj = Problem266(prime_max=190, digits=16, debug=True)
    # obj = Problem266(prime_max=12, digits=16, debug=True)
    sol = obj.solve()
    print(sol)
