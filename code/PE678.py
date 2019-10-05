"""
PROBLEM

If a triple of positive integers (a,b,c) satisfies a2+b2=c2, it is called a Pythagorean triple.
No triple (a,b,c) satisfies ae+be=ce when e≥3 (Fermat's Last Theorem). However, if the exponents of the left-hand side
 and right-hand side differ, this is not true. For example, 3^3+6^3=3^5.

Let a,b,c,e,f be all positive integers, 0<a<b, e≥2, f≥3 and c^f≤N.
Let F(N) be the number of (a,b,c,e,f) such that a^e+b^e=c^f. You are given F(10^3)=7, F(10^5)=53 and F(10^7)=287.

Find F(10^18).

ANSWER:
????
Solve time ~???? seconds
"""

# Problem
# a^e + b^e = c^f, for 0 < a < b, e>= 2, f>=3, c^f <= 10^18
#
# https://www.science20.com/vastness_ways_science/parcelatories_powers_equations_fermats_last_theorem
# e and f need to be co-prime

# BEAL'S CONJECTURE:  If A^x + B^y = C^z, where A, B, C, x, y and z are positive integers
# and x, y and z are all greater than 2, then A, B and C must have a common prime factor.

# assuming the Beal conjecture, we can split the problem into 3 cases:

# CASE 1: e = 2
# a^2 + b^2 = c^f, for 0 < a < b, f>=3, c^f <= 10^18
# For this we can figure out if a number can be expressed as the sum of two squares by counting the number of prime
# factors in it. (see PE 229 and 233)
# Ignore powers of 2. 3 mod 4 primes must be even power. 1 mod 4 primes must exist OR odd power of 2.

# CASE 2: e > 2
# a^e + b^e = c^f, for 0 < a < b, e>= 3, f>=3, c^f <= 10^18
# Assuming Beal's conjecture, a,b,c must all have a common factor.

# The found solutions of case 2: limit (10^18)
# 3^3 + 6^3 = 3^5 = 243
# 9^3 + 18^3 = 3^8 = 6561
# 27^3 + 54^3 = 3^11 = 177147
# 81^3 + 162^3 = 3^14 = 4782969
# 243^3 + 486^3 = 3^17 = 129140163
# 729^3 + 1458^3 = 3^20 = 3486784401
# 2187^3 + 4374^3 = 3^23 = 94143178827
# 6561^3 + 13122^3 = 3^26 = 2541865828329
# 19683^3 + 39366^3 = 3^29 = 68630377364883
# 59049^3 + 118098^3 = 3^32 = 1853020188851841
# 177147^3 + 354294^3 = 3^35 = 50031545098999707
# 9^3 + 18^3 = 9^4 = 6561
# 81^3 + 162^3 = 9^7 = 4782969
# 729^3 + 1458^3 = 9^10 = 3486784401
# 6561^3 + 13122^3 = 9^13 = 2541865828329
# 59049^3 + 118098^3 = 9^16 = 1853020188851841
# 17^4 + 34^4 = 17^5 = 1419857
# 289^4 + 578^4 = 17^9 = 118587876497
# 4913^4 + 9826^4 = 17^13 = 9904578032905937
# 96^3 + 192^3 = 24^5 = 7962624
# 2304^3 + 4608^3 = 24^8 = 110075314176
# 55296^3 + 110592^3 = 24^11 = 1521681143169024
# 33^5 + 66^5 = 33^6 = 1291467969
# 1089^5 + 2178^5 = 33^11 = 50542106513726817
# 65^6 + 130^6 = 65^7 = 4902227890625
# 144^3 + 288^3 = 72^4 = 26873856
# 10368^3 + 20736^3 = 72^7 = 10030613004288
# 729^3 + 1458^3 = 81^5 = 3486784401
# 59049^3 + 118098^3 = 81^8 = 1853020188851841
# 129^7 + 258^7 = 129^8 = 76686282021340161
# 3072^3 + 6144^3 = 192^5 = 260919263232
# 729^3 + 1458^3 = 243^4 = 3486784401
# 177147^3 + 354294^3 = 243^7 = 50031545098999707
# 544^4 + 1088^4 = 272^5 = 1488827973632
# 9375^3 + 18750^3 = 375^5 = 7415771484375
# 2304^3 + 4608^3 = 576^4 = 110075314176
# 23328^3 + 46656^3 = 648^5 = 114254951251968
# 50421^3 + 100842^3 = 1029^5 = 1153657446916149
# 5625^3 + 11250^3 = 1125^4 = 1601806640625
# 4131^4 + 8262^4 = 1377^5 = 4950735239250657
# 98304^3 + 196608^3 = 1536^5 = 8549802417586176
# 11664^3 + 23328^3 = 1944^4 = 14281868906496
# 177147^3 + 354294^3 = 2187^5 = 50031545098999707
# 300000^3 + 600000^3 = 3000^5 = 243000000000000000
# 21609^3 + 43218^3 = 3087^4 = 90812685325761
# 36864^3 + 73728^3 = 4608^4 = 450868486864896
# 59049^3 + 118098^3 = 6561^4 = 1853020188851841
# 90000^3 + 180000^3 = 9000^4 = 6561000000000000
# 131769^3 + 263538^3 = 11979^4 = 20591228579666481
# 186624^3 + 373248^3 = 15552^4 = 58498535041007616
# 257049^3 + 514098^3 = 19773^4 = 152858736488597841
# 345744^3 + 691488^3 = 24696^4 = 371968759094317056
# 455625^3 + 911250^3 = 30375^4 = 851265722900390625

# smaller limit (10^7)
# 3^3 + 6^3 = 3^5 = 243
# 9^3 + 18^3 = 3^8 = 6561
# 27^3 + 54^3 = 3^11 = 177147
# 81^3 + 162^3 = 3^14 = 4782969
# 9^3 + 18^3 = 9^4 = 6561
# 81^3 + 162^3 = 9^7 = 4782969
# 17^4 + 34^4 = 17^5 = 1419857
# 96^3 + 192^3 = 24^5 = 7962624
# 28^3 + 84^3 = 28^4 = 614656
# 70^3 + 105^3 = 35^4 = 1500625

# limit 10^12 (16049)
# 3^3 + 6^3 = 3^5 = 243
# 9^3 + 18^3 = 3^8 = 6561
# 27^3 + 54^3 = 3^11 = 177147
# 81^3 + 162^3 = 3^14 = 4782969
# 243^3 + 486^3 = 3^17 = 129140163
# 729^3 + 1458^3 = 3^20 = 3486784401
# 2187^3 + 4374^3 = 3^23 = 94143178827
# 9^3 + 18^3 = 9^4 = 6561
# 81^3 + 162^3 = 9^7 = 4782969
# 729^3 + 1458^3 = 9^10 = 3486784401
# 17^4 + 34^4 = 17^5 = 1419857
# 289^4 + 578^4 = 17^9 = 118587876497
# 96^3 + 192^3 = 24^5 = 7962624
# 2304^3 + 4608^3 = 24^8 = 110075314176
# 28^3 + 84^3 = 28^4 = 614656
# 784^3 + 2352^3 = 28^7 = 13492928512
# 33^5 + 66^5 = 33^6 = 1291467969
# 70^3 + 105^3 = 35^4 = 1500625
# 2450^3 + 3675^3 = 35^7 = 64339296875
# 65^3 + 260^3 = 65^4 = 17850625
# 144^3 + 288^3 = 72^4 = 26873856
# 729^3 + 1458^3 = 81^5 = 3486784401
# 82^4 + 246^4 = 82^5 = 3707398432
# 273^3 + 364^3 = 91^4 = 68574961
# 194^4 + 291^4 = 97^5 = 8587340257
# 686^3 + 2058^3 = 98^5 = 9039207968
# 126^3 + 630^3 = 126^4 = 252047376
# 266^3 + 665^3 = 133^4 = 312900721
# 456^3 + 760^3 = 152^4 = 533794816
# 3696^3 + 4368^3 = 168^5 = 133827821568
# 756^3 + 945^3 = 189^4 = 1275989841
# 3072^3 + 6144^3 = 192^5 = 260919263232
# 217^3 + 1302^3 = 217^4 = 2217373921
# 448^3 + 1344^3 = 224^4 = 2517630976
# 2508^3 + 8436^3 = 228^5 = 616132666368
# 729^3 + 1458^3 = 243^4 = 3486784401
# 1120^3 + 1680^3 = 280^4 = 6146560000
# 1705^3 + 2046^3 = 341^4 = 13521270961
# 344^3 + 2408^3 = 344^4 = 14003408896
# 702^3 + 2457^3 = 351^4 = 15178486401
# 1110^3 + 2590^3 = 370^4 = 18741610000
# 1628^3 + 2849^3 = 407^4 = 27439591201
# 2340^3 + 3276^3 = 468^4 = 47971512576
# 513^3 + 4104^3 = 513^4 = 69257922561
# 1040^3 + 4160^3 = 520^4 = 73116160000
# 1617^3 + 4312^3 = 539^4 = 84402451441
# 3354^3 + 3913^3 = 559^4 = 97644375361
# 2304^3 + 4608^3 = 576^4 = 110075314176
# 3185^3 + 5096^3 = 637^4 = 164648481361
# 4368^3 + 5824^3 = 728^4 = 280883040256
# 730^3 + 6570^3 = 730^4 = 283982410000
# 1474^3 + 6633^3 = 737^4 = 295032562561
# 2268^3 + 6804^3 = 756^4 = 326653399296
# 3172^3 + 7137^3 = 793^4 = 395451064801
# 4270^3 + 7686^3 = 854^4 = 531901827856
# 5985^3 + 6840^3 = 855^4 = 534397550625
# 5670^3 + 8505^3 = 945^4 = 797493650625


# limit 10^12 (16049)
# 3^3 + 6^3 = 3^5 = 243 This is the same as 1^3 + 2^3 = 3^2 but *3^3 on both sides
# 9^3 + 18^3 = 3^8 = 6561 and = 9^4 = 6561  This is the same as 3^3 + 6^3 = 3^5 but *3^3 on both sides
# 27^3 + 54^3 = 3^11 = 177147
# 81^3 + 162^3 = 3^14 = 4782969 and = 9^7 = 4782969
# 243^3 + 486^3 = 3^17 = 129140163
# 729^3 + 1458^3 = 3^20 = 3486784401 and = 9^10 = 3486784401
# 2187^3 + 4374^3 = 3^23 = 94143178827
# 17^4 + 34^4 = 17^5 = 1419857 This is the same as 1^4 + 2^4 = 17^1 but *17^4 on both sides
# 289^4 + 578^4 = 17^9 = 118587876497
# 96^3 + 192^3 = 24^5 = 7962624  this is the same as 4^3 + 8^3 = 24^2 but *24^3 on both sides. (1^3 + 2^3 = 3^2) * 4^3
# 2304^3 + 4608^3 = 24^8 = 110075314176 this is the same as 96^3 + 192^3 = 24^5 but *24^3 on both sides
# 28^3 + 84^3 = 28^4 = 614656 this is the same as 1^3 + 3^3 = 28 but *28^3 on both sides
# 784^3 + 2352^3 = 28^7 = 13492928512
# 33^5 + 66^5 = 33^6 = 1291467969
# 70^3 + 105^3 = 35^4 = 1500625
# 2450^3 + 3675^3 = 35^7 = 64339296875
# 65^3 + 260^3 = 65^4 = 17850625
# 144^3 + 288^3 = 72^4 = 26873856
# 729^3 + 1458^3 = 81^5 = 3486784401
# 82^4 + 246^4 = 82^5 = 3707398432
# 273^3 + 364^3 = 91^4 = 68574961
# 194^4 + 291^4 = 97^5 = 8587340257
# 686^3 + 2058^3 = 98^5 = 9039207968
# 126^3 + 630^3 = 126^4 = 252047376
# 266^3 + 665^3 = 133^4 = 312900721
# 456^3 + 760^3 = 152^4 = 533794816
# 3696^3 + 4368^3 = 168^5 = 133827821568
# 756^3 + 945^3 = 189^4 = 1275989841
# 3072^3 + 6144^3 = 192^5 = 260919263232
# 217^3 + 1302^3 = 217^4 = 2217373921
# 448^3 + 1344^3 = 224^4 = 2517630976
# 2508^3 + 8436^3 = 228^5 = 616132666368
# 729^3 + 1458^3 = 243^4 = 3486784401
# 1120^3 + 1680^3 = 280^4 = 6146560000
# 1705^3 + 2046^3 = 341^4 = 13521270961
# 344^3 + 2408^3 = 344^4 = 14003408896
# 702^3 + 2457^3 = 351^4 = 15178486401
# 1110^3 + 2590^3 = 370^4 = 18741610000
# 1628^3 + 2849^3 = 407^4 = 27439591201
# 2340^3 + 3276^3 = 468^4 = 47971512576
# 513^3 + 4104^3 = 513^4 = 69257922561
# 1040^3 + 4160^3 = 520^4 = 73116160000
# 1617^3 + 4312^3 = 539^4 = 84402451441
# 3354^3 + 3913^3 = 559^4 = 97644375361
# 2304^3 + 4608^3 = 576^4 = 110075314176
# 3185^3 + 5096^3 = 637^4 = 164648481361
# 4368^3 + 5824^3 = 728^4 = 280883040256
# 730^3 + 6570^3 = 730^4 = 283982410000
# 1474^3 + 6633^3 = 737^4 = 295032562561
# 2268^3 + 6804^3 = 756^4 = 326653399296
# 3172^3 + 7137^3 = 793^4 = 395451064801
# 4270^3 + 7686^3 = 854^4 = 531901827856
# 5985^3 + 6840^3 = 855^4 = 534397550625
# 5670^3 + 8505^3 = 945^4 = 797493650625

# 96^3 + 192^3 = 24^5
# (12*8)^3 + (24*8)^3 = (24)^5 =(3*8)^5
# (24*4)^3 + (24*8)^3 = (24)^5
# 24^3 * (4^3 + 8^3) = (24)^5
# 4^3 + 8^3 = 24^2

from util.utils import timeit, is_coprime, primes_of_n, sieve
import unittest
from functools import reduce
import operator
from math import ceil, log, floor, log10


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


class Problem678:
    def __init__(self, n):
        self.n = n

    @staticmethod
    def number_of_sum_of_squares(dc_prime):
        """
        Given the prime factorization, outputs the number of ways this number can be represented as the sum of two
        squares. Excluding the a^2 + 0^2 case.
        This function does not consider any powers of 2, this simplifies the exceptions.
        Ignore powers of 2. 1 mod 4 primes must exist. 3 mod 4 primes must be even power.
        """
        # n is a sum of two squares iff it factors as n = ab^2, where a has no prime factor p ≡ 3 (mod 4)
        # 3 mod 4 primes must all be even powers
        if any(x % 2 != 0 for p, x in dc_prime.items() if p % 4 == 3):  # odd powers of bad primes
            return 0
        # NOTE: THIS EXCLUDES 0, SO NO 2^2 + 0^2 = 4.
        # n is a sum of two squares iff it factors as n = ab^2, where a has no prime factor p ≡ 3 (mod 4)
        # 3 mod 4 primes must all be even powers

        # At least one 1mod4 prime must exist. Ignoring the special condition of powers of 2.
        mod_4_remainder_1 = {k: v for k, v in dc_prime.items() if k % 4 == 1}
        if len(mod_4_remainder_1) == 0:
            return 0

        num_of_partitions = ceil(prod(v + 1 for k, v in mod_4_remainder_1.items()) / 2)
        # if perfect square then subtract 1 to eliminate the solution 0 + b^2 = square
        if all(exp % 2 == 0 for p, exp in mod_4_remainder_1.items()):
            num_of_partitions -= 1

        return num_of_partitions

    @timeit
    def solve(self):
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        max_c = int(round(self.n**(1/3)))
        ls_primes = list(sieve(max_c))
        answer = 0
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        # for c in range(2, round(self.n**(1/3))+1):

        n_log = log(self.n)

        # # c = 3
        # c = 3
        # dc_prime = {3: 1}
        # max_f = floor(round(n_log / log(c), 2))
        # for f in range(3, max_f + 1):
        #     new_dc_prime = {k: v * f for k, v in dc_prime.items()}
        #
        #     # check if sum of squares
        #     answer += self.number_of_sum_of_squares(new_dc_prime)
        #     answer += self.check_if_sum_of_powers_special(round(c ** f), c, f, dc_prime, new_dc_prime, lowest_e=3)

        # for c in range(4, max_c + 1):  # todo prove that c=2 does not work. This simplifies the below logic
        for c in range(3, max_c + 1):  # todo prove that c=2 does not work. This simplifies the below logic
            dc_prime = primes_of_n(c, ls_primes)
            f = 3
            new_dc_prime = {k: v*f for k, v in dc_prime.items()}
            while c**f <= self.n:
                # check if sum of squares
                answer += self.number_of_sum_of_squares(new_dc_prime)
                # todo speed this part up
                answer += self.check_if_sum_of_powers(round(c**f), c, f, dc_prime, new_dc_prime, lowest_e=3)
                f += 1
                new_dc_prime = {k: v * f for k, v in dc_prime.items()}
        return answer

    @timeit
    def solve3(self):
        # lowest value of f is 3
        # Therefore the highest value of c is N**(1/3)
        max_c = int(round(self.n ** (1 / 3)))
        ls_primes = list(sieve(max_c))
        answer = 0
        n_log = log10(self.n)

        for c in range(3, max_c + 1):  # todo prove that c=2 does not work. This simplifies the below logic
            dc_prime = primes_of_n(c, ls_primes)
            max_f = floor(round(n_log/log10(c), 12))
            dc_fermat_sum = self.calc_dc_possible_fermat_sum(limit=round(c**max_f), c=c, max_f=max_f, lowest_e=3)
            # print(dc_fermat_sum)
            # print("Done generating possible fermat sums for c = {}".format(c))
            # if max_f * log(c) > n_log:
            #     print('f')
            assert max_f * log10(c) <= n_log
            for f in range(3, max_f + 1):
                new_dc_prime = {k: v * f for k, v in dc_prime.items()}
                # check if sum of squares
                answer += self.number_of_sum_of_squares(new_dc_prime)
                answer += dc_fermat_sum.get(round(c ** f), 0)

                # info
                if dc_fermat_sum.get(round(c ** f), 0) != 0:
                    print(c, f, round(c ** f))
        return answer

    @staticmethod
    def calc_dc_possible_fermat_sum(limit, c, max_f, lowest_e=3):
        """
        Returns the set of many a^e + b^e, for a < b. Where a and b are multiples of c.
        Beal's conjecture: a,b,c must have a common prime factor.
        """
        dc_fermat_sum = dict()
        for a in range(c, round((limit / 2) ** (1 / lowest_e)) + 1, c):
            for b in range(a + c, round((limit - a ** lowest_e) ** (1 / lowest_e) + 1), c):
                e = lowest_e
                fermat_sum = round(a**e + b**e)
                while fermat_sum <= limit:
                    if fermat_sum in dc_fermat_sum.keys():
                        dc_fermat_sum[fermat_sum] += 1
                    else:
                        dc_fermat_sum[fermat_sum] = 1
                    e += 1
                    fermat_sum = round(a**e + b**e)

        return dc_fermat_sum

    @staticmethod
    def check_if_sum_of_powers(limit, c, f, dc_prime_c, dc_prime_cf, lowest_e=2):
        """
        Returns how many a^e + b^e = limit, for a < b. Where limit = c^f.
        Beal's conjecture: a,b,c must have a common prime factor.
        """
        count = 0
        # for a in range(1, round((limit/2)**(1/lowest_e))+1):  # way too many
        #     for b in range(a+1, round((limit - a**lowest_e)**(1/lowest_e) + 1)):  # way too many
        for a in range(c, round((limit / 2) ** (1 / lowest_e)) + 1, c):  # way too many
            if f == 3:
                range_b = [2*a]
            else:
                range_b = range(a + c, round((limit - a ** lowest_e) ** (1 / lowest_e) + 1), c)
            for b in range_b:  # way too many
                e = lowest_e  # e must be either 2 or coprime to f
                fermat_sum = round(a**e + b**e)
                while fermat_sum < limit:
                    e += 1
                    fermat_sum = round(a**e + b**e)
                if fermat_sum == limit:
                    count += 1
                    print("{}^{} + {}^{} = {}^{} = {}".format(a, e, b, e, c, f, limit))
        return count

    # @staticmethod
    # def check_if_sum_of_powers_special(limit, c, f, dc_prime_c, dc_prime_cf, lowest_e=3):
    #     """
    #     Returns how many a^e + b^e = limit, for a < b. Where limit = c^f.
    #     Beal's conjecture: a,b,c must have a common prime factor.
    #     """
    #     count = 0
    #     # for a in range(1, round((limit/2)**(1/lowest_e))+1):  # way too many
    #     #     for b in range(a+1, round((limit - a**lowest_e)**(1/lowest_e) + 1)):  # way too many
    #     for a in range(c, round((limit / 2) ** (1 / lowest_e)) + 1, c):  # way too many
    #
    #         b = 2*a  # more cases than just this exist
    #         e = lowest_e  # e must be either 2 or coprime to f
    #         fermat_sum = round(a**e + b**e)
    #         while fermat_sum < limit:
    #             e += 1
    #             fermat_sum = round(a**e + b**e)
    #         if fermat_sum == limit:
    #             count += 1
    #             print("{}^{} + {}^{} = {}^{} = {}".format(a, e, b, e, c, f, limit))
    #     return count


class Solution678(unittest.TestCase):
    def setUp(self):
        # self.problem = Problem678(n=int(1e3))
        pass

    def test_smallest_solution(self):
        problem = Problem678(n=int(1e3))
        self.assertEqual(7, problem.solve())

    def test_small_solution(self):
        problem = Problem678(n=int(1e5))
        self.assertEqual(53, problem.solve())

    def test_big_sample_solution(self):
        problem = Problem678(n=int(1e7))
        self.assertEqual(287, problem.solve())

    def test_smallest_solution3(self):
        problem = Problem678(n=int(1e3))
        self.assertEqual(7, problem.solve3())

    def test_small_solution3(self):
        problem = Problem678(n=int(1e5))
        self.assertEqual(53, problem.solve3())

    def test_big_sample_solution3(self):
        problem = Problem678(n=int(1e7))
        self.assertEqual(287, problem.solve3())

    def test_bigger_sample_solution(self):
        problem = Problem678(n=int(1e12))
        self.assertEqual(16049, problem.solve())

    def test_bigger_sample_solution3(self):
        problem = Problem678(n=int(1e12))
        self.assertEqual(16049, problem.solve3())

    # 1e12 takes 41 seconds

    # 1e18 for just case 1 takes: 24 seconds

    # def test_big(self):
    #     problem = Problem678(n=int(1e18))
    #     print(problem.solve())


if __name__ == '__main__':
    unittest.main()
