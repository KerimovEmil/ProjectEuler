import unittest
from importlib import import_module

solved_quick_problems = [
    1, 2, 3, 4, 5, 6, 10, 16, 18, 30, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49, 50, 51, 53, 54, 55,
    56, 57, 60, 61, 62, 63, 65, 66, 67, 69, 72, 73, 76, 81, 82, 89, 90, 92, 97, 99, 101, 108, 110, 111, 116, 120, 124,
    125, 137, 139, 140, 144, 145, 187, 193, 197, 204, 229, 233, 235, 236, 243, 356, 357, 486, 610, 668, 700, 753]

# todo make this the list to maintain eventually
bad_or_slow_solutions = [46, 96, 179, 185, 211, 266, 330, 345, 401, 419, 420, 432]

for prob in solved_quick_problems:
    _mod = import_module(f'solutions.PE{prob}')
    globals()[f'Solution{prob}'] = getattr(_mod, f'Solution{prob}')


if __name__ == '__main__':
    unittest.main()
