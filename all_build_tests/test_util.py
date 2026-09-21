import unittest
from util.utils import tonelli_shanks, legendre_symbol, coprime, is_palindrome, is_pandigital


class UtilTestCase(unittest.TestCase):
    def test_legendre_symbol(self):
        self.assertEqual(legendre_symbol(0, 7), 0)
        self.assertEqual(legendre_symbol(1, 7), 1)
        self.assertEqual(legendre_symbol(2, 7), 1)  # 3^2 = 9 = 2 mod 7
        self.assertEqual(legendre_symbol(3, 7), -1)
        self.assertEqual(legendre_symbol(4, 7), 1)  # 2^2 = 4 mod 7
        self.assertEqual(legendre_symbol(5, 7), -1)
        self.assertEqual(legendre_symbol(6, 7), -1)
        self.assertEqual(legendre_symbol(7, 7), 0)

    def test_tonelli_shanks(self):
        # Edge cases
        self.assertEqual(tonelli_shanks(0, 13), 0)
        self.assertEqual(tonelli_shanks(1, 13), 1)
        self.assertEqual(tonelli_shanks(4, 2), 0)

        # Non-residue
        self.assertIsNone(tonelli_shanks(2, 29))
        self.assertIsNone(tonelli_shanks(3, 7))

        # Test various prime forms: p = 3 mod 4, p = 5 mod 8, p = 1 mod 8
        test_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 73, 97, 1009]
        for p in test_primes:
            for x in range(p):
                n = (x * x) % p
                r = tonelli_shanks(n, p)
                self.assertIsNotNone(r, f"Expected modular square root for {n} mod {p}")
                self.assertEqual((r * r) % p, n, f"Root {r}^2 mod {p} does not equal {n}")

    def test_coprime(self):
        self.assertTrue(coprime(14, 15))
        self.assertFalse(coprime(14, 21))
        self.assertTrue(coprime(1, 100))

    def test_palindrome(self):
        self.assertTrue(is_palindrome(12321))
        self.assertTrue(is_palindrome(7))
        self.assertFalse(is_palindrome(1234))

    def test_pandigital(self):
        self.assertTrue(is_pandigital(123456789))
        self.assertTrue(is_pandigital(15243))
        self.assertFalse(is_pandigital(10234))
        self.assertFalse(is_pandigital(11234))


if __name__ == '__main__':
    unittest.main()
