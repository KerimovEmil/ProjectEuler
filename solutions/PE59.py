"""
PROBLEM

Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for
 Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value,
taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text,
restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

Your task has been made easy, as the encryption key consists of three lower case characters. Using p059_cipher.txt
(right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the
 plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the
 original text.


ANSWER: 129448
Solve time ~1.6 seconds
"""

from util.utils import timeit
import unittest
import os
from string import ascii_lowercase
from itertools import product


class Problem59:
    def __init__(self, txt_file):
        with open(txt_file, 'r') as f:
            str_line = f.read()
        self.ls_codes = [int(x) for x in str_line.split(',')]

    def xor_every_third_element(self, key, start):
        return [chr(key ^ x) for x in self.ls_codes[start::3]]

    @timeit
    def solve(self):

        max_hit_rate = 0
        best_answer_message = ''
        for key_tup in product(ascii_lowercase, repeat=3):
            ls_decoded_1 = self.xor_every_third_element(key=ord(key_tup[0]), start=0)
            ls_decoded_2 = self.xor_every_third_element(key=ord(key_tup[1]), start=1)
            ls_decoded_3 = self.xor_every_third_element(key=ord(key_tup[2]), start=2)

            str_decoded = ''.join([''.join([x, y, z]) for x, y, z in zip(ls_decoded_1, ls_decoded_2, ls_decoded_3)])

            # The most commonly used letters of the English language are e, t, a, i, o, n, s, h, r
            num = len([x for x in str_decoded if x in ['e', 't', 'a']])

            if num > max_hit_rate:
                max_hit_rate = num
                best_answer_message = str_decoded

            # break condition
            if 'Euler' in str_decoded:
                return sum([ord(x) for x in str_decoded])

        return sum([ord(x) for x in best_answer_message])


class Solution59(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p059_cipher.txt')
        self.problem = Problem59(txt_file=file_path)

    def test_solution(self):
        self.assertEqual(129448, self.problem.solve())


if __name__ == '__main__':
    unittest.main()

