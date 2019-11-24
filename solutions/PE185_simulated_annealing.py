# Project Euler Problem 185

# 90342 ;2 correct
# 70794 ;0 correct
# 39458 ;2 correct
# 34109 ;1 correct
# 51545 ;2 correct
# 12531 ;1 correct

# ans = 39542

# ANSWER
# 4640261571849533
import random


def solution_distance(pos_sol, guess, correct):
    return abs(sum([x == y for (x, y) in zip(pos_sol, guess)]) - correct)


def check_all_guesses(ls_attempts, possible_sol):
    dist = 0
    for attempt in ls_attempts:
        guess = attempt[0]
        num_corr = attempt[1]
        dist += solution_distance(possible_sol, guess, num_corr)
    return dist


def mutate_guess(old_guess):
    rand_index = random.randint(0, len(old_guess) - 1)
    return mutate_guess_i(old_guess, rand_index)


def mutate_guess_i(old_guess, i):
    """randomly mutate single element in string"""
    ls_old_guess = list(old_guess)
    rand_value = str(random.randint(0, 9))
    ls_old_guess[i] = rand_value
    return ''.join(ls_old_guess)


class Problem185:
    def __init__(self, ls_attempts):
        self.ls_attempts = ls_attempts
        self.max_try_wo_improvement = 10
        self.digits = len(self.ls_attempts[0][0])

    def solve_attempt(self):
        best_guess = ''.join([str(random.randint(0, 9)) for _ in range(self.digits)])
        min_dist = check_all_guesses(self.ls_attempts, best_guess)
        if min_dist == 0:
            return best_guess, min_dist
        w = self.max_try_wo_improvement
        # print("Trying new seed")
        while w > 0:
            w -= 1
            indexes = list(range(self.digits))
            random.shuffle(indexes)
            for i in indexes:
                possible_sol = mutate_guess_i(best_guess, i)
                dist = check_all_guesses(self.ls_attempts, possible_sol)
                if dist < min_dist:
                    min_dist = dist
                    w = self.max_try_wo_improvement
                    best_guess = possible_sol
                    # print(best_guess, dist)
                    if min_dist == 0:
                        return best_guess, min_dist

        return best_guess, min_dist

    def solve(self):
        min_dist = self.digits*len(self.ls_attempts)
        is_solved = False
        while is_solved is False:
            best_guess, dist = self.solve_attempt()
            if dist < min_dist:
                min_dist = dist
                print(min_dist, best_guess)
            if dist == 0:
                return best_guess


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

