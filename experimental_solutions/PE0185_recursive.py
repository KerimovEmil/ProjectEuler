"""
EXPERIMENTAL / ALTERNATIVE SOLUTION

Project Euler Problem 185: Number Mind
Variant: Recursive Backtracking with Constraint Propagation & Heuristic Sorting

Description:
  Attempts to solve the 16-digit Number Mind puzzle via recursive depth-first search
  over digit assignments, filtering candidates using zero-match constraints and
  sorting branch exploration by heuristic probability scores.

Status:
  Works on the 5-digit sample game. For the full 16-digit game, this depth-first
  heuristic search encounters search space explosion without exact exact-cover (DLX)
  or SAT solving, making simulated annealing (PE0185.py) the preferred primary solver.
"""

from typing import List, Tuple, Union, Optional


def probability_sort(possible_digits: List[int], attempts: List[Tuple[str, int]]) -> List[int]:
    """Sorts candidate digits by estimated likelihood based on remaining correct counts."""
    num_digits = len(attempts[0][0])
    prob_scores = {d: 0.0 for d in possible_digits}

    for guess, correct_count in attempts:
        leading_digit = int(guess[0])
        prob = correct_count / num_digits
        if leading_digit in prob_scores:
            prob_scores[leading_digit] += prob

    return sorted(possible_digits, key=lambda d: prob_scores[d], reverse=True)


def test_solution_can_work(candidate: str, guess: str, correct_count: int) -> bool:
    """Checks if candidate string matches guess in exactly correct_count positions."""
    return sum(x == y for x, y in zip(candidate, guess)) == correct_count


def consistency_check(attempts: List[Tuple[str, int]], num_digits: int) -> bool:
    """Validates whether current branch of attempts has not violated constraints."""
    if any(correct_count > num_digits for _, correct_count in attempts):
        return False

    # Check against zero-match guesses
    zero_guesses = [guess for guess, correct_count in attempts if correct_count == 0]
    for guess, correct_count in attempts:
        max_possible = num_digits
        for pos in range(num_digits):
            forbidden = {g[pos] for g in zero_guesses}
            if guess[pos] in forbidden:
                max_possible -= 1
        if max_possible < correct_count:
            return False

    # Check exact-match constraints
    exact_matches = [guess for guess, count in attempts if count == num_digits]
    if len(set(exact_matches)) > 1:
        return False

    if len(exact_matches) == 1:
        candidate = exact_matches[0]
        for guess, count in attempts:
            if not test_solution_can_work(candidate, guess, count):
                return False

    return True


def recursive_search(attempts: List[Tuple[str, int]]) -> Optional[str]:
    """Recursive backtracking search for the secret digit sequence."""
    num_digits = len(attempts[0][0])

    if not consistency_check(attempts, num_digits=num_digits):
        return None

    # Check if any attempt already has all remaining digits correct
    for guess, correct_count in attempts:
        if correct_count == num_digits:
            return guess

    # Identify candidate leading digits
    possible_digits = list(range(10))
    for guess, correct_count in attempts:
        leading_digit = int(guess[0])
        if correct_count == 0 and leading_digit in possible_digits:
            possible_digits.remove(leading_digit)

    new_guesses = [guess[1:] for guess, _ in attempts]
    sorted_digits = probability_sort(possible_digits, attempts)

    for digit in sorted_digits:
        new_correct_counts = [
            count - 1 if guess[0] == str(digit) else count
            for guess, count in attempts
        ]
        next_attempts = list(zip(new_guesses, new_correct_counts))
        suffix = recursive_search(next_attempts)
        if suffix is not None:
            return str(digit) + suffix

    return None


class Problem185Recursive:
    def __init__(self, attempts: List[Tuple[Union[int, str], int]]):
        self.attempts = [(str(guess), count) for guess, count in attempts]

    def solve(self) -> Optional[str]:
        return recursive_search(self.attempts)


if __name__ == "__main__":
    sample_attempts = [
        (90342, 2),
        (70794, 0),
        (39458, 2),
        (34109, 1),
        (51545, 2),
        (12531, 1),
    ]
    solver = Problem185Recursive(sample_attempts)
    print("Sample 5-digit solution:", solver.solve())
