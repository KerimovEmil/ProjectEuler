from fractions import Fraction
from math import pi, factorial


def bernoulli(n: int) -> Fraction:
    """
    Returns the nth Bernoulli number
    https://en.wikipedia.org/wiki/Bernoulli_number
    """
    if n < 0:
        raise NotImplementedError
    if n == 0:
        return Fraction(1, 1)
    if n == 1:
        return Fraction(1, 2)
    if n % 2 == 1:  # odd number != 1
        return Fraction(0, 1)

    ls = [0] * (n + 1)
    for m in range(n + 1):
        ls[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            ls[j - 1] = j * (ls[j-1] - ls[j])
    return ls[0]  # B(n)


def zeta(n: int) -> float:
    """
    Returns the Riemann Zeta function value of n.
    """
    if n % 2 != 0:  # not even value
        raise NotImplementedError
    if n < 0:  # negative zeta
        raise NotImplementedError

    sign = (-1)**(n//2 + 1)
    two_pi = 2 * pi

    return sign * float(bernoulli(n)) * two_pi**n / (2 * factorial(n))
