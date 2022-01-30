"""
PROBLEM

There are several ways to write the number 1/2 as a sum of inverse squares using distinct integers.

For instance, the numbers {2,3,4,5,7,12,15,20,28,35} can be used.

In fact, only using integers between 2 and 45 inclusive, there are exactly three ways to do it,
the remaining two being: {2,3,4,6,7,9,10,20,28,35,36,45} and
 {2,3,4,6,7,9,12,15,28,30,35,36,45}.

How many ways are there to write the number 1/2 as a sum of inverse squares using distinct integers between 2 and 80 inclusive?

ANSWER:
Solve time ~s seconds
"""


from util.utils import timeit
import unittest
from fractions import Fraction

x1 = {2,3,4,5,7,12,15,20,28,35}
x2 = {2,3,4,6,7,9,10,20,28,35,36,45}
x3 = {2,3,4,6,7,9,12,15,28,30,35,36,45}

CANDIDATES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 18, 20, 21, 24, 28,
              30, 35, 36, 39, 40, 42, 45, 52, 56, 60, 63, 70, 72]

LS_POSSIBLE_REMOVE = [12, 13, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 39, 40, 42, 45, 52, 56, 60, 63, 70, 72]

def sum_of_recip_sq_frac(s):
    return sum(Fraction(1, i**2) for i in s)

from itertools import chain, combinations

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

# def powerset(iterable):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# sum_of_recip_sq_frac(CANDIDATES) - Fraction(1,2)
# Fraction(155, 1728)


def sum_of_recip_sq(s):
    return sum(pow(i, -2) for i in s)


target_sum = Fraction(1, 2)


from itertools import combinations

def sub_set_sum(size, my_array, sub_set_sum):
   for i in range(size+1):
      for my_sub_set in combinations(my_array, i):
         if sum(my_sub_set) == sub_set_sum:
            print(list(my_sub_set))

my_size = 6
my_list = [21, 32, 56, 78, 45, 99, 0]
print("The list is :")
print(my_list)
subset_sum = 53
print("The result is :")
sub_set_sum(my_size, my_list, subset_sum)

# [t for t in powerset(LS_POSSIBLE_REMOVE) if sum_of_recip_sq_frac(t) ==Fraction(155, 1728)]

def f(s_)

possible_solution = set()
for c in CANDIDATES:
    temp_solution = possible_solution
    temp_solution.add(c)
    if sum_of_recip_sq_frac(temp_solution) < Fraction(1,2):



def is_square(n: int):
    sq = n ** 0.5
    if abs(sq - int(sq)) < 1e-10:
        return True


first_sum = sum(1/i**2 for i in range(2, 36))
remainder_sum = sum(1/i**2 for i in range(36, 46))


def sum_of_recip_sq(s):
    return sum(1/i**2 for i in s)


for n in x1:
    for x in range(36, 46):
        w = Fraction(1, n**2) - Fraction(1, x**2)
        if w.numerator == 1:
            if is_square(w.denominator):
                print(n, x, w)

ls_x1 = list(x1)
up_to = 81
for i, n in enumerate(ls_x1):
    for m in ls_x1[i+1:]:
        first_total = Fraction(1, n**2) + Fraction(1, m**2)
        for x in range(2, up_to):
            if x in x1:
                continue
            for y in range(x+1, up_to):
                if y in x1:
                    continue
                second_total = Fraction(1, x**2) + Fraction(1, y**2)
                check = first_total - second_total
                if check.numerator == 1:
                    if is_square(check.denominator):
                        z = int(check.denominator**0.5)
                        if z in x1:
                            continue
                        if z <= y:
                            continue
                        # print(f'n={n}, m={m}, x={x}, y={y}, z={z}')
                        print(f'1/{n}^2 + 1/{m}^2 = 1/{x}^2 + 1/{y}^2 + 1/{z}^2')



class Problem152:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')


class Solution152(unittest.TestCase):
    def setUp(self):
        self.problem = Problem152()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

