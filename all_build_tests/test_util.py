import unittest
from util.utils import all_possible_factorizations, factorize
from math import prod


class MyTestCase(unittest.TestCase):
    def test_all_possible_factorization(self):
        with self.subTest('120'):
            for f in list(all_possible_factorizations({2: 3, 3: 1, 5: 1})):
                print(f'120={f}')
                self.assertEqual(prod(f), 2*2*2*3*5)

        with self.subTest('600'):
            for f in list(all_possible_factorizations({2: 3, 3: 1, 5: 2})):
                print(f'600={f}')
                self.assertEqual(prod(f), 2*2*2*3*5*5)

        with self.subTest('4800'):
            for f in list(all_possible_factorizations({2: 6, 3: 1, 5: 2})):
                print(f'4800={f}')
                self.assertEqual(prod(f), 2*2*2*2*2*2*3*5*5)

        with self.subTest('8'):
            self.assertEqual(all_possible_factorizations({2: 3}), {(2, 4), (8,), (2, 2, 2)})

    def test_factorize(self):
        self.assertEqual(factorize(12, {2, 3, 5}, {}), {(2, 2, 3), (12,), (2, 6), (3, 4)})


if __name__ == '__main__':
    unittest.main()
