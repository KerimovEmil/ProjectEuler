"""
PROBLEM

The following undirected network consists of seven vertices and twelve edges with a total weight of 243.

The same network can be represented by the matrix below:
    A   B   C   D   E   F   G
A   -  16  12  21   -   -   -
B  16   -   -  17  20   -   -
C  12   -   -  28   -  31   -
D  21  17  28   -  18  19  23
E   -  20   -  18   -   -  11
F   -   -  31  19   -   -  27
G   -   -   -  23  11  27   -

However, it is possible to optimise the network by removing some edges and still ensure that all points on the
network remain connected. The network which achieves the maximum saving has a weight of 93, representing a saving
of 243 - 93 = 150 from the original network.

Using network.txt (p107_network.txt), a 6K text file containing a network with forty vertices, and given in matrix
form, find the maximum saving which can be achieved by removing redundant edges whilst ensuring that the network
remains connected.

ANSWER: 259679
Solve time: ~0.001 seconds

---
MATHEMATICAL DERIVATION:

1. Reduction to Minimum Spanning Tree (MST):
   Let G = (V, E, w) be a connected, undirected, weighted graph with total edge weight W = sum_{e in E} w(e).
   Removing redundant edges while keeping all vertices in V connected is equivalent to selecting a connected
   spanning subgraph T = (V, E') that minimizes W(T) = sum_{e in E'} w(e), which maximizes the saving W - W(T).
   Since all edge weights are positive, any cycle in T can have an edge removed to strictly decrease W(T) without
   disconnecting V. Thus, the optimal subgraph T is a Minimum Spanning Tree of G.

2. Kruskal's Algorithm with Disjoint-Set Union (DSU):
   - Since the adjacency matrix M is symmetric, the undirected edges are extracted from the upper triangle i < j
     where M[i][j] != '-'.
   - Sorting the |E| edges by non-decreasing weight and greedily adding edges (u, v) that connect distinct
     components in a Disjoint-Set Union structure yields the exact MST weight in O(|E| log |E|) time.
"""

import os
import unittest
from util.utils import timeit


class Problem107:
    def __init__(self, matrix: list[list[int | None]] | None = None):
        if matrix is None:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'problem_data', 'p107_network.txt')
            with open(file_path, 'r', encoding='utf-8') as f:
                matrix = [
                    [None if token == '-' else int(token) for token in line.strip().split(',')]
                    for line in f if line.strip()
                ]
        self.matrix = matrix

    @staticmethod
    def max_saving(matrix: list[list[int | None]]) -> int:
        n = len(matrix)
        edges: list[tuple[int, int, int]] = []
        total_weight = 0

        for i in range(n):
            for j in range(i + 1, n):
                weight = matrix[i][j]
                if weight is not None:
                    edges.append((weight, i, j))
                    total_weight += weight

        edges.sort()
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        mst_weight = 0
        edges_added = 0
        for weight, u, v in edges:
            root_u, root_v = find(u), find(v)
            if root_u != root_v:
                parent[root_u] = root_v
                mst_weight += weight
                edges_added += 1
                if edges_added == n - 1:
                    break

        return total_weight - mst_weight

    @timeit
    def solve(self) -> int:
        return self.max_saving(self.matrix)


class Solution107(unittest.TestCase):
    def setUp(self):
        self.problem = Problem107()

    def test_sample(self):
        sample_matrix = [
            [None, 16, 12, 21, None, None, None],
            [16, None, None, 17, 20, None, None],
            [12, None, None, 28, None, 31, None],
            [21, 17, 28, None, 18, 19, 23],
            [None, 20, None, 18, None, None, 11],
            [None, None, 31, 19, None, None, 27],
            [None, None, None, 23, 11, 27, None],
        ]
        self.assertEqual(150, self.problem.max_saving(sample_matrix))

    def test_solution(self):
        self.assertEqual(259679, self.problem.solve())


if __name__ == '__main__':
    unittest.main()
