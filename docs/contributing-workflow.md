# Contributing & Workflow Guide

This document defines the development standards, code conventions, testing requirements, and documentation update checklist for adding new Project Euler solutions.

---

## 1. Solution Development Workflow

### Step 1: Generate Scaffolding
From the repository root, run:
```bash
python solutions/new_problem.py <N>
```
This scrapes problem `<N>` from `projecteuler.net` and creates a template file at `solutions/PE0<N>.py`.

### Step 2: Implement the Algorithm
Open `solutions/PE0<N>.py` and structure the code according to the repository standard:

```python
"""
PROBLEM

<problem statement with exact parameters and provided test examples>

ANSWER: <verified answer>
Solve time: ~X.XXX seconds

---
MATHEMATICAL DERIVATION:

1. <Key Observation / Reduction / Algebraic Simplification>:
   Explain how the problem reduces from a brute-force search to a tractable mathematical form.

2. <Recurrence / Invariant / Formula>:
   Detail the exact formulas, transition equations, generating functions, or dynamic programming state transitions.

3. <Complexity Analysis>:
   State the asymptotic time and space complexity in Big-O notation (e.g. O(log N), O(N^(2/3))).
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

    def test_sample(self):
        # Test known smaller cases or examples given in the problem statement
        ...

    def test_solution(self):
        self.assertEqual(<answer>, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
```

### Step 3: Test and Measure Performance
Run the solution locally:
```bash
pytest solutions/PE0<N>.py
```
Ensure that:
- The answer assertion matches.
- Small sample test cases from the problem statement are included in the `Solution<N>` test suite.
- The runtime printed by `@timeit` is recorded in the docstring (`Solve time: ~X.XXX seconds`).
- Complete mathematical derivations, recurrence equations, and complexity analyses are documented in the docstring.

### Step 4: Run the Global Test Suite
Verify that the full CI test suite passes:
```bash
pytest all_build_tests/
```
If the new solution requires $> \sim 3\text{--}5$ seconds to compute from scratch, add `<N>` to `bad_or_slow_solutions` in `all_build_tests/test_build.py` to ensure GitHub Actions CI completes in under 2 minutes.

### Step 5: Git Branch and Pull Request
- Ensure your local branch is branched from or rebased on the latest `origin/main`.
- Create a new branch named `pe<N>` (e.g. `pe534`).
- Commit with message `Pe<N>` or descriptive summary (e.g. `git commit -m "PE0534: Complete solution with DP and bitmasking"`).
- Push to GitHub and open a PR targeting `main`.

---

## 2. Shared Utilities & Refactoring Guidelines (`util/`)

When solving problems, identify generic mathematical primitives and extract them into `util/utils.py`:

1. **When to Extract**:
   - Algorithms applicable across multiple problems (e.g. modular matrix exponentiation, Tonelli-Shanks, Chinese Remainder Theorem, prime/Möbius sieves, Pell equation solvers).
2. **Implementation Rules**:
   - **Immutability & Safety**: Never mutate caller arguments in-place (e.g. avoid mutating matrix entries during modular arithmetic).
   - **Type Annotations**: Provide explicit type hints for all arguments and return values.
   - **Unit Tests**: Always add corresponding test cases in `all_build_tests/test_util.py`.
   - **Documentation**: Document the new utility with arguments and usage examples in `docs/util-reference.md`.
   - **Refactor Duplicates**: Check and update existing solutions that implemented duplicate local versions to import from `util.utils`.

---

## 3. Documentation Update Checklist (What to Update and Why)

When creating a new solution or adding utilities, update the corresponding documentation files as outlined below:

| File to Update | When to Update | Why / Purpose |
|:---------------|:---------------|:--------------|
| [`docs/solutions-index.md`](solutions-index.md) | **Every new solution** | Adds the problem ID, file link, problem topic/description, and measured solve time to the global ledger so contributors and AI pair programmers can search and cross-reference solved problems. |
| [`all_build_tests/test_build.py`](../all_build_tests/test_build.py) | **If solution is slow (>~3–5 seconds)** | Adds `<N>` to `bad_or_slow_solutions` so GitHub Actions CI continues running in under 2 minutes. |
| [`docs/util-reference.md`](util-reference.md) | **If new reusable helpers are added to `util/`** | Documents function signatures, parameters, return types, and usage examples for shared algorithms (e.g. number theory tools, sieves) to prevent code duplication. |
| [`docs/problem-data.md`](problem-data.md) | **If problem uses an external data file** | Documents the new input file placed in `problem_data/`, its format, structure, and the problem that references it. |
| [`docs/repo-overview.md`](repo-overview.md) | **If architecture/structure changes** | Maintains the high-level architecture overview and directory map. |
