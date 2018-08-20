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


def unique_digits(str_num):
    """
    Test that the digits of the input number are unique and are not 0.
    Args:
        str_num: <str> integer to test

    Returns: False if the digits of the input number are not unique else True
    """
    str_num_set = set(str_num)
    if '0' in str_num_set:
        return False
    elif len(str_num_set) != len(str_num):
        return False
    else:
        return True


class Problem38:
    def __init__(self, max_integer, n_digit):
        self.max_integer = max_integer
        self.n_digit = n_digit
        self.max = 0

    def create_sample_pandigital(self, num):
        num_str = str(num)
        # ensure that the initial number has no repeated digits or 0
        if unique_digits(num_str) is False:
            return 0
        # multiply the number up to the digit 9
        for i in range(2, self.n_digit):
            num_str += str(num * i)
            # check if still no repeated digits
            if unique_digits(num_str) is False:
                break
            # if still no repeated digits and length is 9 then return solution
            if len(num_str) == self.n_digit:
                return int(num_str)
        return 0

    def solve(self):
        self.max = max([self.create_sample_pandigital(i) for i in range(1, self.max_integer)])
        return self.max


if __name__ == "__main__":
    obj = Problem38(max_integer=10000, n_digit=9)
    sol = obj.solve()
    print(sol)
