import numpy as np
import time
from itertools import accumulate
from functools import lru_cache, reduce
import math
from math import gcd
from typing import List, Union, Dict, Generator, Optional, Tuple


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


def basic_falling_factorial(high, low):
    """Returns the high! / low! """
    if low == high:
        return 1
    if high < low:
        return 0
    i = low + 1
    ans = 1
    while i <= high:
        ans *= i
        i += 1
    return ans


def lcm(x, y):
    return x * y // gcd(x, y)


class Matrix:
    def __init__(self, entries):
        self.entries = entries

    def __mul__(self, other):
        result = [[0 for _ in range(len(other.entries[0]))] for _ in range(len(self.entries))]
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
        entries = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
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
    @staticmethod
    def convert_decimal(n, base):
        reversed_rep = []
        d = n
        while d:
            d, r = divmod(d, base)
            reversed_rep.append(r)
        return reversed_rep[::-1]

    @staticmethod
    def convert_rep(rep, base):
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

    @staticmethod
    def __init_base_values(prime):
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


def prime_sieve(n):
    n = int(n)
    sieve = np.ones(n+1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = False
    return sieve


def primes_upto(n):
    return np.nonzero(prime_sieve(n))[0]


def count_primes_upto(n):
    return np.count_nonzero(prime_sieve(n))  # just count True values


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('{} took: {:.3f} seconds'.format(method.__module__, (te - ts)))
        return result
    return timed


def is_pandigital(num):
    """Return true if integer num uses the digits from 1 to n exactly once. False otherwise."""
    str_num = str(num)
    if str_num.count('0') > 0:
        return False
    n_digits = len(str_num)
    for i in range(1, n_digits+1):
        if str_num.count(str(i)) != 1:
            return False
    return True


def is_palindrome(n: int) -> bool:
    ls = list(str(n))
    return ls == ls[::-1]


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


def number_base_rep(n: int, b: int) -> List[int]:
    """
    Returns the base-b representation of a non-negative integer n as a list of digits
    in little-endian order (least significant digit first).

    Args:
        n (int): Non-negative integer to convert (n >= 0).
        b (int): Base (b >= 2).

    Returns:
        List[int]: Digits [d_0, d_1, ..., d_k] such that n = sum_{i=0}^k d_i * b^i,
                   with 0 <= d_i < b and d_k > 0 (for n > 0). For n = 0, returns [0].

    Examples:
        >>> number_base_rep(13, 2)
        [1, 0, 1, 1]  # 13 = 1*1 + 0*2 + 1*4 + 1*8
        >>> number_base_rep(100, 7)
        [2, 0, 2]     # 100 = 2*1 + 0*7 + 2*49
        >>> number_base_rep(0, 10)
        [0]
    """
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits


def get_combination_mod_p(n: int, k: int, p: int) -> int:
    """
    Computes the binomial coefficient (n choose k) modulo a prime p using Lucas' Theorem.

    By Lucas' Theorem, if n and k are expanded in base p:
        n = sum_{i=0}^m n_i * p^i = (n_m n_{m-1} ... n_0)_p
        k = sum_{i=0}^m k_i * p^i = (k_m k_{m-1} ... k_0)_p
    then the binomial coefficient satisfies:
        (n choose k) = prod_{i=0}^m (n_i choose k_i)  (mod p)
    where (n_i choose k_i) = 0 whenever n_i < k_i.

    This reduces the computation of (n choose k) mod p for arbitrarily large n and k
    (e.g., 10^18 choose 10^9) to O(log_p(n)) small binomial coefficients mod p, each
    evaluated in O(1) time.

    Args:
        n (int): Total number of items (n >= 0).
        k (int): Number of items to choose (0 <= k <= n).
        p (int): Prime modulus (p >= 2).

    Returns:
        int: (n choose k) mod p in the range [0, p - 1].

    Examples:
        >>> get_combination_mod_p(10, 3, 7)  # (10 choose 3) = 120 = 1 (mod 7)
        1
        >>> get_combination_mod_p(100, 45, 13)
        2
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1 % p
    p = int(p)
    n_digits = number_base_rep(n, p)
    k_digits = number_base_rep(k, p)
    mult = 1
    for a, b in zip(n_digits, k_digits):
        if a < b:
            return 0
        mult = (mult * math.comb(a, b)) % p
    return mult


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
        primes = primes_upto(int(limit))
    return [int(i**2) for i in primes]


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

    Returns: a generator of sub-sequences of options in ascending order

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
def partition_number(n, mod=None):
    """
    Compute the partition number of n, mod m
    Using recursive equation found here: http://www.cs.utsa.edu/~wagner/python/fp/part.html
    p(n) = sum_{k=1}^{n} (-1)^{k+1} (p(x) + p(y))
    x = n - k*(3k-1)/2
    y = n - k*(3k+1)/2
    """
    if n < 0:
        return 0
    if n == 0:
        return 1

    m_sign = 1
    summation = 0

    for k in range(1, n+1):
        if k*(3*k-1) > 2*n:
            break

        x = n - k*(3*k-1) // 2
        y = n - k*(3*k+1) // 2
        summation += m_sign * (partition_number(x, mod=mod) + partition_number(y, mod=mod))
        m_sign *= -1

    if mod:
        summation = summation % mod
    return summation


def euler_totient_function(n):
    dc_factors = primes_of_n(n)
    iter_primes = ((1-1/p) for p in dc_factors.keys())
    output = n
    for p in iter_primes:
        output *= p
    return int(output)


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


def mobius_sieve(n: int, ls_prime: Union[List[int], None]) -> List[int]:
    """
    Returns a list of all mobius function values.
    mobius(n) = 1 if i is square-free with even number of primes,
               -1 if odd number,
                0 if contains square
    """
    ls_m = [1]*n
    if ls_prime is None:
        ls_p = primes_upto(n)
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
    Given the prime factorization of a number, return a generator of the divisors.
    Args:
        prime_factors: a dictionary with the key being the prime and the value being the multiplicity of the prime.
    For example if n=12 then input would be {2:2, 3:1} since 12 = 2*2*3, and the generator would return
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


def coprime(a: int, b: int) -> bool:
    while b != 0:
        a, b = b, a % b
    return a == 1


def smooth_numbers(current_prime_index, current_value, ls_primes, max_n):
    """
    Return a list of all smooth numbers up to the given limit.

    A smooth number is a natural number that is divisible by no primes other than 2 and 3.

    Args:
      current_prime_index: The index of the current prime in the list primes.
      current_value: The current value.
      ls_primes: A list of primes.
      max_n: The maximum number to consider.

    Returns:
      A list of all smooth numbers up to the given limit.
    """

    if current_prime_index == len(ls_primes):
        return [current_value]

    current_prime = ls_primes[current_prime_index]
    results = []
    while current_value <= max_n:
        results.extend(smooth_numbers(current_prime_index + 1, current_value, ls_primes, max_n))
        current_value *= current_prime

    return results


def pisano_period(m: int) -> int:
    """
    Returns the pisano period of integer m.
    The period with which the sequence of Fibonacci numbers taken modulo n repeats.

    See Also: https://en.wikipedia.org/wiki/Pisano_period
    """
    if m == 1:
        return 1

    prev, curr = 0, 1
    for i in range(0, m * m):
        prev, curr = curr, (prev + curr) % m
        if (prev, curr) == (0, 1):
            return i + 1
    return m


def is_int(n):
    return abs(n - int(n)) < 1e-13


def legendre_symbol(a: int, p: int) -> int:
    """
    Compute the Legendre symbol (a / p) for an integer a and an odd prime p.

    The Legendre symbol is defined as:
        (a / p) =  1  if a is a quadratic residue modulo p and a != 0 (mod p)
        (a / p) = -1  if a is a quadratic non-residue modulo p
        (a / p) =  0  if a = 0 (mod p)

    Euler's criterion states: (a / p) = a^((p - 1) / 2) (mod p).

    Args:
        a: Integer numerator.
        p: Odd prime modulus.

    Returns:
        1, -1, or 0.

    Examples:
        >>> legendre_symbol(2, 7)
        1  # 3^2 = 9 = 2 mod 7
        >>> legendre_symbol(3, 7)
        -1
        >>> legendre_symbol(7, 7)
        0
    """
    ls = pow(a % p, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def tonelli_shanks(n: int, p: int) -> Optional[int]:
    """
    Find a modular square root of n modulo an odd prime p using the Tonelli-Shanks algorithm.
    Solves the congruence r^2 = n (mod p) for r in [0, p - 1].

    Algorithm details:
    1. Check quadratic residuosity using Euler's criterion (Legendre symbol). If (n / p) == -1, no solution.
    2. Factor p - 1 as q * 2^s where q is odd.
    3. If s == 1 (i.e. p = 3 mod 4), the root is directly given by n^((p + 1) // 4) mod p.
    4. If s == 2 (i.e. p = 5 mod 8), the root is computed using Atkin's / Legendre's fast path.
    5. For s >= 3, find a quadratic non-residue z mod p and iteratively adjust the powers.

    Args:
        n: The quadratic residue integer.
        p: Odd prime modulus.

    Returns:
        An integer r in [0, p - 1] such that (r * r) % p == n % p, or None if no square root exists.

    Examples:
        >>> tonelli_shanks(10, 13)
        6  # 6^2 = 36 = 10 mod 13
        >>> tonelli_shanks(7, 29)
        None  # 7 is a quadratic non-residue modulo 29
    """
    n = n % p
    if n == 0:
        return 0
    if p == 2:
        return n
    if legendre_symbol(n, p) != 1:
        return None

    # Fast path for p = 3 (mod 4)
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    # Fast path for p = 5 (mod 8)
    if p % 8 == 5:
        v = pow(2 * n, (p - 5) // 8, p)
        i = (2 * n * v * v) % p
        return (n * v * (i - 1)) % p

    # General Tonelli-Shanks for p = 1 (mod 8)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    # Find the smallest quadratic non-residue z mod p
    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1

    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s

    while t != 1:
        temp = t
        i = 0
        while temp != 1 and i < m:
            temp = (temp * temp) % p
            i += 1
        if i == m:
            return None
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i

    return r


def mobius_sieve(n: int) -> list:
    """
    Computes the Mobius function mu(k) for all 0 <= k <= n using a linear sieve.

    mu(k) =  1 if k is a square-free integer with an even number of prime factors
    mu(k) = -1 if k is a square-free integer with an odd number of prime factors
    mu(k) =  0 if k has a squared prime factor

    Returns:
        A list mu of length n + 1 where mu[k] is the Mobius value of k.
    """
    mu = [0] * (n + 1)
    primes = []
    is_prime_flags = [True] * (n + 1)
    if n >= 1:
        mu[1] = 1
    for i in range(2, n + 1):
        if is_prime_flags[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime_flags[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu


def is_prime_simple(n: int) -> bool:
    """
    Deterministic Miller-Rabin primality test for integers up to 2^64.

    Tests divisibility by small primes first, then runs Miller-Rabin witness checks
    using the 12 prime bases (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37).
    Guaranteed deterministic for all integers n < 2^64 (~1.84e19).

    Args:
        n: Integer to test for primality.

    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for a in small_primes:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def continued_fraction_sqrt(d: int) -> Tuple[int, List[int]]:
    """
    Computes the continued fraction expansion of sqrt(d).

    For an integer d > 0, returns (a0, period) where a0 is the integer part
    and period is the list of repeating partial denominators [a1, a2, ..., a_k]
    such that a_k = 2 * a0.
    If d is a perfect square, period is an empty list.

    Example:
        continued_fraction_sqrt(7) -> (2, [1, 1, 1, 4])
        continued_fraction_sqrt(13) -> (3, [1, 1, 1, 1, 6])
    """
    r0 = math.isqrt(d)
    if r0 * r0 == d:
        return r0, []
    m = 0
    den = 1
    a = r0
    period = []
    while a != 2 * r0:
        m = den * a - m
        den = (d - m * m) // den
        a = (r0 + m) // den
        period.append(a)
    return r0, period


def pell_fundamental_solution(d: int) -> Optional[Tuple[int, int]]:
    """
    Finds the fundamental (minimal positive integer) solution (x1, y1) to Pell's equation:
        x^2 - d * y^2 = 1

    Uses the convergents of the continued fraction expansion of sqrt(d).
    Returns None if d is a perfect square.

    Example:
        pell_fundamental_solution(13) -> (649, 180)  # 649^2 - 13 * 180^2 = 1
        pell_fundamental_solution(2)  -> (3, 2)      # 3^2 - 2 * 2^2 = 1
    """
    r0, period = continued_fraction_sqrt(d)
    if not period:
        return None

    p_prev, p_curr = 1, r0
    q_prev, q_curr = 0, 1

    if p_curr * p_curr - d * q_curr * q_curr == 1:
        return p_curr, q_curr

    seq = period * 2 if len(period) % 2 == 1 else period
    for a in seq:
        p_next = a * p_curr + p_prev
        q_next = a * q_curr + q_prev
        p_prev, p_curr = p_curr, p_next
        q_prev, q_curr = q_curr, q_next
        if p_curr * p_curr - d * q_curr * q_curr == 1:
            return p_curr, q_curr

    return p_curr, q_curr


def digits(n: int) -> List[int]:
    """Returns the list of base-10 digits of |n|."""
    return [int(c) for c in str(abs(n))]


def digits_sum(n: int) -> int:
    """Returns the sum of base-10 digits of |n|."""
    return sum(int(c) for c in str(abs(n)))



