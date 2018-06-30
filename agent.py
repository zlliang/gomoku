import util

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
    global nodes_num
    nodes_num = 0
    x, y, top5_points = maxValue(board, 0, max_depth, -INF, INF, return_pattern=True)
    return x, y, top5_points, nodes_num


def maxValue(board, depth, max_depth, alpha, beta, return_pattern=False):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        # v = board.evaluate()
        # return v
        v = minimax_more_min(board)
        if v != -INF and v != INF:
            return v
        else:
            return board.evaluate()
    v = -INF
    point_scores = {}
    for x, y in board.candidate():
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
        # return board.evaluate()
        v = minimax_more_max(board)
        if v != -INF and v != INF:
            return v
        else:
            return board.evaluate()
    v = INF
    for x, y in board.candidate():
        if board[x, y] == 0:
            board[x, y] = 2
            v = min(v, maxValue(board, depth + 1, max_depth, alpha, beta))
            board[x, y] = 0
            if v <= alpha:
                return v
            beta = min(beta, v)
    return v

def minimax_more_max(board, max_depth=4):
    v = maxValue_more(board, 0, max_depth, -INF, INF)
    if v > 9000000:  # TODO: 如何判断赢
        return True
    return False

# def minimax_more_min(board, max_depth=4):
#     v = minValue_more(board, 0, max_depth, -INF, INF)
#     return v

def maxValue_more(board, depth, max_depth, alpha, beta):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        v = board.evaluate()
        return v
    v = -INF
    for x, y in board.candidate():
        if board.score_1[(x, y)] >= score['BLOCKED_FOUR']:
            if board[x, y] == 0:
                board[x, y] = 1
                v = minValue_more(board, depth + 1, max_depth, alpha, beta)
                board[x, y] = 0
                if v >= beta:
                    return v
                alpha = max(alpha, v)
    if v = -INF:
        return False
    return v

def minValue_more(board, depth, max_depth, alpha, beta):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        v = board.evaluate()
        return v
    v = INF
    for x, y in board.candidate():
        if board.score_2[(x, y)] < score['BLOCKED_FOUR'] and board.score_1[(x, y)] < score['BLOCKED_FOUR']:
            continue
        if board[x, y] == 0:
            board[x, y] = 2
            v = min(v, maxValue_more(board, depth + 1, max_depth, alpha, beta))
            board[x, y] = 0
            if v <= alpha:
                return v
            beta = min(beta, v)
            break
    return v
