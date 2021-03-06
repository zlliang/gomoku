import util

infotext = (
    'name="minimax", '
    'author="Jiancong Gao & Zilong Liang", '
    'version="1.0", '
    'country="China", '
    'www="https://github.com/zlliang/gomoku"'
)

board = util.Board(scale=20)

INF = float("inf")
nodes_num = 0


def minimax(max_depth=3):
    return _minimax(max_depth)


def _minimax(depth=4):
    global nodes_num
    nodes_num = 0
    x, y, top5_points = maxValue(board, 0, depth, -INF, INF, return_pattern=True)
    return x, y


def maxValue(board, depth, max_depth, alpha, beta, return_pattern=False):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        v = board.evaluate()
        return v
    v = -INF
    point_scores = {}
    # Choose candidate
    candidates = board.candidate()
    # if len(candidates) >= 5:
    #     candidates.sort(key=lambda c: _approx(c, 1))
    for x, y in candidates:
        if board[x, y] == 0:
            board[x, y] = 1
            v_new = minValue(board, depth + 1, max_depth, alpha, beta)
            v = max(v, v_new)
            if return_pattern:
                point_scores[(x, y)] = v_new
            board[x, y] = 0
            if v >= beta:
                return v
            alpha = max(alpha, v)
    if return_pattern:
        scores = sorted(list(point_scores.items()), key=lambda x: x[1], reverse=True)
        next_x, next_y = scores[0][0]
        return next_x, next_y, scores[:5]
    else:
        return v


def minValue(board, depth, max_depth, alpha, beta):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        return board.evaluate()
    v = INF
    # Choose candidate
    candidates = board.candidate()
    # if len(candidates) >= 5:
    #     candidates.sort(key=lambda c: _approx(c, 2))
    for x, y in candidates:
        if board[x, y] == 0:
            board[x, y] = 2
            v = min(v, maxValue(board, depth + 1, max_depth, alpha, beta))
            board[x, y] = 0
            if v <= alpha:
                return v
            beta = min(beta, v)
    return v


def _approx(c, role):
    board[c[0], c[1]] = role
    v = board.evaluate()
    board[c[0], c[1]] = 0
    return v
