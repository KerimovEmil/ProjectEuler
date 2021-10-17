from typing import List, Set
from math import gcd
from itertools import product


class NoSolutionException(Exception):
    pass


def bezout_thm(a: int, b: int) -> (int, int):
    """
    return x,y such that a*x + b*y = 1, using the extended gcd algorithm
    """
    (x, y) = (0, 1)
    (last_x, last_y) = (1, 0)
    while b != 0:
        (q, r) = divmod(a, b)
        (a, b) = (b, r)
        (x, last_x) = (last_x - q * x, x)
        (y, last_y) = (last_y - q * y, y)
    return last_x, last_y


class SetInteger(Set):
    """Class for sets of integers"""
    def __mul__(self, other: int):
        if isinstance(other, int):
            return SetInteger(other*x for x in self)
        else:
            return NotImplementedError

    def __rmul__(self, other):
        """Defining x * object as object * x"""
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, int):
            return SetInteger(other + x for x in self)
        elif isinstance(other, SetInteger):  # this is the slowest part
            return SetInteger(x+y for x, y in product(self, other))
        else:
            return NotImplementedError

    def __floordiv__(self, other):
        if isinstance(other, int):
            return SetInteger({x // other for x in self})
        else:
            return NotImplementedError

    def __mod__(self, other):
        if isinstance(other, int):
            return SetInteger({x % other for x in self})
        else:
            return NotImplementedError


class ChineseRemainderTheorem:
    """
    Solve x = a_i (mod n_i)
    Note that is a_i are not co-prime then a_i == a_j mod gcm(n_i, n_j)
    """

    def __init__(self, a_list: List[int], n_list: List[int]):
        self.a_list = a_list
        self.n_list = n_list

        assert len(self.a_list) == len(self.n_list)

        # check for non-coprime conditions
        for i, (m, n) in enumerate(zip(self.n_list[:-1], self.n_list[1:])):
            g = gcd(m, n)
            if (self.a_list[i] - self.a_list[i + 1]) % g != 0:
                # print(f'm={m}, n={n}, a={self.a_list[i]}, b={self.a_list[i + 1]}, g={g}')
                raise NoSolutionException()

    def solve(self):
        a = self.a_list[0]
        m = self.n_list[0]
        for n, b in zip(self.n_list[1:], self.a_list[1:]):
            g = gcd(m, n)
            q = m*n // g
            (x, y) = bezout_thm(m, n)  # solve for x,y such that m*x + n*y = 1
            primary_root = b*x*m + a*n*y
            root = (primary_root // g) % q
            a, m = root, q
        return a


class ChineseRemainderTheoremSets:
    """
    Solve x = {a_i} (mod n_i)
    Note that is a_i are not co-prime then a_i == a_j mod gcm(n_i, n_j)
    """
    def __init__(self, a_sets: List[Set[int]], n_list: List[int]):
        self.a_sets = [SetInteger(x) for x in a_sets]
        self.n_list = n_list

    def __call__(self) -> SetInteger:
        a_set = self.a_sets[0]
        m = self.n_list[0]
        for n, b_set in zip(self.n_list[1:], self.a_sets[1:]):
            g = gcd(m, n)
            q = m * n // g
            (x, y) = bezout_thm(m, n)  # solve for x,y such that m*x + n*y = 1
            root = SetInteger()
            for mod_g_subset in (a_set % g):
                # if a%g != b%g then there are no solutions
                a_sub_set = SetInteger({x for x in a_set if x % g == mod_g_subset})
                b_sub_set = SetInteger({x for x in b_set if x % g == mod_g_subset})
                primary_root = x * (m//g) * b_sub_set + (n//g) * y * a_sub_set
                root = SetInteger(root.union(primary_root % q))

            a_set, m = root, q
        return a_set
