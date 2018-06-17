class Board:
    def __init__(self, board=None, scale=10):
        if not board:
            self._board = [[0 for i in range(scale)] for j in range(scale)]
        else:
            self._board = board
    #     self._pattern_cache = self._init_pattern()
    
    # def pattern(self):
    #     raise NotImplementedError("Pattern getter has not been implemented!")
    
    # def _update_pattern(self):
    #     raise NotImplementedError()
    
    # def _init_pattern(self):
    #     raise NotImplementedError()
    
    def __getitem__(self, indices):
        y, x = indices
        if not isinstance(x, slice) and not isinstance(y, slice):
            return self._board[x][y]
        if isinstance(y, slice):
            subset = [row[y] for row in self._board]
        else:
            subset = [[row[y]] for row in self._board]
        subset = subset[x]
        if isinstance(subset, list):
            return Board(subset)
        else:
            return self._board[x][y]
    
    def __setitem__(self, indices, value):
        y, x = indices
        if isinstance(x, slice) or isinstance(y, slice):
            raise ValueError("Trying to assign multiple values to the board!")
        self._board[x][y] = value
        # self._update_pattern()
    
    def __repr__(self):
        if isinstance(self._board[0], list):
            l = [str(row) for row in self._board]
            return '\n'.join(l)
        else:
            return str(self._board)
