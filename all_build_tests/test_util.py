import unittest
from util.crt import ChineseRemainderTheorem, ChineseRemainderTheoremSets
from random import randint


class TestChineseRemainderTheorem(unittest.TestCase):
    def test_basic_primes(self):
        """(x==1 mod 3) & (x==1 mod 5) & (x==5 mod 7) -> (x==61 mod 3*5*7)"""
        obj = ChineseRemainderTheorem(a_list=[1, 1, 5], n_list=[3, 5, 7])
        self.assertEqual(61, obj.solve())

    def test_basic_sets(self):
        """(x=={1,2} mod 3) & (x=={1,3} mod 5) & (x=={5} mod 7) -> (x=={61,26,68,103} mod 3*5*7)"""
        s1 = {1, 2}
        s2 = {1, 3}
        s3 = {5}
        obj = ChineseRemainderTheoremSets(a_sets=[s1, s2, s3], n_list=[3, 5, 7])
        self.assertEqual({61, 26, 68, 103}, obj())

    def test_basic_non_coprime(self):
        """(x==1 mod 3*7) & (x==1 mod 5*7) -> (x==1 mod 3*5*7)"""
        obj = ChineseRemainderTheorem(a_list=[1, 1], n_list=[3*7, 5*7])
        self.assertEqual(1, obj.solve())

    def test_non_prime_sets(self):
        """Test random set equations"""
        m1 = 9*6
        m2 = 6 * 998 * 1997
        m3 = 6 * 2438 * 4877

        s1 = {randint(1, m1) for _ in range(10)}
        s2 = {randint(1, m2) for _ in range(10)}
        s3 = {randint(1, m3) for _ in range(10)}
        obj = ChineseRemainderTheoremSets([s1, s2, s3], n_list=[m1, m2, m3])
        sol_set = obj()

        for x in sol_set:
            self.assertTrue(x % m1 in s1)
            self.assertTrue(x % m2 in s2)
            self.assertTrue(x % m3 in s3)


if __name__ == '__main__':
    unittest.main()
