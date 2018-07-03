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

switcher = (
    {1: score['ONE'], 2: score['TWO'], 3: score['THREE'], 4: score['FOUR']},
    {1: score['BLOCKED_ONE'], 2: score['BLOCKED_TWO'], 3: score['BLOCKED_THREE'], 4: score['BLOCKED_FOUR']},
    {2: score['TWO'] / 2, 3: score['THREE'], 4: score['BLOCKED_FOUR'], 5: score['FOUR']},
    {2: score['BLOCKED_TWO'], 3: score['BLOCKED_THREE'], 4: score['BLOCKED_FOUR'], 5: score['BLOCKED_FOUR']},
    {3: score['THREE'], 4: 0, 5: score['BLOCKED_FOUR'], 6: score['FOUR']},
    {3: score['BLOCKED_THREE'], 4: score['BLOCKED_FOUR'], 5: score['BLOCKED_FOUR'], 6: score['FOUR']},
    {4: 0, 5: 0, 6: score['BLOCKED_FOUR']},
    {4: 0, 5: score['THREE'], 6: score['BLOCKED_FOUR'], 7: score['FOUR']},
    {4: 0, 5: 0, 6: score['BLOCKED_FOUR'], 7: score['FOUR']},
    {4: 0, 5: 0, 6: 0, 7: score['BLOCKED_FOUR']},
    {5: 0, 6: 0, 7: 0, 8: score['FOUR']},
    {4: 0, 5: 0, 6: 0, 7: score['BLOCKED_FOUR'], 8: score['FOUR']},
    {5: 0, 6: 0, 7: 0, 8: score['BLOCKED_FOUR']}
)



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
            self.step_count = 0
        else:
            self._board = board
            try:
                self.size = (len(board[0]), len(board))
            except TypeError:  # Only one row, a flat list
                self.size = (len(board), 1)
            self.step_count = 0
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self[i, j] != 0:
                        self.step_count += 1
        self.xrange = range(self.size[0])
        self.yrange = range(self.size[1])
        self.score_1 = ddict(lambda: 0.0)
        self.score_2 = ddict(lambda: 0.0)
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
        self._init_score()

    def evaluate(self, role=1):
        max_score_1 = 0
        max_score_2 = 0
        for i in self.xrange:
            for j in self.yrange:
                if self[i, j] == 1:
                    max_score_1 += self._fix_evaluation(self.score_1[(i, j)], i, j, 1)
                    # max_score_1 = max(self.score_1[(i, j)], max_score_1)
                elif self[i, j] == 2:
                    max_score_2 += self._fix_evaluation(self.score_2[(i, j)], i, j, 2)
                    # max_score_2 = max(self.score_2[(i, j)], max_score_2)
        
        # max_score_1 = self._fix_evaluation(max_score_1)
        # max_score_2 = self._fix_evaluation(max_score_2)
        mult = 1 if role == 1 else -1
        result = mult * (max_score_1 - max_score_2)
        return result

    def _init_score(self):
        for i in self.xrange:
            for j in self.yrange:
                if self[i, j] == 0:
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
            if xi < 0 or yi >= scale:
                continue
            if xi >= scale or yi < 0:
                break
            self._update_score_sub(xi, yi, 'l')
        
        self._update_score_sub(x, y, None)
        

    def _update_score_sub(self, x, y, direction):
        role = self[x, y]
        if role == 0 or role == 1:
            if direction:
                self.score_1[(x, y)] -= self.score_cache[1][direction][(x, y)]
                self.score_1[(x, y)] += self._get_point_score(x, y, 1, direction)
            else:
                self.score_1[(x, y)] = self._get_point_score(x, y, 1)
        else:
            self.score_1[(x, y)] = 0

        if role == 0 or role == 2:
            if direction:
                self.score_2[(x, y)] -= self.score_cache[2][direction][(x, y)]
                self.score_2[(x, y)] += self._get_point_score(x, y, 2, direction)
            else:
                self.score_2[(x, y)] = self._get_point_score(x, y, 2)
        else:
            self.score_2[(x, y)] = 0

    def candidate(self):
        fives = list()
        fours = list()
        point_scores = list()
        if self.step_count == 0:
            return [(int(self.size[0] / 2), int(self.size[1] / 2))]
        for x in self.xrange:
            for y in self.yrange:
                if self._has_neighbor(x, y) and self[x, y] == 0:
                    score_1 = self.score_1[(x, y)]
                    score_2 = self.score_2[(x, y)]
                    # print((x, y), score_hum, score_com)
                    if self._is_five(x, y, 1):
                        return [(x, y)]
                    elif self._is_five(x, y, 2):
                        fives.append((x, y))
                    elif score_1 >= score['FOUR']:
                        fours.insert(0, (x, y))
                    elif score_2 >= score['FOUR']:
                        fours.append((x, y))
                    else:
                        point_scores.append((x, y))
        # If forced moves exist, return them
        if fives:
            return [fives[0]]
        if fours:
            return fours
        # If no forced move, sort all candidate with scores
        candidate = sorted(point_scores, key=lambda p: max(self.score_1[p], self.score_2[p]), reverse=True)
        # scores = sorted(list(point_scores.items()), key=lambda x: x[1], reverse=True)
        # candidate = [i[0] for i in scores]
        return candidate

    def _has_neighbor(self, x, y, dist=1):
        for i in range(max(x - dist, 0), min(x + dist + 1, self.size[0])):
            for j in range(max(y - dist, 0), min(y + dist + 1, self.size[1])):
                if not (i == x and j == y) and self[i, j]:
                    return True
        return False

    def __getitem__(self, indices):
        y, x = indices
        if not isinstance(x, slice):  # Scalar
            return self._board[x][y]
        else:
            return [row[y] for row in self._board[x]]

    def __setitem__(self, indices, value):
        y, x = indices
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
                    if empty == -1 and i < scale - 1 and self[i + 1, y] == role:
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
                    if empty == -1 and i > 0 and self[i - 1, y] == role:
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
            v = self._count_to_score(count, block, empty, x, y, role)
            self.score_cache[role]['h'][(x, y)] = v
            result += v

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
                    if empty == -1 and i < scale - 1 and self[x, i + 1] == role:
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
                    if empty == -1 and i > 0 and self[x, i - 1] == role:
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
            v = self._count_to_score(count, block, empty, x, y, role)
            self.score_cache[role]['v'][(x, y)] = v
            result += v

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
                    if empty == -1 and xi < scale - 1 and yi < scale - 1 and self[xi + 1, yi + 1] == role:
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
                yi = y - i
                if xi < 0 or yi < 0:
                    block += 1
                    break
                t = self[xi, yi]
                if t == 0:
                    if empty == -1 and xi > 0 and yi > 0 and self[xi - 1, yi - 1] == role:
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
            v = self._count_to_score(count, block, empty, x, y, role)
            self.score_cache[role]['r'][(x, y)] = v
            result += v

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
                    if empty == -1 and xi < scale - 1 and yi > 0 and self[xi + 1, yi - 1] == role:
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
                yi = y + i
                if xi < 0 or yi < 0 or xi >= scale or yi >= scale:
                    block += 1
                    break
                t = self[xi, yi]
                if t == 0:
                    if empty == -1 and xi > 0 and yi < scale - 1 and self[xi - 1, yi + 1] == role:
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
            v = self._count_to_score(count, block, empty, x, y, role)
            self.score_cache[role]['l'][(x, y)] = v
            result += v
        
        return result

    def _count_to_score(self, count, block, empty, x, y, role):
        if not empty:
            empty = 0
        if empty <= 0:
            if count >= 5:
                return score['FIVE']
            if block == 0 and count in switcher[0]:
                return switcher[0][count]
            if block == 1 and count in switcher[1]:
                return switcher[1][count]
        elif empty == 1 or empty == count - 1:
            if count >= 6:
                return score['FIVE']
            if block == 0 and count in switcher[2]:
                return switcher[2][count]
            if block == 1 and count in switcher[3]:
                return switcher[3][count]
        elif empty == 2 or empty == count - 2:
            if count >= 7:
                return score['FIVE']
            if block == 0 and count in switcher[4]:
                return switcher[4][count]
            if block == 1 and count in switcher[5]:
                return switcher[5][count]
            if block == 2 and count in switcher[6]:
                return switcher[6][count]
        elif empty == 3 or empty == count - 3:
            if count >= 8:
                return score['FIVE']
            if block == 0 and count in switcher[7]:
                return switcher[7][count]
            if block == 1 and count in switcher[8]:
                return switcher[8][count]
            if block == 2 and count in switcher[9]:
                return switcher[9][count]
        elif empty == 4 or empty == count - 4:
            if count >= 9:
                return score['FIVE']
            if block == 0 and count in switcher[10]:
                return switcher[10][count]
            if block == 1 and count in switcher[11]:
                return switcher[11][count]
            if block == 2 and count in switcher[12]:
                return switcher[12][count]
        elif empty == 5 or empty == count - 5:
            return score['FIVE']

        return 0
    

    def _is_five(self, x, y, role):
        scale = self.size[0]

        count = 1
        i = y + 1
        while True:
            if i >= scale:
                break
            t = self[x, i]
            if t != role:
                break
            count += 1
            i += 1
        i = y - 1
        while True:
            if i < 0:
                break
            t = self[x, i]
            if t != role:
                break
            count += 1
            i -= 1
        if count >= 5:
            return role
        
        count = 1
        i = x + 1
        while True:
            if i >= scale:
                break
            t = self[i, y]
            if t != role:
                break
            count += 1
            i += 1
        i = x - 1
        while True:
            if i < 0:
                break
            t = self[i, y]
            if t != role:
                break
            count += 1
            i -= 1
        if count >= 5:
            return role
        
        count = 1
        i = 1
        while True:
            xi = x + i
            yi = y + i
            if xi >= scale or yi >= scale:
                break
            t = self[xi, yi]
            if t != role:
                break
            count += 1
            i += 1
        i = 1
        while True:
            xi = x - i
            yi = y - i
            if xi < 0 or yi < 0:
                break
            t = self[xi, yi]
            if t != role:
                break
            count += 1
            i += 1
        if count >= 5:
            return role
        
        count = 1
        i = 1
        while True:
            xi = x + i
            yi = y - i
            if xi < 0 or yi < 0 or xi >= scale or yi >= scale:
                break
            t = self[xi, yi]
            if t != role:
                break
            count += 1
            i += 1
        i = 1
        while True:
            xi = x - i
            yi = y + i
            if xi < 0 or yi < 0 or xi >= scale or yi >= scale:
                break
            t = self[xi, yi]
            if t != role:
                break
            count += 1
            i += 1
        if count >= 5:
            return role
        
        return False

    def win(self):
        for i in self.xrange:
            for j in self.yrange:
                r = self[i, j]
                if r != 0:
                    role = self._is_five(i, j, r)
                    if role:
                        return role
        return False
    
    def _fix_evaluation(self, s, x, y, role):
        if s < score['FOUR'] and s >= score['BLOCKED_FOUR']:
            if s < score['BLOCKED_FOUR'] + score['THREE']:
                return score['THREE']
            elif s >= score['BLOCKED_FOUR'] + score['THREE'] and s < score['BLOCKED_FOUR'] * 2:
                return score['FOUR']
            else:
                return score['FOUR'] * 2
        if s >= score['FIVE'] and not self._is_five(x, y, role):
            return score['BLOCKED_FOUR'] * 4

        return s
