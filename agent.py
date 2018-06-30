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
    x, y = maxValue(board, 0, max_depth, -INF, INF, return_pattern=True)
    print("Nodes Expanded:", nodes_num)
    return x, y


def maxValue(board, depth, max_depth, alpha, beta, return_pattern=False):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        v = board.evaluate()
        return v
    v = -INF
    x_max, y_max = 0, 0
    for x, y in board.candidate():
        if board[x, y] == 0:
            board[x, y] = 1
            v_old = v
            v = max(v, minValue(board, depth + 1, max_depth, alpha, beta))
            if v > v_old:
                x_max, y_max = x, y
            board[x, y] = 0
            if v >= beta:
                return v
            alpha = max(alpha, v)
    if return_pattern:
        return x_max, y_max
    else:
        return v


def minValue(board, depth, max_depth, alpha, beta):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        return board.evaluate()
    v = INF
    for x, y in board.candidate():
        if board[x, y] == 0:
            board[x, y] = 2
            v = min(v, maxValue(board, depth + 1, max_depth, alpha, beta))
            board[x, y] = 0
            if v <= alpha:
                return v
            alpha = min(beta, v)
    return v
