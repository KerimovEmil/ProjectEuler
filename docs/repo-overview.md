# ProjectEuler Repo Overview

This repository contains Python solutions to [Project Euler](https://projecteuler.net) problems.
As of the latest commit, there are 164 solutions (PE0001 through PE0853), added incrementally via
pull requests. The `README.md` is essentially empty, so
this doc serves as the reference for the project's structure and conventions.

## Directory layout

| Path                        | Purpose                                                                 |
|-----------------------------|-------------------------------------------------------------------------|
| `solutions/`                | One `PE0<N>.py` file per solved problem (e.g. `PE0001.py`, `PE0381.py`)  |
| `solutions/new_problem.py`  | Scaffolding script: scrapes a problem description and writes a stub     |
| `util/`                     | Shared math / number-theory helpers imported by solutions               |
| `problem_data/`             | Input data files for problems that read from a file                     |
| `all_build_tests/`          | Test package that runs every solution's unittest class                  |
| `.github/workflows/`        | GitHub Actions CI                                                       |
| `requirements.txt`          | Single dependency: `numpy==2.3.2`                                       |

## Solution file conventions

Every `solutions/PE0<N>.py` follows the same pattern:

```python
"""
PROBLEM

<pasted problem statement>

ANSWER: <known answer>
Solve time: ~X.XXX seconds
"""

import unittest
from util.utils import timeit


class Problem<N>:
    def __init__(self):
        pass

    @timeit
    def solve(self):
        ...


class Solution<N>(unittest.TestCase):
    def setUp(self):
        self.problem = Problem<N>()

    def test_solution(self):
        self.assertEqual(<answer>, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
```

Notes:

- The module-level docstring records the problem statement, the correct answer, and the
  measured solve time (used to flag slow solutions).
- The solve method is always wrapped with `@timeit`, which prints
  `<module> took: X.XXX seconds`.
- Correctness is verified via a `unittest.TestCase` assertion, never by `print`.
- Intricate problems typically document their derivation in comments above the solution
  (e.g. `PE0381.py` works out the `S(p) = -3/8 mod p` simplification using Wilson's theorem;
  `PE0169.py` explains the binary-zero-count approach).
- Problems that read a file construct their data path with
  `os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p0NN_xxx.txt')`.

## The `util` library

### `util/utils.py` — general toolkit

- **Hungarian algorithm** (`Hungarian`, `CoverZeros`): numpy-based assignment-problem solver
  (cost or profit matrix, auto-pads to square).
- **`Matrix`**: integer matrix with `*`, fast exponentiation `**`, and `% mod` — used to
  compute linear recurrences quickly.
- **`LinearHomogeneousRecurrence`**: solves `f(n+1) = c(n)f(n) + ... + c(n-k)f(n-k)` using a
  companion matrix and fast exponentiation.
- **`BaseConverter`** / **`BinomialCoefficient`** / **`EulerNumber`**: binomial coefficients
  mod a prime (Lucas-style digit decomposition) and Euler numbers.
- **Primes**: `prime_sieve`, `primes_upto`, `count_primes_upto`, `primes_of_n`
  (prime factorization), `square_free_sieve`, `euler_totient_function`.
- **`timeit`**: decorator that prints elapsed seconds.
- **Number theory**: `mobius_sieve`, `partition_number` (DP), `sum_phi` (summatory totient),
  `Farey`/`len_faray_seq`, `divisors`, `num_of_divisors`, `cycle_length` (recurring decimals),
  `pisano_period`, `smooth_numbers`.
- **Combinatorics**: `combin`, `binomial_recursive`, `fib`, `fibonacci_n_term`,
  `fibonacci_k_n_term`, `catalan_transform`, `inv_catalan_transform`.
- **Modular arithmetic**: `get_all_mod_inverse_dict/list`, `new_mod` (string-based
  divisibility rules), `coprime`.
- **Helpers**: `factorial` variants, `lcm`, `cumsum`, `is_pandigital`, `is_palindrome`,
  `is_int`, `generate_ascending_sub_sequence`, `sign`.

### `util/crt.py` — Chinese Remainder Theorem

- `ChineseRemainderTheorem`: solves `x = a_i (mod n_i)` for scalar residues.
- `ChineseRemainderTheoremSets`: solves `x in {a_i} (mod n_i)` where each residue is a set of
  values, returning every compatible root.
- `SetInteger`: integer set class supporting scalar/`SetInteger` arithmetic (`*`, `+`, `//`,
  `%`, `**`, `get_all_under`).
- `bezout_thm`: extended Euclid returning `x, y` with `a*x + b*y = 1`.
- `NoSolutionException`: raised when congruences are incompatible.

### `util/dlx.py` — Dancing Links (exact cover)

- `DancingLinks`: Knuth's DLX exact-cover solver. Columns = constraints, rows = choices that
  satisfy them. Builds a circular sparse matrix (`SparseMatrix`) and solves by backtracking
  with cover/uncover. Exports `DancingLinks`, `LeftIterator`.
- Ships an embedded `unittest` (`DlxTest`) demonstrating the classic 6x7 example matrix.

### `util/special_number_series.py`

- `bernoulli(n)`: nth Bernoulli number as a `Fraction`.
- `zeta(n)`: Riemann zeta function only for even `n`, derived from Bernoulli numbers.

## Problem data map

`problem_data/` holds the input files referenced by solutions:

| File                 | Used by | Contents                              |
|----------------------|---------|--------------------------------------|
| `p008_series.txt`    | PE8     | 1000-digit number series              |
| `p011_grid.txt`      | PE11    | 20x20 number grid                     |
| `p013_numbers.txt`   | PE13    | 100 x 50-digit numbers                |
| `p018_triangle.txt`  | PE18    | Number triangle                       |
| `p022_names.txt`     | PE22    | List of names                         |
| `p042_words.txt`     | PE42    | Triangle words                        |
| `p054_poker.txt`     | PE54    | 1000 poker hands (5 cards per player) |
| `p059_cipher.txt`    | PE59    | XOR-encrypted cipher                  |
| `p067_triangle.txt`  | PE67    | Large number triangle                 |
| `p079_keylog.txt`    | PE79    | 50 keylog attempts                    |
| `p081_matrix.txt`    | PE81    | 80x80 matrix                          |
| `p082_matrix.txt`    | PE82    | 80x80 matrix                          |
| `p083_matrix.txt`    | PE83    | 80x80 matrix                          |
| `p089_roman.txt`     | PE89    | Roman numerals                        |
| `p096_sudoku.txt`    | PE96    | 50 sudoku puzzles                     |
| `p099_base_exp.txt`  | PE99    | 1000 base/exponent pairs              |
| `p102_triangles.txt` | PE102   | Triangle coordinate triples           |

## Testing and CI

- Every solution file is itself a runnable `unittest` module:
  `python -m unittest solutions.PE0381` (or `python solutions/PE0381.py`).
- `all_build_tests/test_build.py` imports **every** `solutions.PE0<N>` module dynamically,
  registers each `Solution<N>` class, and runs the whole suite:
  `python -m unittest discover -s all_build_tests`.
- A hardcoded list skips slow or broken solutions:

  ```python
  bad_or_slow_solutions = [96, 179, 185, 211, 221, 266, 330, 365, 401, 419, 420, 432, 678]
  ```

- `all_build_tests/test_crt.py` unit-tests the CRT implementation (scalar, set-based, and
  random non-coprime cases). `all_build_tests/test_util.py` is a placeholder.
- `.github/workflows/python-package.yml` runs on push/PR to `main` with Python 3.12 and 3.13:
  1. Install `flake8`, `pytest`, and `requirements.txt`.
  2. Lint with flake8 (`E9,F63,F7,F82` fatal; everything else warning-level).
  3. Run `python -m unittest discover -s all_build_tests`.

## Adding a new solution (workflow)

1. Run `python solutions/new_problem.py <N>` from the repo root. It scrapes
   `https://projecteuler.net/problem=<N>` and writes a templated `solutions/PE0<N>.py` stub
   (requires `requests` and `beautifulsoup4`, which are NOT in `requirements.txt`). It refuses
   to overwrite an existing file.
2. Implement `Problem<N>.solve()` and delete the placeholder
   `self.assertEqual(1, self.problem.solve())`.
3. Run the file's tests to confirm the answer; record it in the docstring along with the
   measured solve time.
4. If the problem reads data, drop the file into `problem_data/` and reference it via the
   `os.path.join(os.path.dirname(__file__), '..', 'problem_data', ...)` pattern.
5. If the solution is slow (>~ a few seconds), add its number to `bad_or_slow_solutions` in
   `all_build_tests/test_build.py` so CI stays fast.
6. Open a PR titled like `Pe<N>` (matches historical commit style, e.g. `Pe381`).