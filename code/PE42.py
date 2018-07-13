# The nth term of the sequence of triangle numbers is given by, tn = n(n+1)/2; so the first ten triangle numbers are:

# 1, 3, 6, 10, 15, 21, 28, 36, 45, 55,

# By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.

# Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?

# Answer = 162

T = set()
for i in range(100):
    T.add(i * (i + 1) / 2)


def decod(L):
    if L == "A":
        return 1
    if L == "B":
        return 2
    if L == "C":
        return 3
    if L == "D":
        return 4
    if L == "E":
        return 5
    if L == "F":
        return 6
    if L == "G":
        return 7
    if L == "H":
        return 8
    if L == "I":
        return 9
    if L == "J":
        return 10
    if L == "K":
        return 11
    if L == "L":
        return 12
    if L == "M":
        return 13
    if L == "N":
        return 14
    if L == "O":
        return 15
    if L == "P":
        return 16
    if L == "Q":
        return 17
    if L == "R":
        return 18
    if L == "S":
        return 19
    if L == "T":
        return 20
    if L == "U":
        return 21
    if L == "V":
        return 22
    if L == "W":
        return 23
    if L == "X":
        return 24
    if L == "Y":
        return 25
    if L == "Z":
        return 26


def enum(word):
    sum = 0
    for i in word:
        sum += decod(i)
    return sum


ans = 0

old_words = open(r"..\problem_data\p042_words.txt", 'r+').read().split(',')
words = []
for i in range(len(old_words)):
    word = old_words[i][1:-1]
    if enum(word) in T:
        ans += 1

print(ans)
