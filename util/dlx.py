__all__ = [ 'DancingLinks', 'LeftIterator' ]

class Head:
  '''
  Column header class.

  Used to access elements within a column.
  '''
  def __init__(self, col_idx):
    self.col_idx = col_idx
    self.left, self.right = None, None

  def remove_from_row(self):
    '''
    Remove the column header node from the special column header row.
    '''
    self.left.right = self.right
    self.right.left = self.left

  def readd_to_row(self):
    '''
    Re-add the column header node to the special column header row.
    '''
    self.left.right = self.right.left = self

class Node:
  '''
  Node class that represents, through its existence, a binary value (i.e. 1)

  This is a node that is only ever supposed to be a part of a sparse binary matrix. It can
  access elements in all 4 directions: `up`, `down`, `left`, `right`.
  '''
  def __init__(self, row_idx, col_idx):
    self.row_idx = row_idx
    self.col_idx = col_idx
    self.up, self.down = None, None

  def remove_from_column(self):
    '''
    Remove a particular row element from a column.
    '''
    self.up.down = self.down
    self.down.up = self.up

  def readd_to_column(self):
    '''
    Re-add a particular row element to a column.
    '''
    self.up.down = self.down.up = self


class NodeIterator:
  '''
  Iterate through nodes in a particular direction
  '''
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
  '''
  Sparse boolean matrix

  A fully interconnected set of nodes in a sparse matrix. The existence of a node
  represents a value of `1` in a particular row & column position.
  '''
  def __init__(self, mat):
    '''Converts a fully specified matrix to its sparse form.

    Parameters
    ----------
    self: The sparse matrix instance
    mat: A bool[][] denoting a fully specified matrix

    Returns
    -------
    A sparse matrix version of the provided fully specified matrix.
    '''
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
    '''Iterate through the rows and add left-right links for each item in the row.

    Parameters
    ----------
    self: the sparse matrix
    srows: a Node[][], where each item denotes a particular row, and each element in that item denotes
      an element in the matrix

    Returns
    -------
    None. Purely mutates internal state.
    '''
    for srow in srows:
      n = len(srow)
      for j in range(n):
        srow[j].right = srow[(j + 1) % n]
        srow[j].left = srow[(j - 1 + n) % n]

  def create_ud_links(self, scols):
    '''Iterate through the columns and add up-down links for each item in the column.
    In addition it also adds a reference to the header node.

    Parameters
    ----------
    self: the sparse matrix
    scols: a Node[][], where each item denotes a particular column, and each element in that item denotes
      an element in the matrix

    Returns
    -------
    None. Purely mutates internal state.
    '''
    for scol in scols:
      n = len(scol)
      for j in range(n):
        scol[j].down = scol[(j + 1) % n]
        scol[j].up = scol[(j - 1 + n) % n]
        scol[j].head = scol[0]


class DancingLinks:
  '''
  A class that implements the Dancing Links per Knuth's DLX paper.
  '''

  def __init__(self, mat):
    '''Initializes the solver based on the provided matrix.
    Columns in the matrix represent constraints, rows represent choices that satisfy a given constraint.

    Parameters
    ----------
    self: the DancingLinks solver
    mat: An exact-cover matrix with columns representing constraints and rows representing choices.

    Returns
    -------
    The initialized solver instance.
    '''
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
    for rowInCol in DownIterator(col):
      for rowCell in RightIterator(rowInCol):
        rowCell.remove_from_column()

  def _uncover(self, col):
    '''Uncovers a particular column.

    Re-adds a column to the column header row, after re-adding all rows that satisfy
    said column.

    Parameters
    ----------
    self: the DancingLinks solver instance
    col: The column to be uncovered.

    Returns
    -------
    None. Purely mutates internal state.
    '''
    for rowInCol in UpIterator(col):
      for rowCell in LeftIterator(rowInCol):
        rowCell.readd_to_column()
    col.readd_to_row()

  def solve(self):
    '''Solve the initialized sparse matrix using the DancingLinks algorithm.

    Parameters
    ----------
    self: the initialized DancingLinks solver instance

    Returns
    -------
    The set of rows that satisfy all the required constraints
    '''
    if (self._backtrack()):
      return self.solution
    else:
      return []

  def _backtrack(self):

    # Select the first possible constrain to satisfy
    col = self.smat.ghead.right

    # No constraints left == solved
    if (col == self.smat.ghead):
      return True

    # No rows left that fulfill this constraint == unsolvable, backtrack!
    if (col.down == col):
      return False

    # Remove the column from the column header list
    #
    # Remove all rows in the column, and keep them aside. These are the
    # possible solutions to the constraint.
    #
    # The row-nodes in `col` are still accessible through `col.down`. Nodes
    # to the left and right of them are still accessible through `row.left`
    # and `row.right` etc. However, `row.left` and `row.right` will not be
    # accessible through `row.left.head.up/down`.
    #
    # In plain english, while row-nodes in `col` are still accessible, and
    # through these row-nodes, so too is the rest of the row; and while it
    # is possible to reach the corresponding column via `row-node.head`;
    # it is not possible to reach these nodes by traversing down the
    # corresponding column.
    self._cover(col)

    # select a row as a potential solution
    # remember, all other competing solutions have already been set aside
    for rowInCol in DownIterator(col):

      # this row satisfies more than just `col`, it also satisfies other
      # constraints. this basically means that those columns can be
      # removed/covered as well, since this solution already satisfies
      # them.
      #
      # in addition to removing the fortuitously satisfied column,
      # `self#cover` also removes all the other rows that also satisfy
      # the the same constraint. this is because, for an exact cover
      # problem, each constraint can only be satisfied once.
      #
      # Note 1: `rowInCol` is not removed in this step, since it was
      # already removed in `self.cover(col)` earlier. This removes all
      # other rows rendered redundant by rowInCol.
      #
      # Note 2: the removed rows are technically accessible by
      # `rowCell.up/down` and then traversing left/right. However, this
      # is irrelevant. We are simply looking at the reduced matrix, and
      # aren't actually going to ever traverse in this manner.
      # For all intents and purposes, those rows are removed.
      for rowCell in RightIterator(rowInCol):
        self._cover(rowCell.head)

      # Is the reduced matrix solvable if `rowInCol` is selected as a
      # potential solution?
      if self._backtrack():
        # if so, `rowInCol` is one of the rows that is a part of the
        # exact-cover solution
        self.solution.append(rowInCol)
        return True

      # This row cannot be a part of a potential solution.
      #
      # Add back all the rows that were deleted as conflicting with the
      # selected row. Add back all of the additional constraints that
      # were solved by the selected row.
      for rowCell in LeftIterator(rowInCol):
        self._uncover(rowCell.head)

      # Go to the next possible row (rinse and repeat for all possible
      # rows)
      continue

    # Choosing to satisfy this column and going through all possible rows
    # did not lead to a single solution. This problem/subproblem is
    # unsolvable.
    #
    # Add back the column, and return False to indicate that a solution
    # wasn't found
    #
    # Note: in the case that we were dealing with the actual overall
    # problem, we wouldn't need to add the column back, however, since
    # we're actually recursing, we might actually be in a subproblem, and a
    # different path may end up being chosen. In this case we need to set
    # the matrix back to the way it looked to start with.
    self._uncover(col)
    return False


if __name__ == '__main__':
  mat = [
    [1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 1]]
  q = DancingLinks(mat)
  a = q.solve()
  e = []
  for node in a:
    e.append(node.row_idx)
  assert set(e) == {1, 5, 3}
