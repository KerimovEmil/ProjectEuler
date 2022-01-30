# Project Euler Problem 185

# 90342 ;2 correct
# 70794 ;0 correct
# 39458 ;2 correct
# 34109 ;1 correct
# 51545 ;2 correct
# 12531 ;1 correct

# ans = 39542

from time import time
import itertools as it

start = time()

"""
known_correct: array indexed by [pos] giving the value 0 to 9 of the digit at
    position 'pos', or None if that position is undetermined.
known_incorrect: array indexed by [pos][digit], giving a boolean that says
    whether position 'pos' in the answer is not 'digit'.
"""


def nCr(n, r):
    assert n >= 0
    assert 0 <= r <= n, f"{r} {n}"
    r = min(r, n-r)
    result = 1
    for num, den in zip(range(n, n-r, -1), range(1, r+1)):
        result = (result * num) // den
    return result


def solve(guesses):
    def recurse(depth):
        if depth == num_guesses:
            show_solutions()
            return
        idx, undetermined, num_to_choose = pick_guess(depth)
        if undetermined is None:
            return  # at least one remaining guess is unattainable
        used[idx] = True
        guess = guesses[idx][1]
        for perm in it.combinations(undetermined, num_to_choose):
            remaining = undetermined - set(perm)
            for pos in perm: known_correct[pos] = guess[pos]
            for pos in remaining: known_incorrect[pos][guess[pos]] = True
            recurse(depth+1)
            for pos in perm: known_correct[pos] = None
            for pos in remaining: known_incorrect[pos][guess[pos]] = False
        used[idx] = False

    def pick_guess(depth):
        best, best_choices, best_undetermined, best_num_to_choose = None, None, None, None
        for idx, already_used in enumerate(used):
            if already_used: continue
            correct, guess = guesses[idx]
            num_correct, num_incorrect = 0, 0
            undetermined = set()
            for pos, digit in enumerate(guess):
                if known_correct[pos] is not None:
                    if known_correct[pos] == digit:
                        num_correct += 1
                    else:
                        num_incorrect += 1
                elif known_incorrect[pos][digit]:
                    num_incorrect += 1
                else:
                    undetermined.add(pos)
            num_to_choose = correct - num_correct
            if num_correct > correct:
                return None, None, None   # too many are correct, no solutions
            if len(undetermined) < num_to_choose:
                return None, None, None   # too many are incorrect, no solutions
            choices = nCr(len(undetermined), num_to_choose)
            if best is None or choices < best_choices:
                best, best_choices, best_undetermined, best_num_to_choose = idx, choices, undetermined, num_to_choose
        return best, best_undetermined, best_num_to_choose

    def show_solutions():
        for sol in it.product(*[[i for i in range(10)
                                    if known_correct[pos] == i or
                                       (known_correct[pos] is None and not known_incorrect[pos][i])]
                                for pos in range(digits)]):
            print(''.join(str(d) for d in sol), "\t", time()-start)

    guesses.sort()
    for i, (correct, guess) in enumerate(guesses):
        guesses[i] = (correct, tuple(int(digit) for digit in guess))
    digits = len(guesses[0][1])
    assert all(len(guesses[i][1]) == digits for i in range(len(guesses))), "Guesses aren't all the same length!"
    known_correct = [None] * digits
    known_incorrect = [[False] * 10 for _ in range(digits)]
    while guesses and guesses[0][0] == 0:
        _, guess = guesses.pop(0)
        for pos, digit in enumerate(guess):
            known_incorrect[pos][digit] = True
    num_guesses = len(guesses)
    used = [False] * num_guesses
    recurse(0)


def p185():
    guesses = [ (2, '5616185650518293'),
                (1, '3847439647293047'),
                (3, '5855462940810587'),
                (3, '9742855507068353'),
                (3, '4296849643607543'),
                (1, '3174248439465858'),
                (2, '4513559094146117'),
                (3, '7890971548908067'),
                (1, '8157356344118483'),
                (2, '2615250744386899'),
                (3, '8690095851526254'),
                (1, '6375711915077050'),
                (1, '6913859173121360'),
                (2, '6442889055042768'),
                (0, '2321386104303845'),
                (2, '2326509471271448'),
                (2, '5251583379644322'),
                (3, '1748270476758276'),
                (1, '4895722652190306'),
                (3, '3041631117224635'),
                (3, '1841236454324589'),
                (2, '2659862637316867') ]
    solve(guesses)


def p185_example():
    guesses = [ (2, '90342'),
                (0, '70794'),
                (2, '39458'),
                (1, '34109'),
                (2, '51545'),
                (1, '12531') ]
    solve(guesses)


class Problem185:
    def __init__(self, ls_attempts):
        self.ls_attempts = ls_attempts

    def solve(self):
        return p185()


def main1():
    test_list = [90342, 70794, 39458, 34109, 51545, 12531]
    test_list = [str(x) for x in test_list]
    correct_list = [2, 0, 2, 1, 2, 1]
    ls_attempts = list(zip(test_list, correct_list))
    a = Problem185(ls_attempts)
    sol = a.solve()
    print(sol)


def main2():
    ls_attempts = [
        (5616185650518293, 2),
        (3847439647293047, 1),
        (5855462940810587, 3),
        (9742855507068353, 3),
        (4296849643607543, 3),
        (3174248439465858, 1),
        (4513559094146117, 2),
        (7890971548908067, 3),
        (8157356344118483, 1),
        (2615250744386899, 2),
        (8690095851526254, 3),
        (6375711915077050, 1),
        (6913859173121360, 1),
        (6442889055042768, 2),
        (2321386104303845, 0),
        (2326509471271448, 2),
        (5251583379644322, 2),
        (1748270476758276, 3),
        (4895722652190306, 1),
        (3041631117224635, 3),
        (1841236454324589, 3),
        (2659862637316867, 2)
    ]

    ls_attempts = [(str(x), y) for (x, y) in ls_attempts]
    a = Problem185(ls_attempts)
    sol = a.solve()
    print(sol)


if __name__ == "__main__":
    # main1()
    main2()

