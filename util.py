class Board:
    """Board representation for Gomoku
    
    This class mainly intends to represent current situation of a Gomoku board
    and extract local patterns.

    Parameters
    ----------
    board: Matrix-like list (X x Y), like following, default is all-zero board
              X 0  1  2
          Y 0 [[0, 1, 2],
            1  [1, 2, 2],
            2  [1, 1, 1]]
    scale: size of the board (n x n), default is 20

    Usage
    -----
    To initialize a board, just construct it:
        >>> b = Board(scale=6)
    Then you can slice it like a NumPy array:
        >>> b[3:5, 2:4]
        >>> b[2, 2] = 1
    The main usage is get local patterns. Call `pattern` and you can get all
    n-triples or nxm-subsets:
        >>> b.pattern('5')
        >>> b.pattern('3x5')
    """
    
    def __init__(self, board=None, scale=20):
        if not board:
            self._board = [[0 for i in range(scale)] for j in range(scale)]
            self.size = (scale, scale)
        else:
            self._board = board
            try:
                self.size = (len(board[0]), len(board))
            except TypeError:  # Only one row, a flat list
                self.size = (len(board), 1)
        # Initialize ranges
        self._x_min = int(scale/2)
        self._x_max = int(scale/2)
        self._y_min = int(scale/2)
        self._y_max = int(scale/2)
        self.xrange = range(self._x_min-1, self._x_max+1)
        self.yrange = range(self._y_min-1, self._y_max+1)
    
    def pattern(self, t):
        """Get local patterns of a board

        Parameters
        ----------
        type: The pattern type you want to get
              If 'n', you will get all n-triples of horizental, vertical, left
              and right diagonal
              If 'nxm', you will get all nxm-subset in the board
        
        Returns
        -------
        patterns: An iterable generator, in which all subset are instances of 
                  this class `Board`
        """
        nx, ny = self.size
        if str(t).isdigit():  # 'n' <-> n-triples
            t = int(t)
            for x in range(nx):
                for y in range(ny-t+1):
                    yield Board([self[x, y+i] for i in range(t)])  # V
            for x in range(nx-t+1):
                for y in range(ny):
                    yield self[x:x+t, y]  # H
            for x in range(nx-t+1):
                for y in range(ny-t+1):
                    yield Board([self[x+i, y+i] for i in range(t)])  # RD
            for x in range(t-1, nx):
                for y in range(ny-t+1):
                    yield Board([self[x-i, y+i] for i in range(t)])  # LD
        elif 'x' in t:  # 'nxm' -> [n, m]-subsets
            sx, sy = map(int, t.split('x'))
            for x in range(nx-sx+1):
                for y in range(ny-sy+1):
                    yield self[x:x+sx, y:y+sy]
        else:
            raise ValueError("Not an appropriate parameter for pattern query!")
    
    def __getitem__(self, indices):
        if self.size[1] == 1:  # Only one row, a flat list
            return self._board[indices]
        else:
            y, x = indices
            if not isinstance(x, slice) and not isinstance(y, slice):  # Scalar
                return self._board[x][y]
            if isinstance(y, slice):
                subset = [row[y] for row in self._board]
            else:
                subset = [[row[y]] for row in self._board]
            subset = subset[x]
            return Board(subset)
    
    def __setitem__(self, indices, value):
        y, x = indices
        if isinstance(x, slice) or isinstance(y, slice):
            raise ValueError("Trying to assign multiple values to the board!")
        self._board[x][y] = value
        # Update ranges
        self._x_min = min(self._x_min, x)
        self._x_max = max(self._x_max, x)
        self._y_min = min(self._y_min, y)
        self._y_max = max(self._y_max, y)
        self.xrange = range(self._x_min-1, self._x_max+1)
        self.yrange = range(self._y_min-1, self._y_max+1)
    
    def __eq__(self, obj):
        if type(self) == type(obj):
            return self._board == obj._board
        else:
            return self._board == obj
    
    def __repr__(self):
        if isinstance(self._board[0], list):
            l = [str(row) for row in self._board]
            return '\n'.join(l)
        else:
            return str(self._board)
