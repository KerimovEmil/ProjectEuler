import unittest
from importlib import import_module

solved_quick_problems = [1, 2, 3, 4, 5, 6, 10, 16, 18, 30, 90, 116, 486, 753]

for prob in solved_quick_problems:
    _mod = import_module(f'solutions.PE{prob}')
    globals()[f'Solution{prob}'] = getattr(_mod, f'Solution{prob}')


if __name__ == '__main__':
    unittest.main()
