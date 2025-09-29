import unittest
from importlib import import_module
from os import listdir, path

bad_or_slow_solutions = [96, 179, 185, 211, 221, 266, 330, 365, 401, 419, 420, 432]

file_path = path.join(path.dirname(__file__), '..', 'solutions',)

for file in listdir(file_path):
    # ignore known files that don't follow convention
    if file in ['new_problem.py', '__init__.py', '__pycache__']:
        continue

    # get project euler problem number from file name
    problem_number = int(file.split('.')[0][2:])

    # don't run slow or bad solutions
    if problem_number in bad_or_slow_solutions:
        continue

    # else import the solution class
    _mod = import_module(f'solutions.PE{problem_number}')
    globals()[f'Solution{problem_number}'] = getattr(_mod, f'Solution{problem_number}')


if __name__ == '__main__':
    unittest.main()
