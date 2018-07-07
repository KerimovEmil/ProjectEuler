# PROBLEM

# The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

# Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

# ANSWER
# 9110846700


def pe48(max_int, mod):
    """
    PE48 answer.
    Args:
        max_int: the max int of the sum
        mod: how many last digits to keep

    Returns: the PE48 answer.
    """
    answer = 0
    for i in range(1, max_int + 1):
        temp = (i % mod) ** i
        temp = temp % mod
        answer += temp
        answer = answer % mod
    return answer


if __name__ == '__main__':

    last_ten_digits = int(1e10)
    up_to = 1000
    print(pe48(up_to, last_ten_digits))
