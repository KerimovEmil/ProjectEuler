# The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

# There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

# What 12-digit number do you form by concatenating the three terms in this sequence?

# Answer: 2969, 6299, 9629

from util.utils import sieve


P = list(sieve(10000))
P2 = list(sieve(1000))
T = P[len(P2):]
Q = set(T)
U = []
for x in T:
    for i in range(1, 5000):
        if ((x + i) in Q) and ((x + 2 * i) in Q):
            if set(str(x)) == set(str(x + i)):
                if set(str(x)) == set(str(x + 2 * i)):
                    U.append(x)
                    U.append(x + i)
                    U.append(x + 2 * i)

print(U)
ls_sol = [str(x) for x in U if x not in {1487, 4817, 8147}]

print(''.join(ls_sol))