class Board:
    def __init__(self, board=None, scale=10, subset=False):
        self.issubset = subset
        if not board:
            self._board = [[0 for i in range(scale)] for j in range(scale)]
            self.size = (scale, scale)
        else:
            self._board = board
            try:
                self.size = (len(board[0]), len(board))
            except TypeError:
                self.size = (len(board), 1)
        if not subset:
            self._pattern_cache = self._init_pattern()
    
    def pattern(self, t):
        if self.issubset:
            raise ValueError("Trying to get patterns on a subset!")
        else:
            return self._pattern_cache[str(t)]  # Example: 5 -> '5'
    
    def _update_pattern(self):
        raise NotImplementedError()
        
    def _init_pattern(self):
        pattern_cache = dict()
        scale = self.size[0]
        # RENJU
        for n in [4, 5, 6]:
            pattern_cache[str(n)] = list()
            range_dict = {'v': (range(scale), range(scale - (n - 1))),
                    'h': (range(scale - (n - 1)), range(scale)),
                    'rd': (range(scale - (n - 1)), range(scale - (n - 1))),
                    'ld': (range(n - 1, scale - (n - 1)), range(scale - (n - 1)))}
            for direction in ['v', 'h', 'rd', 'ld']:
                pattern_cache[str(n)] += [[0 for _ in range(n)] for _ in range_dict[direction][0] for _ in range_dict[direction][1]]
        # 3 x 5
        return pattern_cache
    
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
            return Board(subset, subset=True)
        else:
            return self._board[x][y]
    
    def __setitem__(self, indices, value):
        y, x = indices
        if isinstance(x, slice) or isinstance(y, slice):
            raise ValueError("Trying to assign multiple values to the board!")
        self._board[x][y] = value
        # self._update_pattern()
    
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
