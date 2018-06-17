class Board:
    def __init__(self, board=None, scale=10):
        if not board:
            self._board = [[0 for i in range(scale)] for j in range(scale)]
            self.size = (scale, scale)
        else:
            self._board = board
            try:
                self.size = (len(board[0]), len(board))
            except TypeError:
                self.size = (len(board), 1)
    
    def pattern(self, t):
        nx, ny = self.size
        if str(t).isdigit():  # '5' <-> 5
            t = int(t)
            # Vertically
            for x in range(nx):
                for y in range(ny-t+1):
                    yield self[x, y:y+t]
            for x in range(nx-t+1):
                for y in range(ny):
                    yield self[x:x+t, y]  # Horizentally  
            for x in range(nx-t+1):
                for y in range(nx-t+1):
                    yield Board([self[x+i, y+i] for i in range(t)])
            for x in range(t-1, nx):
                for y in range(ny-t+1):
                    yield Board([self[x-i, y+i] for i in range(t)])
        elif 'x' in t:
            sx, sy = list(map(int, t.split('x')))  # '3x5' -> [3, 5]
            for x in range(nx-sx+1):
                for y in range(ny-sy+1):
                    yield self[x:x+sx, y:y+sy]
        else:
            raise ValueError("Not an appropriate parameter for pattern query!")
    
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
