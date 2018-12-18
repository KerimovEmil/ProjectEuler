import os
import argparse
import sys

TEMPLATE = """from util.utils import timeit
import unittest

class Problem{0}:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        raise NotImplementedError('Please implement this method!')

class Solution{0}(unittest.TestCase):
    def setUp(self):
        self.problem = Problem{0}()

    def test_solution(self):
        # Fill this in once you've got a working solution!
        self.assertEqual(1, self.problem.solve())

if __name__ == '__main__':
    unittest.main()
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='What problem are you trying to solve?')
    parser.add_argument(
        'p',
        action='store',
        type=int,
        help="The integer representing the problem that you're trying to solve!")
    args = parser.parse_args()
    fn = f'PE{args.p}.py'
    if os.path.exists(f'./{fn}'):
        raise AssertionError(
            f'{fn} already exists! Just update the file you lazy bastard!')
    with open(fn, 'w') as f:
        f.write(TEMPLATE.format(args.p))

    sys.exit(0)
