# Project Euler Problem 185

# 90342 ;2 correct
# 70794 ;0 correct
# 39458 ;2 correct
# 34109 ;1 correct
# 51545 ;2 correct
# 12531 ;1 correct

# ans = 39542


# IDEA:
# keep track of which digits cannot be first digit. by 0's
# Try digit with least number of corrects.
# rescursive call


def test_solution_can_work(pos_sol, guess, correct):
    return sum([x == y for (x, y) in zip(pos_sol, guess)]) == correct


# [('42', 1), ('94', 0), ('58', 2), ('09', 1), ('45', 1), ('31', 1)]


def consistency_check(ls_attempts, digits):
    """For 1 digit choices, checks the consistency"""
    # If two corrects, then False
    if len([x for x in ls_attempts if x[1] > digits]) > 0:
        return False

    n_digit_correct = [x for x in ls_attempts if x[1] == digits]
    # If none are correct, ensure not all numbers have been checked
    if len(n_digit_correct) == 0:
        if len(set([x[0] for x in ls_attempts])) == 10:
            return False

    ls_correct_n_digit = [x[0] for x in n_digit_correct]
    # If more than 1 has n correct, and not the same, return false
    if len(set(ls_correct_n_digit)) > 1:
        return False

    # If only 1 has n(=2) correct, ensure that the other ones are consistent
    if len(set(ls_correct_n_digit)) == 1:
        possible_sol = ls_correct_n_digit[0]
        for attempt in ls_attempts:
            guess = attempt[0]
            num_corr = attempt[1]
            consistent_bool = test_solution_can_work(possible_sol, guess, num_corr)
            if consistent_bool is False:
                return False
    return True


def recursive_search(ls_attempts):
    digits = len(str(ls_attempts[0][0]))

    consistent = consistency_check(ls_attempts, digits=digits)
    if consistent is False:
        return False

    # Check for correct sequence
    # if number or correct matches length of guess, returns string of guess
    for attempt in ls_attempts:
        if digits == attempt[1]:
            return attempt[0]
    # if more
    ls_possible = set(range(10))

    # Remove the possible from the 0 correct guesses
    for attempt in ls_attempts:
        if attempt[1] == 0:
            ls_possible = ls_possible - {int(attempt[0][0])}
    # Create new game with one less digit
    # print(ls_possible)
    new_guesses = [attempt[0][1:] for attempt in ls_attempts]
    for possible_first_digit in ls_possible:  # loop over possible digits
        ls_new_correct = []
        # Change the number of correct in each guess, based on the guess
        for attempt in ls_attempts:
            if attempt[0][0] == str(possible_first_digit):
                new_correct_counter = attempt[1] - 1
            else:
                new_correct_counter = attempt[1]
            ls_new_correct.append(new_correct_counter)

        ls_new_attempts = list(zip(new_guesses, ls_new_correct))
        # Call new problem
        print("attempts: ", ls_attempts)
        print("Guess: ", possible_first_digit)
        print("New Attempts: ", ls_new_attempts)
        solution = recursive_search(ls_new_attempts)
        if solution is not False:
            print(solution)
            return str(possible_first_digit) + solution

    return False


class Problem185:
    def __init__(self, ls_attempts):
        self.ls_attempts = ls_attempts

    def solve(self):
        return recursive_search(self.ls_attempts)


if __name__ == "__main__":
    # test_list = [90342, 70794, 39458, 34109, 51545, 12531]
    # test_list = [str(x) for x in test_list]
    # correct_list = [2, 0, 2, 1, 2, 1]
    # ls_attempts = list(zip(test_list, correct_list))
    # a = Problem185(ls_attempts)
    # sol = a.solve()
    # print(sol)

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
