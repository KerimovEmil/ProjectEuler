# ANSWER
# 210


def answer():
    i = 1
    ls = []
    while i < 500000:
        ls.append(i)
        i = i + 1
    s = ''.join(map(str, ls))
    return int(s[0]) * int(s[9]) * int(s[99]) * int(s[999]) * int(s[9999]) * int(s[99999]) * int(s[999999])


if __name__ == '__main__':
    print(answer())
