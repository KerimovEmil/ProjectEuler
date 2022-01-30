import numpy as np
import time
from itertools import accumulate
from functools import lru_cache, reduce
from math import gcd
from typing import List, Union, Dict, Generator, Optional


class Hungarian:
    """
    Implementation of the Hungarian (Munkres) Algorithm using np.
    Usage:
        hungarian = Hungarian(cost_matrix)
        hungarian.calculate()
    or
        hungarian = Hungarian()
        hungarian.calculate(cost_matrix)
    Handle Profit matrix:
        hungarian = Hungarian(profit_matrix, is_profit_matrix=True)
    or
        cost_matrix = Hungarian.make_cost_matrix(profit_matrix)
    The matrix will be automatically padded if it is not square.
    For that numpy's resize function is used, which automatically adds 0's to any row/column that is added
    Get results and total potential after calculation:
        hungarian.get_results()
        hungarian.get_total_potential()

        Implementation of the Hungarian (Munkres) Algorithm using Python and NumPy
        References:
            http://www.ams.jhu.edu/~castello/362/Handouts/hungarian.pdf
            http://weber.ucsd.edu/~vcrawfor/hungar.pdf
            http://en.wikipedia.org/wiki/Hungarian_algorithm
            http://www.public.iastate.edu/~ddoty/HungarianAlgorithm.html
            http://www.clapper.org/software/python/munkres/

        # Module Information.
        __version__ = "1.1.1"
        __author__ = "Thom Dedecko"
        __url__ = "http://github.com/tdedecko/hungarian-algorithm"
        __copyright__ = "(c) 2010 Thom Dedecko"
        __license__ = "MIT License"
            """

    def __init__(self, input_matrix=None, is_profit_matrix=False):
        """
        input_matrix is a List of Lists.
        input_matrix is assumed to be a cost matrix unless is_profit_matrix is True.
        """
        if input_matrix is not None:
            # Save input
            my_matrix = np.array(input_matrix)
            self._input_matrix = np.array(input_matrix)
            self._maxColumn = my_matrix.shape[1]
            self._maxRow = my_matrix.shape[0]

            # Adds 0s if any columns/rows are added. Otherwise stays unaltered
            matrix_size = max(self._maxColumn, self._maxRow)
            my_matrix.resize(matrix_size, matrix_size)

            # Convert matrix to profit matrix if necessary
            if is_profit_matrix:
                my_matrix = self.make_cost_matrix(my_matrix)

            self._cost_matrix = my_matrix
            self._size = len(my_matrix)
            self._shape = my_matrix.shape

            # Results from algorithm.
            self._results = []
            self._totalPotential = 0
        else:
            self._cost_matrix = None

    def get_results(self):
        """Get results after calculation."""
        return self._results

    def get_total_potential(self):
        """Returns expected value after calculation."""
        return self._totalPotential

    def calculate(self, input_matrix=None, is_profit_matrix=False):
        """
        Implementation of the Hungarian (Munkres) Algorithm.
        input_matrix is a List of Lists.
        input_matrix is assumed to be a cost matrix unless is_profit_matrix is True.
        """
        # Handle invalid and new matrix inputs.
        if input_matrix is None and self._cost_matrix is None:
            raise TypeError("Invalid input")
        elif input_matrix is not None:
            self.__init__(input_matrix, is_profit_matrix)

        result_matrix = self._cost_matrix.copy()

        # Step 1: Subtract row mins from each row.
        for index, row in enumerate(result_matrix):
            result_matrix[index] -= row.min()

        # Step 2: Subtract column mins from each column.
        for index, column in enumerate(result_matrix.T):
            result_matrix[:, index] -= column.min()

        # Step 3: Use minimum number of lines to cover all zeros in the matrix.
        # If the total covered rows+columns is not equal to the matrix size then adjust matrix and repeat.
        total_covered = 0
        while total_covered < self._size:
            # Find minimum number of lines to cover all zeros in the matrix and find total covered rows and columns.
            cover_zeros = CoverZeros(result_matrix)
            covered_rows = cover_zeros.get_covered_rows()
            covered_columns = cover_zeros.get_covered_columns()
            total_covered = len(covered_rows) + len(covered_columns)

            # if the total covered rows+columns is not equal to the matrix size then adjust it by min uncovered num (m).
            if total_covered < self._size:
                result_matrix = self._adjust_matrix_by_min_uncovered_num(result_matrix, covered_rows, covered_columns)

        # Step 4: Starting with the top row, work your way downwards as you make assignments.
        # Find single zeros in rows or columns.
        # Add them to final result and remove them and their associated row/column from the matrix.
        expected_results = min(self._maxColumn, self._maxRow)
        zero_locations = (result_matrix == 0)
        while len(self._results) != expected_results:

            # If number of zeros in the matrix is zero before finding all the results then an error has occurred.
            if not zero_locations.any():
                raise TypeError("Unable to find results. Algorithm has failed.")

            # Find results and mark rows and columns for deletion
            matched_rows, matched_columns = self.__find_matches(zero_locations)

            # Make arbitrary selection
            total_matched = len(matched_rows) + len(matched_columns)
            if total_matched == 0:
                matched_rows, matched_columns = self.select_arbitrary_match(zero_locations)

            # Delete rows and columns
            for row in matched_rows:
                zero_locations[row] = False
            for column in matched_columns:
                zero_locations[:, column] = False

            # Save Results
            self.__set_results(zip(matched_rows, matched_columns))

        # Calculate total potential
        value = 0
        for row, column in self._results:
            value += self._input_matrix[row, column]
        self._totalPotential = value

    @staticmethod
    def make_cost_matrix(profit_matrix):
        """
        Converts a profit matrix into a cost matrix.
        Expects NumPy objects as input.
        """
        # subtract profit matrix from a matrix made of the max value of the profit matrix
        matrix_shape = profit_matrix.shape
        offset_matrix = np.ones(matrix_shape) * profit_matrix.max()
        cost_matrix = offset_matrix - profit_matrix
        return cost_matrix

    def _adjust_matrix_by_min_uncovered_num(self, result_matrix, covered_rows, covered_columns):
        """Subtract m from every uncovered number and add m to every element covered with two lines."""
        # Calculate minimum uncovered number (m)
        elements = []
        for row_index, row in enumerate(result_matrix):
            if row_index not in covered_rows:
                for index, element in enumerate(row):
                    if index not in covered_columns:
                        elements.append(element)
        min_uncovered_num = min(elements)

        # Add m to every covered element
        adjusted_matrix = result_matrix
        for row in covered_rows:
            adjusted_matrix[row] += min_uncovered_num
        for column in covered_columns:
            adjusted_matrix[:, column] += min_uncovered_num

        # Subtract m from every element
        m_matrix = np.ones(self._shape) * min_uncovered_num
        adjusted_matrix -= m_matrix

        return adjusted_matrix

    def __find_matches(self, zero_locations):
        """Returns rows and columns with matches in them."""
        marked_rows = np.array([], dtype=int)
        marked_columns = np.array([], dtype=int)

        # Mark rows and columns with matches
        # Iterate over rows
        for index, row in enumerate(zero_locations):
            row_index = np.array([index])
            if np.sum(row) == 1:
                column_index, = np.where(row)
                marked_rows, marked_columns = self.__mark_rows_and_columns(marked_rows, marked_columns, row_index,
                                                                           column_index)

        # Iterate over columns
        for index, column in enumerate(zero_locations.T):
            column_index = np.array([index])
            if np.sum(column) == 1:
                row_index, = np.where(column)
                marked_rows, marked_columns = self.__mark_rows_and_columns(marked_rows, marked_columns, row_index,
                                                                           column_index)

        return marked_rows, marked_columns

    @staticmethod
    def __mark_rows_and_columns(marked_rows, marked_columns, row_index, column_index):
        """Check if column or row is marked. If not marked then mark it."""
        new_marked_rows = marked_rows
        new_marked_columns = marked_columns
        if not (marked_rows == row_index).any() and not (marked_columns == column_index).any():
            new_marked_rows = np.insert(marked_rows, len(marked_rows), row_index)
            new_marked_columns = np.insert(marked_columns, len(marked_columns), column_index)
        return new_marked_rows, new_marked_columns

    @staticmethod
    def select_arbitrary_match(zero_locations):
        """Selects row column combination with minimum number of zeros in it."""
        # Count number of zeros in row and column combinations
        rows, columns = np.where(zero_locations)
        zero_count = []
        for index, row in enumerate(rows):
            total_zeros = np.sum(zero_locations[row]) + np.sum(zero_locations[:, columns[index]])
            zero_count.append(total_zeros)

        # Get the row column combination with the minimum number of zeros.
        indices = zero_count.index(min(zero_count))
        row = np.array([rows[indices]])
        column = np.array([columns[indices]])

        return row, column

    def __set_results(self, result_lists):
        """Set results during calculation."""
        # Check if results values are out of bound from input matrix (because of matrix being padded).
        # Add results to results list.
        for result in result_lists:
            row, column = result
            if row < self._maxRow and column < self._maxColumn:
                new_result = (int(row), int(column))
                self._results.append(new_result)


class CoverZeros:
    """
    Use minimum number of lines to cover all zeros in the matrix.
    Algorithm based on: http://weber.ucsd.edu/~vcrawfor/hungar.pdf
    """

    def __init__(self, matrix):
        """
        Input a matrix and save it as a boolean matrix to designate zero locations.
        Run calculation procedure to generate results.
        """
        # Find zeros in matrix
        self._zero_locations = (matrix == 0)
        self._shape = matrix.shape

        # Choices starts without any choices made.
        self._choices = np.zeros(self._shape, dtype=bool)

        self._marked_rows = []
        self._marked_columns = []

        # marks rows and columns
        self.__calculate()

        # Draw lines through all unmarked rows and all marked columns.
        self._covered_rows = list(set(range(self._shape[0])) - set(self._marked_rows))
        self._covered_columns = self._marked_columns

    def get_covered_rows(self):
        """Return list of covered rows."""
        return self._covered_rows

    def get_covered_columns(self):
        """Return list of covered columns."""
        return self._covered_columns

    def __calculate(self):
        """
        Calculates minimum number of lines necessary to cover all zeros in a matrix.
        Algorithm based on: http://weber.ucsd.edu/~vcrawfor/hungar.pdf
        """
        while True:
            # Erase all marks.
            self._marked_rows = []
            self._marked_columns = []

            # Mark all rows in which no choice has been made.
            for index, row in enumerate(self._choices):
                if not row.any():
                    self._marked_rows.append(index)

            # If no marked rows then finish.
            if not self._marked_rows:
                return True

            # Mark all columns not already marked which have zeros in marked rows.
            num_marked_columns = self.__mark_new_columns_with_zeros_in_marked_rows()

            # If no new marked columns then finish.
            if num_marked_columns == 0:
                return True

            # While there is some choice in every marked column.
            while self.__choice_in_all_marked_columns():
                # Some Choice in every marked column.

                # Mark all rows not already marked which have choices in marked columns.
                num_marked_rows = self.__mark_new_rows_with_choices_in_marked_columns()

                # If no new marks then Finish.
                if num_marked_rows == 0:
                    return True

                # Mark all columns not already marked which have zeros in marked rows.
                num_marked_columns = self.__mark_new_columns_with_zeros_in_marked_rows()

                # If no new marked columns then finish.
                if num_marked_columns == 0:
                    return True

            # No choice in one or more marked columns.
            # Find a marked column that does not have a choice.
            choice_column_index = self.__find_marked_column_without_choice()

            while choice_column_index is not None:
                # Find a zero in the column indexed that does not have a row with a choice.
                choice_row_index = self.__find_row_without_choice(choice_column_index)

                # Check if an available row was found.
                new_choice_column_index = None
                if choice_row_index is None:
                    # Find a good row to accomodate swap. Find its column pair.
                    choice_row_index, new_choice_column_index = \
                        self.__find_best_choice_row_and_new_column(choice_column_index)

                    # Delete old choice.
                    self._choices[choice_row_index, new_choice_column_index] = False

                # Set zero to choice.
                self._choices[choice_row_index, choice_column_index] = True

                # Loop again if choice is added to a row with a choice already in it.
                choice_column_index = new_choice_column_index

    def __mark_new_columns_with_zeros_in_marked_rows(self):
        """Mark all columns not already marked which have zeros in marked rows."""
        num_marked_columns = 0
        for index, column in enumerate(self._zero_locations.T):
            if index not in self._marked_columns:
                if column.any():
                    row_indices, = np.where(column)
                    zeros_in_marked_rows = (set(self._marked_rows) & set(row_indices)) != set([])
                    if zeros_in_marked_rows:
                        self._marked_columns.append(index)
                        num_marked_columns += 1
        return num_marked_columns

    def __mark_new_rows_with_choices_in_marked_columns(self):
        """Mark all rows not already marked which have choices in marked columns."""
        num_marked_rows = 0
        for index, row in enumerate(self._choices):
            if index not in self._marked_rows:
                if row.any():
                    column_index, = np.where(row)
                    if column_index in self._marked_columns:
                        self._marked_rows.append(index)
                        num_marked_rows += 1
        return num_marked_rows

    def __choice_in_all_marked_columns(self):
        """Return Boolean True if there is a choice in all marked columns. Returns boolean False otherwise."""
        for column_index in self._marked_columns:
            if not self._choices[:, column_index].any():
                return False
        return True

    def __find_marked_column_without_choice(self):
        """Find a marked column that does not have a choice."""
        for column_index in self._marked_columns:
            if not self._choices[:, column_index].any():
                return column_index

        raise TypeError(
            "Could not find a column without a choice. Failed to cover matrix zeros. Algorithm has failed.")

    def __find_row_without_choice(self, choice_column_index):
        """Find a row without a choice in it for the column indexed. If a row does not exist then return None."""
        row_indices, = np.where(self._zero_locations[:, choice_column_index])
        for row_index in row_indices:
            if not self._choices[row_index].any():
                return row_index

        # All rows have choices. Return None.
        return None

    def __find_best_choice_row_and_new_column(self, choice_column_index):
        """
        Find a row index to use for the choice so that the column that needs to be changed is optimal.
        Return a random row and column if unable to find an optimal selection.
        """
        row_indices, = np.where(self._zero_locations[:, choice_column_index])
        for row_index in row_indices:
            column_indices, = np.where(self._choices[row_index])
            column_index = column_indices[0]
            if self.__find_row_without_choice(column_index) is not None:
                return row_index, column_index

        # Cannot find optimal row and column. Return a random row and column.
        from random import shuffle

        shuffle(row_indices)
        column_index, = np.where(self._choices[row_indices[0]])
        return row_indices[0], column_index[0]


def basic_factorial(x):
    """Returns the factorial of the integer x."""
    ans = 1
    while x:
        ans *= x
        x -= 1
    return ans


class Matrix:
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


class LinearHomogeneousRecurrence:
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


class BaseConverter:
    def convert_decimal(self, n, base):
        reversed_rep = []
        d = n
        while d:
            d, r = divmod(d, base)
            reversed_rep.append(r)
        return reversed_rep[::-1]

    def convert_rep(self, rep, base):
        result = 0
        for digit in rep:
            result = result * base + digit
        return result


class BinomialCoefficient:
    def __init__(self, prime):
        self.prime = prime
        self.base_values = self.__init_base_values(prime)
        self.cache_values = {}
        self.base_converter = BaseConverter()

    def __init_base_values(self, prime):
        curr = [1]
        result = [curr]
        for n in range(2, prime + 1):
            next = [1]
            for k in range(1, n - 1):
                next.append(curr[k - 1] + curr[k])
            next.append(1)
            curr = next
            result.append(curr)
        return result

    def get(self, m, n):
        if m not in self.cache_values:
            self.cache_values[m] = {}
        if n not in self.cache_values[m]:
            m_rep = self.base_converter.convert_decimal(m, self.prime)
            n_rep = self.base_converter.convert_decimal(n, self.prime)
            offset = len(m_rep) - len(n_rep)
            result = 1
            for i in range(len(n_rep)):
                m_i = m_rep[offset + i]
                n_i = n_rep[i]
                if m_i < n_i:
                    return 0
                result = (result * self.base_values[m_i][n_i]) % self.prime
            self.cache_values[m][n] = result
        return self.cache_values[m][n]


class EulerNumber:
    def __init__(self, prime):
        self.prime = prime
        self.binomial_coefficient = BinomialCoefficient(prime)
        self.factorial_mod = self.__init_factorial_mod(prime)

        self.values = {0: (1, prime - 1)}

    def __init_factorial_mod(self, prime):
        result = [1]
        for i in range(1, prime):
            result.append((result[-1] * i) % prime)
        return result

    def get(self, n):
        if n not in self.values:
            a = self.__factorial_mod(n)
            b = -1
            for k in range(n):
                c = self.binomial_coefficient.get(n, k)
                a_k, b_k = self.get(k)
                a += c * a_k
                b += c * b_k
                b -= c * self.__factorial_mod(n - k)
            self.values[n] = (a % self.prime, b % self.prime)
        return self.values[n]

    def __factorial_mod(self, n):
        if n >= self.prime:
            return 0
        return self.factorial_mod[n]


class ChineseRemainderTheorem:
    """
    Solve x = a_i (mod n_i) where n_i are coprime.
    """

    def solve(self, a_list, n_list):
        a = a_list[0]
        m = n_list[0]
        for i in range(1, len(n_list)):
            n = n_list[i]
            b = a_list[i]
            q = m * n
            (x, y) = self.__extended_gcd(m, n)
            root = (a + (b - a) * x * m) % q
            a, m = root, q
        return a

    def __extended_gcd(self, a, b):
        (x, y) = (0, 1)
        (last_x, last_y) = (1, 0)
        while b != 0:
            (q, r) = divmod(a, b)
            (a, b) = (b, r)
            (x, last_x) = (last_x - q * x, x)
            (y, last_y) = (last_y - q * y, y)
        return (last_x, last_y)


def sieve(n):
    """Return all primes <= n."""
    np1 = n + 1
    s = list(range(np1))
    s[1] = 0
    sqrtn = int(round(n ** 0.5))
    for i in range(2, sqrtn + 1):
        if s[i]:
            s[i * i: np1: i] = [0] * len(range(i * i, np1, i))
    return filter(None, s)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('{} took: {:.3f} seconds'.format(method.__name__, (te - ts)))
        return result
    return timed


def is_pandigital(num):
    """Return true if integer num uses all of the digits from 1 to n exactly once. False otherwise."""
    str_num = str(num)
    if str_num.count('0') > 0:
        return False
    n_digits = len(str_num)
    for i in range(1, n_digits+1):
        if str_num.count(str(i)) != 1:
            return False
    return True


def new_mod(str_a, m):  # todo: test for bugs
    """
    Returns a mod m.
    Works well for m=0,1,2,3,4,5,8,9,10,11
    Args:
        str_a: <str>
        m: <num>
    Returns: a mod m
    """
    int_a = int(str_a)
    if len(str_a) > 2:

        if m == 0 or m == 1:
            return 0

        if int_a == m:
            return 0

        if m == 2:
            last = str_a[-1:]
            return new_mod(last, m)

        if m == 3 or m == 9:
            sum_of_digits = sum([int(d) for d in str_a])
            return new_mod(str(sum_of_digits), m)

        if m == 4:
            last = int(str_a[-1])
            second_last = int(str_a[-2:-1])
            answer = 2 * second_last + last
            return new_mod(str(answer), m)

        if m == 5:
            last = str_a[-1]
            return new_mod(last, m)

        if m == 7:
            last = int(str_a[-1:])
            first = int(str_a[:-1])
            answer = new_mod(str(first - 2 * last), m)
            if answer == 0:
                return 0
            else:
                return int_a % m

        if m == 8:
            last = int(str_a[-1:])
            second_last = int(str_a[-2:-1])
            third_last = int(str_a[-3:-2])
            answer = 4 * third_last + 2 * second_last + last
            return new_mod(str(answer), m)

        if m == 10:
            last = int(str_a[-1:])
            return last

        if m == 11:
            new_a = 0
            for i, digit in enumerate(str_a):
                if not i % 2:
                    new_a += int(digit)
                else:
                    new_a -= int(digit)
            return new_mod(str(new_a), m)

        if m == 13:
            last = int(str_a[-1:])
            first = int(str_a[:-1])
            answer = new_mod(str(first - 9 * last), m)
            if answer == 0:
                return 0
            else:
                return int_a % m

        return int_a % m

    else:

        return int_a % m


def combin(n, r):
    """A fast way to calculate binomial coefficients by Andrew Dalke (contrib)."""
    if 0 <= r <= n:
        ntok = 1
        rtok = 1
        for t in range(1, min(r, n - r) + 1):
            ntok *= n
            rtok *= t
            n -= 1
        return ntok // rtok  # bit-wise operation
    else:
        return 0


def square_free_sieve(limit):
    """Generator that yields all square free numbers less than limit"""
    a = [True] * limit
    # Needed so we don't mark off multiples of 1^2
    yield 1
    a[0] = a[1] = False
    for i, is_square_free in enumerate(a):
        if is_square_free:
            yield i
            i2 = i * i
            for n in range(i2, limit, i2):
                a[n] = False


def square_primes_sieve(limit, primes=None):
    """Returns a list all prime squares less than limit"""
    if primes is None:
        primes = sieve(int(limit))
    return [i**2 for i in primes]


def primes_of_n(n, ls_prime=None):
    """
    Given an integer n, return the prime factorization.

    Args:
        n: <int> integer
        ls_prime: <list> optional parameter to specify a list of possible primes

    Returns: <dict> of prime factors with the keys being the prime number, and the values
        being the multiplicity of that factor.

    """
    factors = {}

    if ls_prime is None:
        i = 2
        p = 2

        def next_prime(j):
            return j
    else:
        i = 0
        p = ls_prime[i]

        def next_prime(j):
            return ls_prime[j]

    while p * p <= n:
        while n % p == 0:
            if p not in factors:
                factors[p] = 0
            factors[p] += 1
            n //= p
        i += 1
        p = next_prime(i)

    if n > 1:
        factors[n] = 1
    return factors


def cumsum(ls):
    """
    Given a list, return the cumulative sum of the list
    Args:
        ls: list of numbers
    Returns: <list>
    """
    return list(accumulate(ls))


def generate_ascending_sub_sequence(options, num):
    """

    Args:
        options: <list> of objects, ordered in ascending order
        num: <int> the size of the sub-sequence to return

    Returns: an generator of sub-sequences of options in ascending order

    e.g.
     options = ['0', '1', '2']
     num = 3

     Returns:
     ('0', '0', '0')
     ('0', '0', '1')
     ('0', '0', '2')
     ('0', '1', '1')
     ('0', '1', '2')
     ('0', '2', '2')
     ('1', '1', '1')
     ('1', '1', '2')
     ('1', '2', '2')
     ('2', '2', '2')
    """
    if num == 1:
        for i in options:
            yield (i, )
    else:
        for idx, j in enumerate(options):
            for k in generate_ascending_sub_sequence(options[idx:], num - 1):
                yield (j, *k)


@lru_cache(maxsize=None, typed=False)
def partition_number(n):
    """
    Compute the partition number of n.
    Using recursive equation found here: http://www.cs.utsa.edu/~wagner/python/fp/part.html
    p(n) = sum_{k=1}^{n} (-1)^{k+1} (p(x) + p(y))
    x = n - k*(3k-1)/2
    y = n - k*(3k+1)/2
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    sign = 1
    summation = 0
    for k in range(1, n+1):
        x = n - int(k*(3*k-1)/2)
        y = n - int(k*(3*k+1)/2)
        summation += sign*(partition_number(x) + partition_number(y))
        sign *= -1
    return summation


def euler_totient_function(n):
    dc_factors = primes_of_n(n)
    iter_primes = ((1-1/p) for p in dc_factors.keys())
    output = n
    for p in iter_primes:
        output *= p
    return int(output)


def is_coprime(a, b):
    """Returns True if a and b are co-prime, False otherwise"""
    return gcd(a,b) == 1


@lru_cache(maxsize=None)
def sum_phi(n):
    """Returns sum_{i=1 to n} phi(i) where phi is the euler totient function"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    v = int(n**0.5)
    nv = n//(v+1)

    return n*(n+1)//2 - sum(sum_phi(x) * (n//x - n//(x+1)) for x in range(1, v+1)) - sum(sum_phi(n//k) for k in range(2, nv+1))


def farey(n, descending=False):
    """Print the n'th Farey sequence. Allow for either ascending or descending."""
    a, b, c, d = 0, 1, 1, n
    if descending:
        a, c = 1, n - 1
    ls_farey = [(a, b)]
    while (c <= n and not descending) or (a > 0 and descending):
        k = int((n + b) / d)
        a, b, c, d = c, d, k * c - a, k * d - b
        ls_farey.append((a, b))
    return ls_farey


@lru_cache(maxsize=None, typed=False)
def len_faray_seq(n):
    """
    Calculates the length of the n'th Faray Sequence.
    Args:
        n: <int>

    Returns: <int>

    Using the recursive relation |F_{n}| = |F_{n-1}| + euler_totient(n),
    Expanding for all n and then inverting the relation, after using |F_1| = 2 we get
    |F_{n}| = 1/2 * (n+3) * n  - sum_{d=2}^{n} |F_{floor(n/d)}|
    See Also: https://en.wikipedia.org/wiki/Farey_sequence
    """

    if n == 1:
        return 2
    elif n < 1:
        raise NotImplementedError("What happened??")
    else:

        return int(0.5*(n+3)*n) - sum(len_faray_seq(int(n/d)) for d in range(2, n+1))


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


@timeit
def mobius_sieve(n: int, ls_prime: Union[List[int], None]) -> List[int]:
    """
    Returns a list of all mobius function values.
    mobius(n) = 1 if i is square-free with even number of primes,
               -1 if odd number,
                0 if contains square
    """
    ls_m = [1]*n
    if ls_prime is None:
        ls_p = list(sieve(n))
    else:
        ls_p = ls_prime
    for p in ls_p:
        ls_m[p:n:p] = [-1 * x for x in ls_m[p:n:p]]
        p2 = p ** 2
        ls_m[p2:n:p2] = [0] * ((n-1)//p2)  # len(ls_m[p2:n:p2]) == (n-1)//p2
    return ls_m


# @lru_cache(maxsize=None)
def num_of_divisors(n):
    """
    Return the number of positive divisors of n.
    e.g. sigma(12) = 6
    """
    dc_primes = primes_of_n(n)
    return reduce(lambda a, b: a * b, (v + 1 for v in dc_primes.values()))


def divisors(prime_factors: Dict[int, int]) -> Generator[int, None, None]:
    """
    Given the prime factorization of a number, return a generator of all of it's divisors.
    Args:
        prime_factors: a dictionary with the key being the prime and the value being the multiplicity of the prime.
    For example if n=12 then then input would be {2:2, 3:1} since 12 = 2*2*3, and the generator would return
    1,2,4,3,6,12
    """
    ls_primes = list(prime_factors.keys())

    # generates factors from ls_primes[k:] subset
    def generate(k):
        if k == len(ls_primes):
            yield 1
        else:
            rest = generate(k + 1)
            prime = ls_primes[k]
            for factor in rest:
                prime_to_i = 1
                # prime_to_i iterates prime**i values, i being all possible exponents
                for _ in range(prime_factors[prime] + 1):
                    yield factor * prime_to_i
                    prime_to_i *= prime

    yield from generate(0)


@lru_cache(maxsize=None)
def binomial_recursive(n: int, k: int, mod_m: int) -> int:
    if k == 0:
        return 1
    if n == 0:
        return 0
    if n == k:
        return 1
    if k > (n-k):
        return binomial_recursive(n, n-k, mod_m)
    return (binomial_recursive(n-1, k, mod_m) + binomial_recursive(n-1, k-1, mod_m)) % mod_m


@lru_cache(maxsize=None)
def fib(n: int, mod_m: int = int(1e12)) -> int:
    if n < 2:
        return n
    return (fib(n-1, mod_m) + fib(n-2, mod_m)) % mod_m


def fibonacci_n_term(n: int) -> Union[int, NotImplementedError]:
    """Returns the nth fibonacci number"""
    if n < 0:
        return NotImplementedError('negative n is not implemented')
    sq_5 = 5**0.5
    phi_pos = (1 + sq_5) / 2
    return round(phi_pos**n / sq_5)


def fibonacci_k_n_term(n: int, k: int) -> Union[int, NotImplementedError]:
    """
    Returns the nth fibonacci_k number.
    Where F_{k,n+1} = k*F_{k,n} + F_{k,n−1} for n ≥ 1
    """
    if n < 0:
        return NotImplementedError('negative n is not implemented')
    if n in [0, 1]:
        return n

    root = (k+(k**2 + 4)**0.5) / 2
    return round((root**n - (-root)**(-n)) / (root + 1/root))


def catalan_transform(n: int = 1, seq: List[int] = None, mod_m: Optional[int] = None) -> int:
    """http://www.kurims.kyoto-u.ac.jp/EMIS/journals/JIS/VOL8/Barry/barry84.pdf"""
    if n == 0:
        return 0
    if mod_m is not None:
        return int(sum((i * combin(2*n-i, n-i) * seq[i] // (2*n-i)) % mod_m for i in range(1, n+1)))
    else:
        return int(sum(i * combin(2*n-i, n-i) * seq[i] // (2*n-i) for i in range(1, n+1)))


def inv_catalan_transform(n: int = 1, seq: List[int] = None) -> int:
    """http://www.kurims.kyoto-u.ac.jp/EMIS/journals/JIS/VOL8/Barry/barry84.pdf"""
    return sum(combin(i, n-i) * (-1)**(n-i) * seq[i] for i in range(n+1))


def get_all_mod_inverse_dict(m: int, max_n: int) -> Dict[int, int]:
    """
    Computes a^-1 mod m for all a in [1, a-1]
    https://cp-algorithms.com/algebra/module-inverse.html#mod-inv-all-num

    Taking the key * value mod m for each key value would result in 1
    """
    dc_inv = {1: 1}
    for i in range(2, max_n+1):
        dc_inv[i] = m - (m // i) * dc_inv[m % i] % m
    return dc_inv


def get_all_mod_inverse_list(m: int, max_n: int) -> List[int]:
    """
    Computes a^-1 mod m for all a in [1, a-1]
    https://cp-algorithms.com/algebra/module-inverse.html#mod-inv-all-num
    """
    ls_inv = [0, 1]
    for i in range(2, max_n+1):
        ls_inv.append(m - (m // i) * ls_inv[m % i] % m)
    return ls_inv


def cycle_length(k: int) -> int:
    """
    Computes the repeated cycle length of the decimal expansion of 1/k.
    e.g.
    1/6 = 0.1(6)  -> 1
    1/7 = 0.(142857) -> 6

    For k not equal to a multiple of 2 or 5,
    1/k has a cycle of d digits if 10^d == 1 mod k = 0
    """
    while k % 2 == 0:
        k //= 2  # remove factors of 2
    while k % 5 == 0:
        k //= 5  # remove factors of 5
    if k == 1:
        return 0  # this is not a repeating decimal
    d = 1
    x = 10 % k
    while x != 1:
        x = (x*10) % k
        d += 1
    return d
