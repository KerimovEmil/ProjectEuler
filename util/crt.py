from typing import List, Set
from math import gcd
from itertools import product


class NoSolutionException(Exception): pass


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
            (x, y) = self.__extended_gcd(m, n)  # solve for x,y such that m*x + n*y = 1
            primary_root = b*x*m + a*n*y
            root = (primary_root // g) % q
            a, m = root, q
        return a

    @staticmethod
    def __extended_gcd(a, b):
        (x, y) = (0, 1)
        (last_x, last_y) = (1, 0)
        while b != 0:
            (q, r) = divmod(a, b)
            (a, b) = (b, r)
            (x, last_x) = (last_x - q * x, x)
            (y, last_y) = (last_y - q * y, y)
        return last_x, last_y


class ChineseRemainderTheoremSets:
    """
    Solve x = {a_i} (mod n_i) where n_i are coprime.
    """
    def __init__(self, a_sets: List[Set[int]], n_list: List[int]):
        self.a_sets = a_sets
        self.n_list = n_list

    def __call__(self) -> Set[int]:
        sol_set = set()
        for a_list in product(*self.a_sets):
            try:
                sol = ChineseRemainderTheorem(a_list=a_list, n_list=self.n_list).solve()
                sol_set.add(sol)
            except NoSolutionException:
                pass
        return sol_set
