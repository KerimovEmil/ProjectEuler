# ProjectEuler Repo Overview

This repository contains Python solutions to [Project Euler](https://projecteuler.net) problems.
As of the latest commit, there are 175 solutions (PE0001 through PE0853), added incrementally via pull requests.

This document serves as the high-level architecture overview and directory map. For detailed guides, see the specialized documents linked below.

---

## Documentation Index

- **[Contributing & Workflow Guide](contributing-workflow.md)**: Coding conventions, standard solution template, performance guidelines, PR practices, and the **Documentation Update Checklist** (what docs to update when adding a solution and why).
- **[Utility Library Reference](util-reference.md)**: Catalog of mathematical algorithms, number theory tools (e.g. `tonelli_shanks`, `legendre_symbol`, sieves), linear recurrences (`Matrix`, `LinearHomogeneousRecurrence`), Chinese Remainder Theorem, and exact-cover (`DancingLinks`) in `util/`.
- **[Solutions Index](solutions-index.md)**: Comprehensive table of all solved problems, filenames, topics, and solve times.
- **[Problem Data Map](problem-data.md)**: Mapping of input text and grid files in `problem_data/` to their respective problem solutions.

---

## Directory Layout

| Path | Purpose |
|:-----|:--------|
| `solutions/` | One `PE0<N>.py` file per solved problem (e.g. `PE0001.py`, `PE0752.py`) |
| `solutions/new_problem.py` | Scaffolding script: scrapes problem description and generates a stub |
| `experimental_solutions/` | Alternative, experimental, or pedagogical variants of problem solutions |
| `util/` | Reusable math, number-theory, and matrix algorithms imported by solutions |
| `problem_data/` | Input datasets, triangles, matrices, and word lists |
| `all_build_tests/` | Comprehensive test package running every solution's `unittest.TestCase` |
| `docs/` | Repository documentation, guides, and reference materials |
| `.github/workflows/` | GitHub Actions Continuous Integration (CI) |
| `requirements.txt` | Runtime dependencies (`numpy==2.3.2`) |

---

## Testing and CI

- **Single Solution**: Run `python -m unittest solutions.PE0<N>` (or `python solutions/PE0<N>.py`).
- **All Solutions**: Run `python -m unittest discover -s all_build_tests`.
- **Utilities**: Run `python -m unittest all_build_tests/test_util.py` or `python -m unittest all_build_tests/test_crt.py`.
- **Continuous Integration**: `.github/workflows/python-package.yml` runs on push/PR to `main` across Python 3.12 and 3.13, checking linting via `flake8` and executing the full build test suite.