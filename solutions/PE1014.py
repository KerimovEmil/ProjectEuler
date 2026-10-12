r"""
PROBLEM

A club has $7$ members, named $\mathtt A$ to $\mathtt G$.
Every night, $3$ of the $7$ members come to the club. After several nights, they find that for every combination of $2$ members, there is exactly one night when they both come.

If the members who come on the first $2$ nights are $\mathtt{ABC}$ and $\mathtt{BDF}$ respectively, then on the night that $\mathtt E$ and $\mathtt G$ both come, the members who come must be $\mathtt{BEG}$.

A larger club has $24$ members, named $\mathtt A$ to $\mathtt X$.
Every night, $8$ of the $24$ members come to the club. After several nights, they find that for every combination of $5$ members, there is exactly one night when they all come.

Here are the members who come on the first $11$ nights:
ABCDKMPR
ABJKLMNW
ACIOQTUW
ADFMPQTU
AEFNPTVX
AEFQRSTW
AEGIMQSU
BDEKORUX
BEFGHIKU
DEFHKOSW
FHIJKRST

Find the members who come on the night that $\mathtt{CGJLV}$ all come. Enter your answer by concatenating the names in alphabetic order.

ANSWER: CFGJLMVW
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Witt Design $W_{24} = S(5, 8, 24)$ and the Extended Binary Golay Code $\mathcal{G}_{24}$:
   - A family of $8$-element subsets (octads) of a $24$-element set such that every $5$-element
     subset is contained in a unique octad is the Steiner system $S(5, 8, 24)$, which is unique
     up to isomorphism.
   - Its $759$ blocks are precisely the weight-$8$ codewords (octads) of the extended binary
     Golay code $\mathcal{G}_{24}$, a $[24, 12, 8]$ linear code over $\mathbb{F}_2$.
   - The $11$ given blocks are linearly independent over $\mathbb{F}_2$ and, together with the
     all-ones vector $\mathbf{1}_{24}$ (or strictly within the $11$-dimensional span), generate
     all codewords of $\mathcal{G}_{24}$.

2. Sample Case $S(2, 3, 7)$ and the Dual Hamming Code:
   - In $S(2, 3, 7)$ (the Fano plane), the complements of the $7$ blocks of size $3$ form the
     non-zero codewords of the $[7, 3, 4]$ simplex code (dual of the $[7, 4, 3]$ Hamming code).
   - Equivalently, for any two distinct blocks $B_1, B_2 \in S(2, 3, 7)$, $|B_1 \cap B_2| = 1$,
     and the complement $(B_1 \cup B_2)^c$ is the unique block disjoint from $B_1 \triangle B_2$,
     sharing $B_1 \cap B_2$.
"""

import unittest
from util.utils import timeit

DEFAULT_BLOCKS_24 = (
    "ABCDKMPR",
    "ABJKLMNW",
    "ACIOQTUW",
    "ADFMPQTU",
    "AEFNPTVX",
    "AEFQRSTW",
    "AEGIMQSU",
    "BDEKORUX",
    "BEFGHIKU",
    "DEFHKOSW",
    "FHIJKRST",
)


class Problem1014:
    def __init__(
        self,
        t: int = 5,
        k: int = 8,
        v: int = 24,
        given_blocks: tuple[str, ...] = DEFAULT_BLOCKS_24,
        query: str = "CGJLV",
    ):
        self.t = t
        self.k = k
        self.v = v
        self.given_blocks = given_blocks
        self.query = query

    @staticmethod
    def _to_mask(s: str) -> int:
        mask = 0
        for ch in s:
            mask |= 1 << (ord(ch) - ord("A"))
        return mask

    @staticmethod
    def _from_mask(mask: int, v: int) -> str:
        return "".join(chr(ord("A") + i) for i in range(v) if (mask >> i) & 1)

    @staticmethod
    def _span_gf2(vectors: list[int]) -> list[int]:
        basis: list[int] = []
        for vec in vectors:
            for b in basis:
                vec = min(vec, vec ^ b)
            if vec:
                basis.append(vec)
                basis.sort(reverse=True)
        codewords = [0]
        for b in basis:
            codewords += [c ^ b for c in codewords]
        return codewords

    def _solve_fano(self, target_mask: int, all_ones: int) -> str:
        comp_vecs = [self._to_mask(b) ^ all_ones for b in self.given_blocks]
        for c in self._span_gf2(comp_vecs):
            block = c ^ all_ones
            if block.bit_count() == self.k and (block & target_mask) == target_mask:
                return self._from_mask(block, self.v)

        if len(self.given_blocks) >= 2:
            b1 = self._to_mask(self.given_blocks[0])
            b2 = self._to_mask(self.given_blocks[1])
            b3 = (b1 & b2) | (all_ones ^ (b1 | b2))
            if b3.bit_count() == self.k and (b3 & target_mask) == target_mask:
                return self._from_mask(b3, self.v)
        raise ValueError(f"No block found containing {self.query}")

    @timeit
    def solve(self) -> str:
        all_ones = (1 << self.v) - 1
        target_mask = self._to_mask(self.query)

        if (self.t, self.k, self.v) == (2, 3, 7):
            return self._solve_fano(target_mask, all_ones)

        # For S(5, 8, 24), the blocks are the weight-8 codewords of the extended binary Golay code G_24.
        vecs = [self._to_mask(b) for b in self.given_blocks] + [all_ones]
        for c in self._span_gf2(vecs):
            if c.bit_count() == self.k and (c & target_mask) == target_mask:
                return self._from_mask(c, self.v)

        raise ValueError(f"No block found containing {self.query}")


class Solution1014(unittest.TestCase):
    def setUp(self):
        self.problem = Problem1014()

    def test_sample(self):
        sample = Problem1014(t=2, k=3, v=7, given_blocks=("ABC", "BDF"), query="EG")
        self.assertEqual("BEG", sample.solve())

    def test_solution(self):
        self.assertEqual("CFGJLMVW", self.problem.solve())


if __name__ == "__main__":
    unittest.main()
