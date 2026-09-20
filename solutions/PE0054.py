"""
PROBLEM

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example,
 a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players
  have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards
  tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand	 Player 1	 	            Player 2	 	Winner
1	 	5H 5C 6S 7S KD         2C 3S 8S 8D TD
        Pair of Fives           Pair of Eights     Player 2
2	 	5D 8C 9S JS AC         2C 5C 7D 8S QH
        Highest card Ace       Highest card Queen  Player 1
3	 	2D 9C AS AH AC          3D 6D 7D TD QD
        Three Aces 	        Flush with Diamonds    Player 2
4	 	4D 6S 9H QH QC      	3D 6D 7H QD QS
        Pair of Queens         Pair of Queens
        Highest card Nine     Highest card Seven   Player 1
5	 	2H 2D 4C 4D 4S          3C 3D 3S 9S 9D
        Full House              Full House
        With Three Fours        with Three Threes   Player 1

The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains
ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards.
 You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no
  specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?

ANSWER: 376
Solve time: ~0.035 seconds
"""

from collections import Counter
from enum import IntEnum
import os

import unittest
from util.utils import timeit


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):  # high card comparison
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return "{}{}".format(self.suit, self.value)

    @staticmethod
    def to_cards(string):
        cards = string.split(' ')
        special = {
            'J': 11,
            'T': 10,
            'Q': 12,
            'K': 13,
            'A': 14
        }
        ds = {
            **special,
            **{str(i): i for i in range(2, 10)}
        }

        cs = []
        for c in cards:
            n = ds[c[0]]
            s = c[1]
            cs.append(Card(n, s))

        return cs


class HandType(IntEnum):
    HighCard = 1
    OnePair = 2
    TwoPairs = 3
    ThreeofaKind = 4
    Straight = 5
    Flush = 6
    FullHouse = 7
    FourofaKind = 8
    StraightFlush = 9
    RoyalFlush = 10


class Hand:

    def __init__(self, hand_type, ls_cards, ls_important):
        self.ht = hand_type
        self.ls_cards = ls_cards
        self.lsi = ls_important

    def __lt__(self, other):  # high card comparison
        if self.ht < other.ht:
            return True
        elif self.ht > other.ht:
            return False
        else:
            val = self.cmp(self.lsi, other.lsi)
            if val:
                return val < 0
            else:
                val = self.cmp(self.ls_cards, other.ls_cards)
                if val:
                    return val < 0
                else:
                    return False

    def __gt__(self, other):
        if self.ht > other.ht:
            return True
        elif self.ht < other.ht:
            return False
        else:
            val = self.cmp(self.lsi, other.lsi)
            if val:
                return val > 0
            else:
                val = self.cmp(self.ls_cards, other.ls_cards)
                if val:
                    return val > 0
                else:
                    return False

    def __eq__(self, other):
        return (self.ht is other.ht) and (self.cmp(self.ls_cards, other.ls_cards) == 0)

    def __repr__(self):
        return "{} / {} / {}".format(self.ht, self.lsi, self.ls_cards)

    @staticmethod
    def cmp(cards1, cards2):
        c1 = Counter([x.value for x in cards1])
        c2 = Counter([x.value for x in cards2])

        sc1 = sorted(c1.items(), reverse=True, key=lambda x: (x[1], x[0]))
        sc2 = sorted(c2.items(), reverse=True, key=lambda x: (x[1], x[0]))

        for a, b in zip(sc1, sc2):
            if a[0] < b[0]:
                return -1
            if a[0] > b[0]:
                return 1
            else:
                continue
        return 0


class HandBuilder:
    def __init__(self, cards):
        self.cards = cards
        self.values = [x.value for x in cards]
        self.suits = [x.suit for x in cards]
        self.ic = None
        self.c = Counter(self.values)

    def build(self):
        if self.is_royal_flush():
            return Hand(HandType.RoyalFlush, self.cards, self.ic)
        elif self.is_straight_flush():
            return Hand(HandType.StraightFlush, self.cards, self.ic)
        elif self.four_kind():
            return Hand(HandType.FourofaKind, self.cards, self.ic)
        elif self.full_house():
            return Hand(HandType.FullHouse, self.cards, self.ic)
        elif self.flush():
            return Hand(HandType.Flush, self.cards, self.ic)
        elif self.straight():
            return Hand(HandType.Straight, self.cards, self.ic)
        elif self.threekind():
            return Hand(HandType.ThreeofaKind, self.cards, self.ic)
        elif self.twopair():
            return Hand(HandType.TwoPairs, self.cards, self.ic)
        elif self.onepair():
            return Hand(HandType.OnePair, self.cards, self.ic)
        elif self.high():
            return Hand(HandType.HighCard, self.cards, self.ic)
        else:
            raise NotImplementedError("WTF")

    def is_royal_flush(self):
        is_same_suit = (len(set(self.suits)) == 1)
        is_royal = len(({10, 11, 12, 13, 14}.intersection(set(self.values)))) == 5
        self.ic = self.cards
        return is_royal and is_same_suit

    def is_straight_flush(self):
        is_same_suit = (len(set(self.suits)) == 1)
        is_conseq_a = max(self.values) - min(self.values) == 4
        is_conseq_b = len(set(self.values)) == 5
        self.ic = self.cards
        return is_same_suit and is_conseq_a and is_conseq_b

    def four_kind(self):
        toDrop = None
        for k, v in self.c.items():
            if v == 1:
                toDrop = k
                break
        self.ic = [x for x in self.cards if x.value != toDrop]
        return 4 in self.c.values()

    def full_house(self):
        self.ic = self.cards
        c = Counter(self.values)
        return len({2, 3}.intersection(set(c.values()))) == 2

    def flush(self):
        self.ic = self.cards
        is_same_suit = (len(set(self.suits)) == 1)
        return is_same_suit

    def straight(self):
        self.ic = self.cards
        is_conseq_a = max(self.values) - min(self.values) == 4
        is_conseq_b = len(set(self.values)) == 5
        return is_conseq_b and is_conseq_a

    def threekind(self):
        toKeep = None
        for k, v in self.c.items():
            if v == 3:
                toKeep = k
                break

        self.ic = [x for x in self.cards if x.value == toKeep]
        return 3 in self.c.values()

    def twopair(self):
        c = Counter(self.c.values())
        toDrop = None
        for k, v in self.c.items():
            if v == 1:
                toDrop = k
        self.ic = [x for x in self.cards if x.value != toDrop]
        return c.get(2) == 2

    def onepair(self):
        toKeep = None
        for k, v in self.c.items():
            if v == 2:
                toKeep = k
        self.ic = [x for x in self.cards if x.value == toKeep]
        return 2 in self.c.values()

    def high(self):
        self.ic = [max(self.cards)]
        return True


class Problem54:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    @timeit
    def solve(self):
        p1 = 0
        p2 = 0
        with open(self.txt_file, 'r') as f:
            for line in f:
                cs = Card.to_cards(line)
                h1 = HandBuilder(cs[:5]).build()
                h2 = HandBuilder(cs[5:]).build()
                if h1 > h2:
                    p1 += 1
                elif h2 > h1:
                    p2 += 1
                else:
                    print('WTFFFFFFFFFFFF whyyyyyyyy?')
                    p1 += 0.5
                    p2 += 0.5
        return p1


class Solution54(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p054_poker.txt')
        self.problem = Problem54(txt_file=file_path)

    def test_solution(self):
        self.assertEqual(376, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
