# Utility Library Reference (`util/`)

This document catalogs shared mathematical algorithms, number theory tools, matrix utilities, and combinatorial functions available in the `util/` package.

---

## 1. Modular Arithmetic & Number Theory (`util/utils.py`)

### `legendre_symbol(a: int, p: int) -> int`
Computes the Legendre symbol $\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod p$ for an integer $a$ and an odd prime $p$.
- Returns `1` if $a$ is a quadratic residue modulo $p$ ($a \not\equiv 0$).
- Returns `-1` if $a$ is a quadratic non-residue modulo $p$.
- Returns `0` if $a \equiv 0 \pmod p$.

### `tonelli_shanks(n: int, p: int) -> Optional[int]`
Solves $r^2 \equiv n \pmod p$ for $r \in [0, p-1]$ using the Tonelli-Shanks algorithm.
- Supports fast paths for $p \equiv 3 \pmod 4$ and $p \equiv 5 \pmod 8$.
- Returns `None` if $n$ is a quadratic non-residue modulo $p$.

### `prime_sieve(n: int) -> np.ndarray[bool]`
Generates a boolean numpy array of size `n + 1` where index `i` is `True` if `i` is prime.

### `primes_upto(n: int) -> np.ndarray[int]`
Returns a numpy array containing all prime numbers less than or equal to `n`.

### `count_primes_upto(n: int) -> int`
Returns the total count of prime numbers $\le n$.

### `primes_of_n(n: int, ls_prime: list = None) -> Dict[int, int]`
Returns the prime factorization of $n$ as a dictionary of `{prime: multiplicity}`.

### `square_free_sieve(limit: int) -> Generator[int]`
Generator yielding all square-free numbers strictly less than `limit`.

### `square_primes_sieve(limit: int, primes: list = None) -> List[int]`
Returns all prime squares $p^2 < \text{limit}$.

### `euler_totient_function(n: int) -> int`
Computes Euler's totient $\phi(n) = n \prod_{p \mid n} (1 - 1/p)$.

### `sum_phi(n: int) -> int`
Computes the summatory totient function $\sum_{i=1}^n \phi(i)$ using memoized sublinear recurrence.

### `mobius_sieve(n: int, ls_prime: Optional[List[int]] = None) -> List[int]`
Computes the Möbius function $\mu(k)$ for all $0 \le k \le n$. Uses prime slicing if `ls_prime` is provided; otherwise uses an $O(n)$ linear sieve.
- Returns `1` if $k$ is square-free with an even number of prime factors.
- Returns `-1` if $k$ is square-free with an odd number of prime factors.
- Returns `0` if $k$ has a squared prime factor.

### `is_prime_simple(n: int) -> bool`
Deterministic Miller-Rabin primality test for integers up to $2^{64}$ ($\approx 1.84 \times 10^{19}$).
- Tests small prime divisibility first, then checks 12 prime bases $(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)$.
- Runs in $O(\log^3 n)$ time without memory allocation.

### `continued_fraction_sqrt(d: int) -> Tuple[int, List[int]]`
Computes the continued fraction expansion of $\sqrt{d}$ using exact integer arithmetic.
- Returns `(a0, period)` where $a_0 = \lfloor\sqrt{d}\rfloor$ and `period` is the repeating sequence $[a_1, a_2, \dots, a_k]$ (ending in $2a_0$).
- Returns `(isqrt(d), [])` if $d$ is a perfect square.

### `pell_fundamental_solution(d: int) -> Optional[Tuple[int, int]]`
Finds the fundamental (minimal positive integer) solution $(x_1, y_1)$ to Pell's equation $x^2 - d y^2 = 1$.
- Uses convergents of the continued fraction expansion of $\sqrt{d}$.
- Returns `None` if $d$ is a perfect square.

### `digits(n: int) -> List[int]`
Returns the list of base-10 digits of $|n|$ (e.g. `digits(12345) -> [1, 2, 3, 4, 5]`).

### `digits_sum(n: int) -> int`
Returns the sum of base-10 digits of $|n|$ (e.g. `digits_sum(12345) -> 15`).

### `is_palindrome(n: Union[int, str]) -> bool`
Returns `True` if $n$ is a palindrome (reads identically forwards and backwards in base 10), else `False`.

### `is_int(n: float, tol: float = 1e-12) -> bool`
Returns `True` if floating-point number $n$ is within `tol` of an integer.

### `coprime(a: int, b: int) -> bool`
Returns `True` if $\gcd(a, b) == 1$, else `False`.

### `pisano_period(m: int) -> int`
Computes the Pisano period (the period length with which the sequence of Fibonacci numbers modulo $m$ repeats).

### `cycle_length(k: int) -> int`
Returns the period length of recurring decimal digits in $1/k$.


---

## 2. Matrix Algebra & Linear Recurrences (`util/utils.py`)

### `Matrix`
Integer matrix class supporting:
- Matrix multiplication (`A * B` or `A @ B`)
- Modular matrix multiplication (`(A * B) % mod`)
- Fast matrix exponentiation (`pow(A, power, mod)` or `A ** power`)

### `LinearHomogeneousRecurrence(coefficients, initial_values)`
Solves constant-coefficient linear homogeneous recurrences of the form:
$$f(n) = c_1 f(n-1) + c_2 f(n-2) + \dots + c_k f(n-k)$$
using companion matrix exponentiation in $O(k^3 \log n)$ time.
- Method: `get(n, mod=None)` returns $f(n) \pmod{\text{mod}}$.

---

## 3. Chinese Remainder Theorem (`util/crt.py`)

### `ChineseRemainderTheorem(remainders, modulos)`
Solves systems of congruences $x \equiv a_i \pmod{n_i}$ where moduli $n_i$ are pairwise coprime.

### `ChineseRemainderTheoremSets(remainders, modulos)`
Solves systems where each remainder is a set of candidate residues: $x \equiv r \pmod{n_i}$ for $r \in R_i$. Returns all consistent global residues.

### `bezout_thm(a, b) -> (x, y)`
Extended Euclidean Algorithm: finds integers $x, y$ such that $a \cdot x + b \cdot y = \gcd(a, b)$.

---

## 4. Exact Cover & Backtracking (`util/dlx.py`)

### `DancingLinks(matrix)`
Knuth's Algorithm X using Dancing Links (DLX) for solving exact cover problems (e.g. Sudoku, Pentominoes, Polyomino tiling).

---

## 5. Special Sequences & Combinatorics (`util/utils.py`, `util/special_number_series.py`)

### `combin(n: int, r: int) -> int`
Fast bitwise computation of binomial coefficient $\binom{n}{r}$.

### `partition_number(n: int, mod: int = None) -> int`
Computes the integer partition function $p(n)$ using Euler's pentagonal number theorem recurrence.

### `BinomialCoefficient(prime: int)`
Evaluates $\binom{m}{n} \pmod p$ for large $m, n$ using Lucas' theorem.

### `EulerNumber(prime: int)`
Computes Euler numbers modulo a prime.

### `bernoulli(n: int) -> Fraction` (`util/special_number_series.py`)
Computes the $n$-th Bernoulli number $B_n$ as an exact rational `fractions.Fraction`.

### `zeta(n: int) -> float` (`util/special_number_series.py`)
Computes $\zeta(2k)$ for even integers using exact Bernoulli numbers.

---

## 6. General Helpers & Profiling (`util/utils.py`)

### `@timeit`
Decorator measuring and logging the elapsed execution time of a method:
```python
@timeit
def solve(self):
    ...
```

### `Hungarian(cost_matrix)`
Numpy-based Hungarian (Munkres) assignment problem solver (for min-cost or max-profit bipartite matchings).
