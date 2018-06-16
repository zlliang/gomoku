class Board:
    def __init__(self, scale=10):
        self._board = [[0 for i in range(scale)] for j in range(scale)]
        self._pattern_cache = self._init_pattern()
    
    def pattern(self):
        raise NotImplementedError("Pattern getter has not been implemented!")
    
    def _update_pattern(self):
        raise NotImplementedError()
    
    def _init_pattern(self):
        raise NotImplementedError()
    
    def __getitem__(self, indices):
        x, y = indices
        return self._board[x][y]
    
    def __setitem__(self, indices, value):
        x, y = indices
        self._board[x][y] = value
        self._update_pattern()
    
    def __repr__(self):
        raise NotImplementedError()
