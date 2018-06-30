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
        self.xrange = range(self.size[0])
        self.yrange = range(self.size[1])
        self.step_count = 0

    def candidate(self):
        point_score = {}
        if self.step_count == 0:
            return [(int(self.size[0] / 2), int(self.size[1] / 2))]
        for x in self.xrange:
            for y in self.yrange:
                if self._has_neighbor(x, y):
                    score = self._get_point_score(x, y)
                    if score > 3:
                        return [(x, y)]
                    else:
                        point_score[(x, y)] = score
        scores = sorted(list(point_score.items()), key=lambda x: x[1], reverse=True)
        candidate = [i[0] for i in scores]
        return candidate

    def _get_point_score(self, x, y):
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        max_count = 0
        for dir in directions:
            dx, dy = dir
            if self._board[x + dx][y + dy] == 0:
                continue
            else:
                neighbor_type = self._board[x + dx][y + dy]
            blocked = False
            count = 1
            while not blocked:
                if self._out_of_boards(x + count * dx, y + count * dy):
                    break
                elif self._board[x + count * dx][y + count * dy] == neighbor_type:
                    count += 1
                elif self._board[x + count * dx][y + count * dy] == 0:  # 活X的情况
                    count += 0.5
                    blocked = True
                else:
                    blocked = True
            max_count = max(max_count, count-1)
        return max_count

    def _out_of_boards(self, x, y):
        return (x < 0 or x >= self.size[0]) and (y < 0 or y >= self.size[1])

    def _has_neighbor(self, x, y, dist=1):
        for i in range(max(x - dist, 0), min(x + dist + 1, self.size[0])):
            for j in range(max(y - dist, 0), min(y + dist + 1, self.size[1])):
                if not (i == x and j == y) and self._board[i][j]:
                    return True
        return False

    def __getitem__(self, indices):
        if self.size[1] == 1:  # Only one row, a flat list
            return self._board[indices]
        else:
            y, x = indices
            if not isinstance(x, slice):  # Scalar
                return self._board[x][y]
            else:
                return [row[y] for row in self._board[x]]
    
    def __setitem__(self, indices, value):
        y, x = indices
        if isinstance(x, slice) or isinstance(y, slice):
            raise ValueError("Trying to assign multiple values to the board!")
        self._board[x][y] = value
        if value == 0:
            self.step_count -= 1
        else:
            self.step_count += 1

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
