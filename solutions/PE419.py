"""
The look and say sequence goes 1, 11, 21, 1211, 111221, 312211, 13112221, 1113213211, ...
The sequence starts with 1 and all other members are obtained by describing the previous member in terms of consecutive digits.
It helps to do this out loud:
1 is 'one one' → 11
11 is 'two ones' → 21
21 is 'one two and one one' → 1211
1211 is 'one one, one two and two ones' → 111221
111221 is 'three ones, two twos and one one' → 312211
...

Define A(n), B(n) and C(n) as the number of ones, twos and threes in the n'th element of the sequence respectively.
One can verify that A(40) = 31254, B(40) = 20259 and C(40) = 11625.

Find A(n), B(n) and C(n) for n = 1012.
Give your answer modulo 230 and separate your values for A, B and C by a comma.
E.g. for n = 40 the answer would be 31254,20259,11625

ANSWER: 998567458,1046245404,43363922
Solve time ~21 seconds
"""

import unittest
from util.utils import timeit


# the look and say sequence only has a finite amount of 'atoms'. Hence we just need to know how the atoms
# evolve to the others
# solution from https://titanwolf.org/Network/Articles/Article?AID=32bdf7b4-e007-4e9d-a8a6-679d860f970d


class Matrix:
    def multiply(self, x, y, mod):
        results = [[0 for _ in range(len(y[0]))] for _ in range(len(x))]
        for i in range(len(x)):
            for j in range(len(y[0])):
                for k in range(len(y)):
                    results[i][j] = (results[i][j] + x[i][k] * y[k][j]) % mod
        return results

    def power(self, x, power, mod):
        base = x
        rv = self.identity_matrix(len(x))
        while power > 0:
            if power & 1 == 1:
                rv = self.multiply(rv, base, mod)
            base = self.multiply(base, base, mod)
            power >>= 1
        return rv

    def identity_matrix(self, n):
        rv = [[0 for _ in range(n)] for i in range(n)]
        for i in range(n):
            rv[i][i] = 1
        return rv


class Problem:
    def __init__(self, mod):
        self.mod = mod
        self.trivial_sequence_list = [None, '1', '11', '21', '1211', '111221', '312211', '13112221']
        self.subsequence_list = [
            '1112', '1112133', '111213322112', '111213322113', '1113', '11131', '111311222112', '111312', '11131221',
            '1113122112', '1113122113', '11131221131112', '111312211312', '11131221131211', '111312211312113211',
            '111312211312113221133211322112211213322112', '111312211312113221133211322112211213322113',
            '11131221131211322113322112', '11131221133112', '1113122113322113111221131221', '11131221222112',
            '111312212221121123222112', '111312212221121123222113', '11132', '1113222', '1113222112', '1113222113',
            '11133112', '12', '123222112', '123222113', '12322211331222113112211', '13', '131112',
            '13112221133211322112211213322112', '13112221133211322112211213322113', '13122112', '132', '13211',
            '132112', '1321122112', '132112211213322112', '132112211213322113', '132113', '1321131112', '13211312',
            '1321132', '13211321', '132113212221', '13211321222113222112', '1321132122211322212221121123222112',
            '1321132122211322212221121123222113', '13211322211312113211', '1321133112', '1322112', '1322113',
            '13221133112', '1322113312211', '132211331222113112211', '13221133122211332', '22', '3', '3112',
            '3112112', '31121123222112', '31121123222113', '3112221', '3113', '311311', '31131112', '3113112211',
            '3113112211322112', '3113112211322112211213322112', '3113112211322112211213322113', '311311222',
            '311311222112', '311311222113', '3113112221131112', '311311222113111221', '311311222113111221131221',
            '31131122211311122113222', '3113112221133112', '311312', '31132', '311322113212221', '311332',
            '3113322112', '3113322113', '312', '312211322212221121123222113', '312211322212221121123222112', '32112']
        self.evolving_list = [
            [62], [63, 61], [64], [65], [67], [68], [83, 54], [69], [70], [75], [76], [81], [77], [78], [79],
            [80, 28, 90], [80, 28, 89], [80, 29], [74, 28, 91], [74, 31], [71], [72], [73], [82], [85], [86],
            [87], [88, 91], [0], [2], [3], [1, 60, 28, 84], [4], [27], [23, 32, 60, 28, 90], [23, 32, 60, 28, 89],
            [6], [7], [8], [9], [20], [21], [22], [10], [18], [11], [12], [13], [14], [17], [15], [16], [19],
            [5, 60, 28, 91], [25], [26], [24, 28, 91], [24, 28, 66], [24, 28, 84], [24, 28, 67, 60, 28, 88],
            [60], [32], [39], [40], [41], [42], [37, 38], [43], [47], [53], [48], [49], [50], [51], [46, 37],
            [46, 54], [46, 55], [46, 56], [46, 57], [46, 58], [46, 59], [46, 32, 60, 28, 91], [44], [45], [52],
            [37, 28, 88], [37, 29], [37, 30], [33], [35], [34], [36]
        ]
        self.transition_matrix = self.__init_transition_matrix()
        self.initial_state = self.__init_initial_state()

    def __init_transition_matrix(self):
        transition_matrix = [[0 for _ in range(92)] for _ in range(92)]
        for i in range(92):
            for j in self.evolving_list[i]:
                transition_matrix[j][i] += 1
        return transition_matrix

    def __init_initial_state(self):
        initial_state = [[0] for _ in range(92)]
        initial_state[23][0] = 1
        initial_state[38][0] = 1
        return initial_state

    def solve(self, n):
        return ','.join(str(i) for i in self.get(n))

    def get(self, n):
        if n < 8:
            return [self.trivial_sequence_list[n].count(d) for d in ['1', '2', '3']]

        x = Matrix().power(self.transition_matrix, n - 8, self.mod)
        y = Matrix().multiply(x, self.initial_state, self.mod)
        output = [0, 0, 0]
        for i in range(92):
            subsequence_count = y[i][0]
            subsequence = self.subsequence_list[i]
            output[0] = (output[0] + subsequence_count * subsequence.count('1')) % self.mod
            output[1] = (output[1] + subsequence_count * subsequence.count('2')) % self.mod
            output[2] = (output[2] + subsequence_count * subsequence.count('3')) % self.mod
        return output


class Problem419:
    def __init__(self, mod):
        self.mod = mod

    @timeit
    def solve(self, n):
        return Problem(mod=self.mod).solve(n=n)

        # start = '1'
        #
        # st = start
        # for i in range(40):
        #     # print(st, st.count('1'), st.count('2'), st.count('3'))
        #     print('i={}, 1={}, 2={}, 3={}'.format(i, st.count('1'), st.count('2'), st.count('3')))
        #     st = self.get_next_str(st)

    @staticmethod
    def get_next_str(input_string):
        count = 0
        new_st = ''
        for i, char in enumerate(input_string):
            count += 1
            if i == len(input_string) - 1:
                new_st += '{}{}'.format(count, char)
                break
            if char == input_string[i+1]:
                continue
            else:
                new_st += '{}{}'.format(count, char)
                count = 0
        return new_st


class Solution419(unittest.TestCase):
    def setUp(self):
        self.problem = Problem419(mod=2**30)

    def test_small_solution(self):
        # 40 => 31254,20259,11625
        self.assertEqual('31254,20259,11625', self.problem.solve(n=40))

    def test_solution(self):
        # 1000000000000 => 998567458,1046245404,43363922
        self.assertEqual('998567458,1046245404,43363922', self.problem.solve(n=10**12))


if __name__ == '__main__':
    unittest.main()
