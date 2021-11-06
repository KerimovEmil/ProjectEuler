import unittest
from importlib import import_module

solved_quick_problems = [1, 2, 3, 4, 5, 6, 10, 16, 18, 30, 90, 116, 486, 753]


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for prob in solved_quick_problems:
        _mod = import_module(f'solutions.PE{prob}')
        test_suite.addTests(loader.loadTestsFromModule(_mod))
    return test_suite


if __name__ == '__main__':
    mySuite = suite()

    runner = unittest.TextTestRunner()
    runner.run(mySuite)
