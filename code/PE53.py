# It is not until n = 23, that a value exceeds one-million: 23C10 = 1144066.

# How many, not necessarily distinct, values of  nCr, for 1 <= n <= 100, are greater than one-million?

# Answer = 4075

def combin(n, r):
    """A fast way to calculate binomial coefficients by Andrew Dalke (contrib)."""
    if 0 <= r <= n:
        ntok = 1
        rtok = 1
        for t in range(1, min(r, n - r) + 1):
            ntok *= n
            rtok *= t
            n -= 1
        return ntok // rtok
    else:
        return 0


count = 0
for n in range(0, 101):
    for r in range(0, int(n / 2 + 1)):
        if combin(n, r) > 1000000:
            count += n - 2 * r + 1
            break
print(count)
