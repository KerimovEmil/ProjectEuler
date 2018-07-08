# PE 356

# ANSWER
# 28010159


terms = 30
exp = 987654321  # 987654321 = 3*3*17*17*379721
modN = int(1e8)


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


class Matrix():
    def __init__(self, entries):
        self.entries = entries

    def __mul__(self, other):
        result = [[0 for j in range(len(other.entries[0]))] for i in range(len(self.entries))]
        for i in range(len(self.entries)):
            for j in range(len(other.entries[0])):
                for k in range(len(other.entries)):
                    result[i][j] += self.entries[i][k] * other.entries[k][j]
        return Matrix(result)

    def __mod__(self, mod):
        if mod:
            for i in range(len(self.entries)):
                for j in range(len(self.entries[0])):
                    self.entries[i][j] %= mod
        return self

    def __pow__(self, n, mod=None):
        assert (n > 0)
        if n == 1:
            return self.__mod__(mod)
        half = self.__pow__(n >> 1, mod)
        if n & 1 == 1:  # if odd
            return half.__mul__(half).__mul__(self).__mod__(mod)
        else:  # if even
            return half.__mul__(half).__mod__(mod)

    def __str__(self):
        return str(self.entries)


class LinearHomogeneousRecurrence():
    """
    Solve f(n+1) = c(n) f(n) + c(n-1) f(n-1) + ... + c(n-k) f(n-k) with
    f(0) = a(0), f(1) = a(1), ..., f(k) = a(k).
    
    Input:
        coefficients = [c(n), c(n-1), ..., c(n-k)]
        initial_values = [a(k), a(k-1), ..., a(0)]
    """

    def __init__(self, coefficients, initial_values):
        assert (len(coefficients) == len(initial_values))
        self.dim = len(coefficients)
        self.companion_matrix = self.__init__companion_matrix(coefficients)
        self.initial_state = self.__init__initial_state(initial_values)

    def __init__companion_matrix(self, coefficients):
        entries = [[0 for j in range(self.dim)] for i in range(self.dim)]
        for i in range(self.dim):
            entries[0][i] = coefficients[i]
        for i in range(1, self.dim):
            entries[i][i - 1] = 1
        return Matrix(entries)

    def __init__initial_state(self, initial_values):
        entries = [[value] for value in initial_values]
        return Matrix(entries)

    def get(self, n, mod=None):
        if n < self.dim:
            value = self.initial_state.entries[self.dim - n - 1][0]
            return value % mod if mod else value
        else:
            return ((pow(self.companion_matrix, n - self.dim + 1, mod) * self.initial_state) % mod).entries[0][0]


class Problem356():
    def solve(self):
        result = 0
        for i in range(1, terms + 1):
            result = (result + self.get(i, exp, modN)) % modN
        print(result)

    def get(self, n, power, mod):
        recurrence = LinearHomogeneousRecurrence([2 ** n, 0, -n], [4 ** n, 2 ** n, 3])
        return recurrence.get(power, mod) - 1


def main():
    problem = Problem356()
    problem.solve()


if __name__ == '__main__':
    main()
