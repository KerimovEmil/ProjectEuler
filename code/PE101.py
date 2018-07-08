# Problem 101

# ANSWER
# 37076114526

import numpy as np


def generating_poly(n):
    return (1 + n ** 11) / (1 + n)


def get_answer():
    sum_of_bod = 0
    for k in range(1, 11):
        ls_coef = np.polyfit(y=[generating_poly(i) for i in range(1, k + 1)], x=range(1, k + 1), deg=k - 1)
        sum_of_bod += int(np.poly1d(ls_coef)(k + 1) + 0.5)

    return sum_of_bod


if __name__ == '__main__':
    print(get_answer())

