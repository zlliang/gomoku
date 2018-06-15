class Board:
    def __init__(self, board=None):
        self.board = None
        self._pattern_cache = None
    
    def __getitem__(self, indices):
        x, y = indices
        return self.board[x][y]
    
    def pattern(self):
        raise NotImplementedError("Pattern getter has not been implemented!")
