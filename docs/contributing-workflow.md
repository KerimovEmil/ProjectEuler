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

<problem statement>

ANSWER: <verified answer>
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

### Step 3: Test and Measure Performance
Run the solution locally:
```bash
python -m unittest solutions/PE0<N>.py
```
Ensure that:
- The answer assertion matches.
- The runtime printed by `@timeit` is recorded in the docstring (`Solve time: ~X.XXX seconds`).
- Intricate mathematical derivations and key observations are documented in comments above the class or method.

### Step 4: Run the Global Test Suite
Verify that the full CI test suite passes:
```bash
python -m unittest discover -s all_build_tests
```

### Step 5: Git Branch and Pull Request
- Create a new branch named `pe<N>`.
- Commit with message `Pe<N>` (e.g. `git commit -m "Pe297"`).
- Push to GitHub and open a PR with title `Pe<N>`.

---

## 2. Documentation Update Checklist (What to Update and Why)

When creating a new solution or adding utilities, update the corresponding documentation files as outlined below:

| File to Update | When to Update | Why / Purpose |
|:---------------|:---------------|:--------------|
| [`docs/solutions-index.md`](solutions-index.md) | **Every new solution** | Adds the problem ID, file link, problem topic/description, and measured solve time to the global ledger so contributors and AI pair programmers can search and cross-reference solved problems. |
| [`docs/repo-overview.md`](repo-overview.md) | **Every new solution** | Increments the total solution count and maintains the high-level architecture overview. |
| [`all_build_tests/test_build.py`](../all_build_tests/test_build.py) | **If solution is slow (>~3–5 seconds)** | Adds `<N>` to `bad_or_slow_solutions` so GitHub Actions CI continues running in under 2 minutes. |
| [`docs/problem-data.md`](problem-data.md) | **If problem uses an external data file** | Documents the new input file placed in `problem_data/`, its format, structure, and the problem that references it. |
| [`docs/util-reference.md`](util-reference.md) | **If new reusable helpers are added to `util/`** | Documents function signatures, parameters, return types, and usage examples for shared algorithms (e.g. number theory tools, sieves) to prevent code duplication. |
