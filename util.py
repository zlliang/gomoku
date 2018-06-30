from collections import defaultdict as ddict

score = {
    'ONE': 10,
    'TWO': 100,
    'THREE': 1000,
    'FOUR': 100000,
    'FIVE': 10000000,
    'BLOCKED_ONE': 1,
    'BLOCKED_TWO': 10,
    'BLOCKED_THREE': 100,
    'BLOCKED_FOUR': 10000
}

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
        self.score_cache = {
            1: {
                'h': ddict(lambda: 0.0),
                'v': ddict(lambda: 0.0),
                'r': ddict(lambda: 0.0),
                'l': ddict(lambda: 0.0)
            },
            2: {
                'h': ddict(lambda: 0.0),
                'v': ddict(lambda: 0.0),
                'r': ddict(lambda: 0.0),
                'l': ddict(lambda: 0.0)
            }
        }
        self.score_1 = ddict(lambda: 0.0)
        self.score_2 = ddict(lambda: 0.0)
        self._init_score()
    
    def evaluate(self, role=1):
        max_score_1 = 0
        max_score_2 = 0
        for i in self.xrange:
            for j in self.yrange:
                if self[i, j] == 1:
                    max_score_1 = max(self.score_1[(i, j)], max_score_1)
                elif self[i, j] == 2:
                    max_score_2 = max(self.score_2[(i, j)], max_score_2)
        mult = 1 if role == 1 else -1
        result = mult * (max_score_1 - max_score_2)
        return result
    
    def _init_score(self):
        for i in self.xrange:
            for j in self.yrange:
                if self[i, j] == 0:
                    if self._has_neighbor(i, j):
                        self.score_1[(i, j)] = self._get_point_score(i, j, 1)
                        self.score_2[(i, j)] = self._get_point_score(i, j, 2)
                elif self[i, j] == 1:
                    self.score_1[(i, j)] = self._get_point_score(i, j, 1)
                elif self[i, j] == 2:
                    self.score_2[(i, j)] = self._get_point_score(i, j, 2)
    
    def _update_score(self, x, y, radius=6):
        
        scale = self.size[0]
        # h
        for i in range(-radius, radius):
            xi = x + i
            yi = y
            if xi < 0:
                continue
            if xi >= scale:
                break
            self._update_score_sub(xi, yi, 'h')
        
        # v
        for i in range(-radius, radius):
            xi = x
            yi = y + i
            if yi < 0:
                continue
            if yi >= scale:
                break
            self._update_score_sub(xi, yi, 'v')

        # r
        for i in range(-radius, radius):
            xi = x + i
            yi = y + i
            if xi < 0 or yi < 0:
                continue
            if xi >= scale or yi >= scale:
                break
            self._update_score_sub(xi, yi, 'r')
        
        # l
        for i in range(-radius, radius):
            xi = x + i
            yi = y - i
            if xi < 0 or yi < 0:
                continue
            if xi >= scale or yi >= scale:
                break
            self._update_score_sub(xi, yi, 'l')
    
    def _update_score_sub(self, x, y, direction):
        role = self[x, y]
        if role == 0 or role == 1:
            self.score_1[(x, y)] = self._get_point_score(x, y, 1, direction)
        else:
            self.score_1[(x, y)] = 0
        
        if role == 0 or role == 2:
            self.score_2[(x, y)] = self._get_point_score(x, y, 2, direction)
        else:
            self.score_2[(x, y)] = 0
                    

    def candidate(self):
        point_score = {}
        if self.step_count == 0:
            return [(int(self.size[0] / 2), int(self.size[1] / 2))]
        for x in self.xrange:
            for y in self.yrange:
                if self._has_neighbor(x, y):
                    score = self._get_point_score(x, y, 1)
                    if score > 3:
                        return [(x, y)]
                    else:
                        point_score[(x, y)] = score
        scores = sorted(list(point_score.items()), key=lambda x: x[1], reverse=True)
        print(scores)
        candidate = [i[0] for i in scores]
        return candidate


    # def _get_point_score(self, x, y):
    #     directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    #     max_count = 0
    #     for dir in directions:
    #         dx, dy = dir
    #         if self._board[x + dx][y + dy] == 0:
    #             continue
    #         else:
    #             neighbor_type = self._board[x + dx][y + dy]
    #         blocked = False
    #         count = 1
    #         while not blocked:
    #             if self._out_of_boards(x + count * dx, y + count * dy):
    #                 break
    #             elif self._board[x + count * dx][y + count * dy] == neighbor_type:
    #                 count += 1
    #             elif self._board[x + count * dx][y + count * dy] == 0:  # 活X的情况
    #                 count += 0.5
    #                 blocked = True
    #             else:
    #                 blocked = True
    #         max_count = max(max_count, count-1)
    #     return max_count

    def _out_of_boards(self, x, y):
        return (x < 0 or x >= self.size[0]) and (y < 0 or y >= self.size[1])

    def _has_neighbor(self, x, y, dist=1):
        for i in range(max(x - dist, 0), min(x + dist + 1, self.size[0])):
            for j in range(max(y - dist, 0), min(y + dist + 1, self.size[1])):
                if not (i == x and j == y) and self[i, j]:
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
        self._update_score(y, x)

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

    def _get_point_score(self, x, y, role, direction=None):
        result = 0
        count = 0
        block = 0
        second_count = 0
        scale = self.size[0]
        
        # horizental
        if direction == None or direction == 'h':
            count = 1
            block = 0
            empty = -1
            second_count = 0
            i = x
            while True:
                i += 1
                if i >= scale:
                    block += 1
                    break
                t = self[i, y]
                if t == 0:
                    if empty == -1 and i < scale-1 and self[i+1, y] == role:
                        empty = count
                        continue
                    else:
                        break
                if t == role:
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = x
            while True:
                i -= 1
                if i < 0:
                    block += 1
                    break
                t = self[i, y]
                if t == 0:
                    if empty == -1 and i > 0 and self[i-1, y] == role:
                        empty = 0
                        continue
                    else:
                        break
                if t == role:
                    second_count += 1
                    if empty != -1 and empty:
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += second_count
            self.score_cache[role]['h'][(x, y)] = self._count_to_score(count, block, empty)
            result += self.score_cache[role]['h'][(x, y)]

        # vertical
        if direction == None or direction == 'v':
            count = 1
            block = 0
            empty = -1
            second_count = 0
            i = y
            while True:
                i += 1
                if i >= scale:
                    block += 1
                    break
                t = self[x, i]
                if t == 0:
                    if empty == -1 and i < scale-1 and self[x, i+1] == role:
                        empty = count
                        continue
                    else:
                        break
                if t == role:
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = y
            while True:
                i -= 1
                if i < 0:
                    block += 1
                    break
                t = self[x, i]
                if t == 0:
                    if empty == -1 and i > 0 and self[x, i-1] == role:
                        empty = 0
                        continue
                    else:
                        break
                if t == role:
                    second_count += 1
                    if empty != -1 and empty:
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += second_count
            self.score_cache[role]['v'][(x, y)] = self._count_to_score(count, block, empty)
            result += self.score_cache[role]['v'][(x, y)]

        # r
        if direction == None or direction == 'r':
            count = 1
            block = 0
            empty = -1
            second_count = 0
            i = 0
            while True:
                i += 1
                xi = x + i
                yi = y + i
                if xi >= scale or yi >= scale:
                    block += 1
                    break
                t = self[xi, yi]
                if t == 0:
                    if empty == -1 and xi < scale-1 and yi < scale-1 and self[xi+1, yi+1] == role:
                        empty = count
                        continue
                    else:
                        break
                if t == role:
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = 0
            while True:
                i += 1
                xi = x - i
                yi = x - i
                if xi < 0 or yi < 0:
                    block += 1
                    break
                t = self[xi, yi]
                if t == 0:
                    if empty == -1 and xi > 0 and yi > 0 and self[xi-1, yi-1] == role:
                        empty = 0
                        continue
                    else:
                        break
                if t == role:
                    second_count += 1
                    if empty != -1 and empty:
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += second_count
            self.score_cache[role]['r'][(x, y)] = self._count_to_score(count, block, empty)
            result += self.score_cache[role]['r'][(x, y)]

        # l
        if direction == None or direction == 'l':
            count = 1
            block = 0
            empty = -1
            second_count = 0
            i = 0
            while True:
                i += 1
                xi = x + i
                yi = y - i
                if xi < 0 or yi < 0 or xi >= scale or yi >= scale:
                    block += 1
                    break
                t = self[xi, yi]
                if t == 0:
                    if empty == -1 and xi < scale-1 and yi > 0 and self[xi+1, yi-1] == role:
                        empty = count
                        continue
                    else:
                        break
                if t == role:
                    count += 1
                    continue
                else:
                    block += 1
                    break
            i = 0
            while True:
                i += 1
                xi = x - i
                yi = x + i
                if xi < 0 or yi < 0 or xi >= scale or yi >= scale:
                    block += 1
                    break
                t = self[xi, yi]
                if t == 0:
                    if empty == -1 and xi > 0 and yi < scale-1 and self[xi-1, yi+1] == role:
                        empty = 0
                        continue
                    else:
                        break
                if t == role:
                    second_count += 1
                    if empty != -1 and empty:
                        empty += 1
                    continue
                else:
                    block += 1
                    break
            count += second_count
            self.score_cache[role]['r'][(x, y)] = self._count_to_score(count, block, empty)
            result += self.score_cache[role]['r'][(x, y)]
        
        return result

    def _count_to_score(self, count, block, empty):
        if not empty:
            empty = 0
        if empty <= 0:
            if count >= 5:
                return score['FIVE']
            if block == 0:
                switcher = {1: score['ONE'], 2: score['TWO'], 3: score['THREE'], 4: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 1:
                switcher = {1: score['BLOCKED_ONE'], 2: score['BLOCKED_TWO'], 3: score['BLOCKED_THREE'], 4: score['BLOCKED_FOUR']}
                if count in switcher:
                    return switcher[count]
        elif empty == 1 or empty == count-1:
            if count >= 6:
                return score['FIVE']
            if block == 0:
                switcher = {2: score['TWO']/2, 3: score['THREE'], 4: score['BLOCKED_FOUR'], 5: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 1:
                switcher = {2: score['BLOCKED_TWO'], 3: score['BLOCKED_THREE'], 4: score['BLOCKED_FOUR'], 5: score['BLOCKED_FOUR']}
                if count in switcher:
                    return switcher[count]
        elif empty == 2 or empty == count-2:
            if count >= 7:
                return score['FIVE']
            if block == 0:
                switcher = {3: score['THREE'], 4: 0, 5: score['BLOCKED_FOUR'], 6: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 1:
                switcher = {3: score['BLOCKED_THREE'], 4: score['BLOCKED_FOUR'], 5: score['BLOCKED_FOUR'], 6: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 2:
                switcher = {4: 0, 5: 0, 6: score['BLOCKED_FOUR']}
                if count in switcher:
                    return switcher[count]
        elif empty == 3 or empty == count-3:
            if count >= 8:
                return score['FIVE']
            if block == 0:
                switcher = {4: 0, 5: score['THREE'], 6: score['BLOCKED_FOUR'], 7: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 1:
                switcher = {4: 0, 5: 0, 6: score['BLOCKED_FOUR'], 7: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 2:
                switcher = {4: 0, 5: 0, 6: 0, 7: score['BLOCKED_FOUR']}
                if count in switcher:
                    return switcher[count]
        elif empty == 4 or empty == count-4:
            if count >= 9:
                return score['FIVE']
            if block == 0:
                switcher = {5: 0, 6: 0, 7: 0, 8: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 1:
                switcher = {4: 0, 5: 0, 6: 0, 7: score['BLOCKED_FOUR'], 8: score['FOUR']}
                if count in switcher:
                    return switcher[count]
            if block == 2:
                switcher = {5: 0, 6: 0, 7: 0, 8: score['BLOCKED_FOUR']}
                if count in switcher:
                    return switcher[count]
        elif empty == 5 or empty == count-5:
            return score['FIVE']
        
        return 0
