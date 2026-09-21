# Problem Data Map

The `problem_data/` directory contains input datasets and text files required by specific Project Euler problems.

## Data Files Catalog

| File Name | Solution | Description / Format |
|:----------|:---------|:---------------------|
| `p008_series.txt` | [`PE0008.py`](../solutions/PE0008.py) | 1000-digit integer series |
| `p011_grid.txt` | [`PE0011.py`](../solutions/PE0011.py) | 20x20 grid of numbers |
| `p013_numbers.txt` | [`PE0013.py`](../solutions/PE0013.py) | 100 x 50-digit integers |
| `p018_triangle.txt` | [`PE0018.py`](../solutions/PE0018.py) | 15-row number triangle |
| `p022_names.txt` | [`PE0022.py`](../solutions/PE0022.py) | Over 5,000 comma-separated, quoted first names |
| `p042_words.txt` | [`PE0042.py`](../solutions/PE0042.py) | Nearly 2,000 common English words |
| `p054_poker.txt` | [`PE0054.py`](../solutions/PE0054.py) | 1,000 poker hands for two players (5 cards each) |
| `p059_cipher.txt` | [`PE0059.py`](../solutions/PE0059.py) | Comma-separated ASCII values encrypted with XOR |
| `p067_triangle.txt` | [`PE0067.py`](../solutions/PE0067.py) | 100-row number triangle |
| `p079_keylog.txt` | [`PE0079.py`](../solutions/PE0079.py) | 50 successful 3-digit passcode login attempts |
| `p081_matrix.txt` | [`PE0081.py`](../solutions/PE0081.py) | 80x80 matrix of integers (path sum: two ways) |
| `p082_matrix.txt` | [`PE0082.py`](../solutions/PE0082.py) | 80x80 matrix of integers (path sum: three ways) |
| `p083_matrix.txt` | [`PE0083.py`](../solutions/PE0083.py) | 80x80 matrix of integers (path sum: four ways) |
| `p089_roman.txt` | [`PE0089.py`](../solutions/PE0089.py) | 1,000 numbers in valid but un-minimized Roman numerals |
| `p096_sudoku.txt` | [`PE0096.py`](../solutions/PE0096.py) | 50 9x9 Sudoku puzzles |
| `p098_words.txt` | [`PE0098.py`](../solutions/PE0098.py) | List of ~2,000 English words for anagram square analysis |
| `p099_base_exp.txt` | [`PE0099.py`](../solutions/PE0099.py) | 1,000 lines of `base,exponent` pairs |
| `p102_triangles.txt` | [`PE0102.py`](../solutions/PE0102.py) | 1,000 triangle coordinate triples `(x1,y1,x2,y2,x3,y3)` |

## Accessing Problem Data in Solutions

When loading data files from inside a solution file in `solutions/`, always use relative paths anchored to `__file__`:

```python
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p022_names.txt')
with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read()
```
