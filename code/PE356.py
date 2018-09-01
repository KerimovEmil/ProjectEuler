# PE 356

# ANSWER
# 28010159

from util.utils import LinearHomogeneousRecurrence


# Note that every linear relation has a corresponding generating function
# u_(n+3) = 2^n * u_(n+2) - n * u_(n)
# this corresponds with g_n(x) = x^3 - 2^n x^2 + n 
# The roots of the cubic are the solutions to u_n = k_1 * a_1^n + k_2 * a_2^n + k_3 * a_3^n

# Note that all the roots of g_n(x) add up to 2^n 
# proof:
# p*(x-a1)*(x-a2)*(x-a3) = p*(x^3 - (a1+a2+a3)*x^2 + (a1*a2+a2*a1+a3*a1)x - (a1*a2*a3))
# Note that all the sum of squared of all the roots of g_n(x) add up to 4^n 
# proof:
# we know: (a1+a2+a3) = 2^n and (a1*a2+a2*a1+a3*a1) = 0
# hence: (2^n)^2 = 4^n = (a1+a2+a3)^2 = a1^2 + a2^2 + a3^2 + 0


# ALSO NOTE: That since the other two roots are less than 1, we can look at the recusive 
# relation instead of floating point exponenations.

# And the following recurence relation: u_(n+3) = 2^n * u_(n+2) - n * u_(n) 
# u(0) = 3, u(1) = 2^n , u(2) = 4^n
# will have the functional solution of:
# u(n) = a1^n + a2^2 + a3^n
# Since a2 and a3 are less than 1, for large n, they will contribute almost nothing to the value
# therefore for large n, u(n) ~= a1^n 

# a1 falls under a bigger branch of numbers called Pisot numbers. Whose algebraic conjuguates are all
# less than 1 in magnitude


class Problem356:
    def __init__(self, terms, exp, modN):
        self.terms = terms
        self.exp = exp
        self.modN = modN

    def solve(self):
        result = 0
        for i in range(1, self.terms + 1):
            result = (result + self.get(i, self.exp, self.modN)) % self.modN
        print(result)

    def get(self, n, power, mod):
        recurrence = LinearHomogeneousRecurrence([2 ** n, 0, -n], [4 ** n, 2 ** n, 3])
        return recurrence.get(power, mod) - 1


def main():
    terms = 30
    exp = 987654321  # 987654321 = 3*3*17*17*379721
    modN = int(1e8)
    problem = Problem356(terms, exp, modN)
    problem.solve()


if __name__ == '__main__':
    main()
