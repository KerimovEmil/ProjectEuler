# Take the number 192 and multiply it by each of 1, 2, and 3:
# 192 * 1 = 192
# 192 * 2 = 384
# 192 * 3 = 576
# By concatenating each product we get the 1 to 9 pandigital, 192384576.
# We will call 192384576 the concatenated product of 192 and (1,2,3)

# The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5,
# giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

# What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated
#  product of an integer with (1,2, ... , n) where n > 1?

# Answer = 932718654


def unique_digits(num, existing_digits):
    """
    Test that the digits of the input number are unique and are not in the set of existing digits.
    Args:
        num: <str> integer to test
        existing_digits: <set> digits not allowed (optional)

    Returns: False if the digits of the input number are not unique or are in the set of existing digits,
        else returns new set of used digits.
    """
    str_num_set = set(str(num))
    if '0' in str_num_set:
        return False
    if len(str_num_set) != len(str(num)):
        return False
    if len(str_num_set.intersection(existing_digits)) > 0:
        return False
    else:
        return str_num_set.union(existing_digits)


class Problem38:
    def __init__(self, max_integer, n_digit):
        self.max_integer = max_integer
        self.n_digit = n_digit
        self.max = 0

    def create_sample_pandigital(self, a):
        # ensure that the initial number has no repeated digits
        x = unique_digits(a, set())
        if x is False:
            return 0
        # multiply the number up to the digit 9
        for i in range(2, self.n_digit):
            # check if still no repeated digits
            x = unique_digits(a * i, x)
            if x is False:
                break
            # if still no repeated digits and length is 9 then return solution
            if len(x) == self.n_digit:
                r = str(a)
                i = 2
                while len(r) < self.n_digit:
                    r += str(a * i)
                    i += 1
                return int(r)
        return 0

    def solve(self):
        self.max = max([self.create_sample_pandigital(i) for i in range(1, self.max_integer)])
        return self.max


if __name__ == "__main__":
    obj = Problem38(max_integer=10000, n_digit=9)
    sol = obj.solve()
    print(sol)
