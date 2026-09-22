import unittest
from util.utils import (
    tonelli_shanks, legendre_symbol, coprime, is_palindrome, is_pandigital,
    mobius_sieve, is_prime_simple, continued_fraction_sqrt, pell_fundamental_solution,
    digits, digits_sum, number_base_rep, get_combination_mod_p
)


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

    def test_mobius_sieve(self):
        mu = mobius_sieve(30)
        expected = [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0, -1, 1, 1, 0, -1, 0, -1, 0, 1, 1, -1, 0, 0, 1, 0, 0, -1, -1]
        self.assertEqual(mu, expected)

    def test_is_prime_simple(self):
        primes_below_50 = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
        for n in range(-5, 50):
            self.assertEqual(is_prime_simple(n), n in primes_below_50, f"Failed for n={n}")
        # Large primes and composites
        self.assertTrue(is_prime_simple(1000000007))
        self.assertTrue(is_prime_simple(1000000009))
        self.assertFalse(is_prime_simple(1000000007 * 1000000009))
        self.assertTrue(is_prime_simple(2**31 - 1))  # Mersenne prime M31


    def test_continued_fraction_sqrt(self):
        self.assertEqual(continued_fraction_sqrt(4), (2, []))
        self.assertEqual(continued_fraction_sqrt(2), (1, [2]))
        self.assertEqual(continued_fraction_sqrt(3), (1, [1, 2]))
        self.assertEqual(continued_fraction_sqrt(7), (2, [1, 1, 1, 4]))
        self.assertEqual(continued_fraction_sqrt(13), (3, [1, 1, 1, 1, 6]))

    def test_pell_fundamental_solution(self):
        self.assertIsNone(pell_fundamental_solution(4))
        self.assertEqual(pell_fundamental_solution(2), (3, 2))
        self.assertEqual(pell_fundamental_solution(3), (2, 1))
        self.assertEqual(pell_fundamental_solution(5), (9, 4))
        self.assertEqual(pell_fundamental_solution(7), (8, 3))
        self.assertEqual(pell_fundamental_solution(13), (649, 180))

    def test_digits(self):
        self.assertEqual(digits(12345), [1, 2, 3, 4, 5])
        self.assertEqual(digits(0), [0])
        self.assertEqual(digits(-987), [9, 8, 7])

    def test_digits_sum(self):
        self.assertEqual(digits_sum(12345), 15)
        self.assertEqual(digits_sum(0), 0)
        self.assertEqual(digits_sum(-987), 24)

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

    def test_number_base_rep(self):
        self.assertEqual(number_base_rep(0, 10), [0])
        self.assertEqual(number_base_rep(13, 2), [1, 0, 1, 1])
        self.assertEqual(number_base_rep(100, 7), [2, 0, 2])
        self.assertEqual(number_base_rep(27, 3), [0, 0, 0, 1])

    def test_get_combination_mod_p(self):
        self.assertEqual(get_combination_mod_p(10, 3, 7), 1)
        self.assertEqual(get_combination_mod_p(100, 45, 13), 2)
        self.assertEqual(get_combination_mod_p(5, 6, 7), 0)
        self.assertEqual(get_combination_mod_p(5, 0, 7), 1)
        self.assertEqual(get_combination_mod_p(5, 5, 7), 1)
        self.assertEqual(get_combination_mod_p(10**18, 10**9, 1009), 0)
        self.assertEqual(get_combination_mod_p(10**18, 10**9, 1103), 185)


if __name__ == '__main__':
    unittest.main()


