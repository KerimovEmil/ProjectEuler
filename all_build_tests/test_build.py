import unittest
from importlib import import_module

solved_quick_problems = [1, 2, 3, 4, 5, 6, 10, 16, 18, 30, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49,
                         50, 51, 53, 54, 55, 56, 57, 60, 63, 65, 66, 67, 69, 72, 73, 76, 81, 82, 89, 90, 92, 97,
                         116, 144, 486, 753]
bad_or_slow_solutions = [46, 96]  # todo make this the final list to maintain eventually

for prob in solved_quick_problems:
    _mod = import_module(f'solutions.PE{prob}')
    globals()[f'Solution{prob}'] = getattr(_mod, f'Solution{prob}')


if __name__ == '__main__':
    unittest.main()
