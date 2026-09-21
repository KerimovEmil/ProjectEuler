__all__ = ['DancingLinks', 'LeftIterator']

import unittest


class Head:
    """
    Column header class.

    Used to access elements within a column.
    """

    def __init__(self, col_idx):
        self.col_idx = col_idx
        self.left, self.right = None, None
        self.up, self.down = self, self
        self.size = 0

    def remove_from_row(self):
        """
        Remove the column header node from the special column header row.
        """
        self.left.right = self.right
        self.right.left = self.left

    def readd_to_row(self):
        """
        Re-add the column header node to the special column header row.
        """
        self.left.right = self.right.left = self


class Node:
    """
    Node class that represents, through its existence, a binary value (i.e. 1)

    This is a node that is only ever supposed to be a part of a sparse binary matrix. It can
    access elements in all 4 directions: `up`, `down`, `left`, `right`.
    """

    def __init__(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.up, self.down = None, None
        self.left, self.right = None, None
        self.head = None

    def remove_from_column(self):
        """
        Remove a particular row element from a column.
        """
        self.up.down = self.down
        self.down.up = self.up
        self.head.size -= 1

    def readd_to_column(self):
        """
        Re-add a particular row element to a column.
        """
        self.up.down = self.down.up = self
        self.head.size += 1


class NodeIterator:
    """
    Iterate through nodes in a particular direction
    """

    def __init__(self, node):
        self.curr = self.start = node

    def __iter__(self):
        return self

    def __next__(self):
        _next = self._move(self.curr)
        if _next == self.start:
            raise StopIteration()
        else:
            self.curr = _next
            return _next

    def _move(self, node):
        raise NotImplementedError()


class LeftIterator(NodeIterator):
    def _move(self, node):
        return node.left


class RightIterator(NodeIterator):
    def _move(self, node):
        return node.right


class UpIterator(NodeIterator):
    def _move(self, node):
        return node.up


class DownIterator(NodeIterator):
    def _move(self, node):
        return node.down


class SparseMatrix:
    """
    Sparse boolean matrix

    A fully interconnected set of nodes in a sparse matrix. The existence of a node
    represents a value of `1` in a particular row & column position.
    """

    def __init__(self, mat):
        """Converts a fully specified matrix to its sparse form.

        Parameters
        ----------
        self: The sparse matrix instance
        mat: A bool[][] denoting a fully specified matrix

        Returns
        -------
        A sparse matrix version of the provided fully specified matrix.
        """
        nrows = len(mat)
        ncols = len(mat[0])

        srows = [[] for _ in range(nrows)]
        heads = [Head(j) for j in range(ncols)]
        scols = [[head] for head in heads]

        self.ghead = Head(-1)
        heads = [self.ghead] + heads
        self.create_lr_links([heads])

        for i in range(nrows):
            for j in range(ncols):
                if mat[i][j]:
                    node = Node(i, j)
                    scols[j].append(node)
                    srows[i].append(node)

        self.create_lr_links(srows)
        self.create_ud_links(scols)

    def create_lr_links(self, srows):
        """Iterate through the rows and add left-right links for each item in the row.

        Parameters
        ----------
        self: the sparse matrix
        srows: a Node[][], where each item denotes a particular row, and each element in that item denotes
          an element in the matrix

        Returns
        -------
        None. Purely mutates internal state.
        """
        for srow in srows:
            n = len(srow)
            for j in range(n):
                srow[j].right = srow[(j + 1) % n]
                srow[j].left = srow[(j - 1 + n) % n]

    def create_ud_links(self, scols):
        """Iterate through the columns and add up-down links for each item in the column.
        In addition it also adds a reference to the header node.

        Parameters
        ----------
        self: the sparse matrix
        scols: a Node[][], where each item denotes a particular column, and each element in that item denotes
          an element in the matrix

        Returns
        -------
        None. Purely mutates internal state.
        """
        for scol in scols:
            n = len(scol)
            scol[0].size = n - 1
            for j in range(n):
                scol[j].down = scol[(j + 1) % n]
                scol[j].up = scol[(j - 1 + n) % n]
                scol[j].head = scol[0]


class DancingLinks:
    """
    A class that implements the Dancing Links per Knuth's DLX paper.
    """

    def __init__(self, mat):
        """Initializes the solver based on the provided matrix.
        Columns in the matrix represent constraints, rows represent choices that satisfy a given constraint.

        Parameters
        ----------
        self: the DancingLinks solver
        mat: An exact-cover matrix with columns representing constraints and rows representing choices.

        Returns
        -------
        The initialized solver instance.
        """
        self.solution = []
        self.smat = SparseMatrix(mat)

    def _cover(self, col):
        """Cover a particular column.

        Removes a column from the column header row, and then removes all rows that satisfy
        said column.

        Parameters
        ----------
        self: the DancingLinks solver instance.
        col: The column that aught to be covered.

        Returns
        -------
        None. Purely mutates internal state.
        """
        col.remove_from_row()
        row_in_col = col.down
        while row_in_col != col:
            row_cell = row_in_col.right
            while row_cell != row_in_col:
                row_cell.remove_from_column()
                row_cell = row_cell.right
            row_in_col = row_in_col.down

    def _uncover(self, col):
        """Uncovers a particular column.

        Re-adds a column to the column header row, after re-adding all rows that satisfy
        said column.

        Parameters
        ----------
        self: the DancingLinks solver instance
        col: The column to be uncovered.

        Returns
        -------
        None. Purely mutates internal state.
        """
        row_in_col = col.up
        while row_in_col != col:
            row_cell = row_in_col.left
            while row_cell != row_in_col:
                row_cell.readd_to_column()
                row_cell = row_cell.left
            row_in_col = row_in_col.up
        col.readd_to_row()

    def solve(self):
        """Solve the initialized sparse matrix using the DancingLinks algorithm.

        Parameters
        ----------
        self: the initialized DancingLinks solver instance

        Returns
        -------
        The set of rows that satisfy all the required constraints
        """
        if self._backtrack():
            return self.solution
        else:
            return []

    def _backtrack(self):
        # All constraints covered == solved
        if self.smat.ghead.right == self.smat.ghead:
            return True

        # Choose the column with the minimum number of 1s (Knuth's S-heuristic)
        best_col = None
        min_size = float('inf')
        curr = self.smat.ghead.right
        while curr != self.smat.ghead:
            if curr.size < min_size:
                min_size = curr.size
                best_col = curr
                if min_size <= 1:
                    break
            curr = curr.right

        if min_size == 0 or best_col is None:
            return False

        col = best_col
        self._cover(col)

        row_in_col = col.down
        while row_in_col != col:
            row_cell = row_in_col.right
            while row_cell != row_in_col:
                self._cover(row_cell.head)
                row_cell = row_cell.right

            if self._backtrack():
                self.solution.append(row_in_col)
                return True

            row_cell = row_in_col.left
            while row_cell != row_in_col:
                self._uncover(row_cell.head)
                row_cell = row_cell.left

            row_in_col = row_in_col.down

        self._uncover(col)
        return False


class DlxTest(unittest.TestCase):
    def setUp(self):
        self.mat = [
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 0, 1]]
        self.dlx = DancingLinks(self.mat)

    def test_dancinglinks_canSolveExactCoverProbs(self):
        soln = self.dlx.solve()
        e = []
        for node in soln:
            e.append(node.row_idx)
        self.assertEqual({1, 5, 3}, set(e))


if __name__ == '__main__':
    unittest.main()
