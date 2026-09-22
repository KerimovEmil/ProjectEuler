# Experimental and Alternative Solutions

This directory contains alternative, experimental, or pedagogical solution implementations that explore different algorithmic angles (e.g. heuristics, alternative formulations, specialized algorithms) alongside the primary solutions in `solutions/`.

## Catalog

| File | Problem | Paradigm / Variant | Notes |
|:-----|:--------|:-------------------|:------|
| [`PE0185_recursive.py`](PE0185_recursive.py) | PE 185: Number Mind | Depth-First Search with Constraint Propagation | Solves sample 5-digit game in ~0.05s; encounters combinatorial explosion on 16-digit game. |
| [`PE0185_simulated_annealing.py`](PE0185_simulated_annealing.py) | PE 185: Number Mind | Stochastic Hill Climbing / Local Search | Original randomized local search solver (~180s); optimizes clue overlap error via random restarts & mutations. |
| [`PE0345_Hungarian_Algorithm.py`](PE0345_Hungarian_Algorithm.py) | PE 345: Matrix Sum | Hungarian (Munkres) Bipartite Matching | Demonstrates polynomial $O(N^3)$ assignment using `util.utils.Hungarian`. |
| [`PE0345_recursive.py`](PE0345_recursive.py) | PE 345: Matrix Sum | Subproblem Memoization / Bitmask DP | Standalone memoized depth-first search over remaining columns. |
