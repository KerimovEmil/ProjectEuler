"""
EXPERIMENTAL / ALTERNATIVE SOLUTION

Project Euler Problem 185: Number Mind
Variant: Randomized Local Search / Stochastic Hill Climbing

Description:
  Solves the 16-digit Number Mind game by defining an objective distance function
  (sum of absolute errors between guess overlap and actual correct count across all clues)
  and using randomized single-digit mutations with restarts to find the global minimum (distance = 0).

Answer: 4640261571849533
"""

import random
from typing import List, Tuple, Union


def solution_distance(candidate: str, guess: str, correct: int) -> int:
    """Calculates absolute error between actual matches and target correct count."""
    return abs(sum(x == y for x, y in zip(candidate, guess)) - correct)


def total_error(attempts: List[Tuple[str, int]], candidate: str) -> int:
    """Computes total constraint violation across all clues."""
    return sum(solution_distance(candidate, guess, count) for guess, count in attempts)


def mutate_at(guess: str, index: int) -> str:
    """Mutates a single character in the candidate string at the specified index."""
    chars = list(guess)
    chars[index] = str(random.randint(0, 9))
    return "".join(chars)


class Problem185SimulatedAnnealing:
    def __init__(self, attempts: List[Tuple[Union[int, str], int]], max_retries: int = 10):
        self.attempts = [(str(guess), count) for guess, count in attempts]
        self.max_retries = max_retries
        self.digits = len(self.attempts[0][0])

    def solve_attempt(self) -> Tuple[str, int]:
        best_guess = "".join(str(random.randint(0, 9)) for _ in range(self.digits))
        min_dist = total_error(self.attempts, best_guess)
        if min_dist == 0:
            return best_guess, min_dist

        retries_remaining = self.max_retries
        while retries_remaining > 0:
            retries_remaining -= 1
            indices = list(range(self.digits))
            random.shuffle(indices)
            for idx in indices:
                mutated = mutate_at(best_guess, idx)
                dist = total_error(self.attempts, mutated)
                if dist < min_dist:
                    min_dist = dist
                    retries_remaining = self.max_retries
                    best_guess = mutated
                    if min_dist == 0:
                        return best_guess, min_dist

        return best_guess, min_dist

    def solve(self) -> str:
        while True:
            best_guess, dist = self.solve_attempt()
            if dist == 0:
                return best_guess


if __name__ == "__main__":
    clues_16 = [
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
        (2659862637316867, 2),
    ]
    solver = Problem185SimulatedAnnealing(clues_16)
    print("Found solution:", solver.solve())
