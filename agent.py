import util
import random
import math

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


def minimax(depth=4):
    global nodes_num
    nodes_num = 0
    x, y, top5_points = maxValue(board, 0, depth, -INF, INF, return_pattern=True)
    return x, y


def maxValue(board, depth, max_depth, alpha, beta, return_pattern=False):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        win = checkmate(board)
        if win:
            return INF
        else:
            return board.evaluate()
    v = -INF
    point_scores = {}
    cand = board.candidate()
    cand = cand[:math.ceil(len(cand) / (depth + 1))+1]
    for x, y in cand:
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
    cand = board.candidate()
    cand = cand[:math.ceil(len(cand) / (depth + 1))]
    for x, y in cand:
        if board[x, y] == 0:
            board[x, y] = 2
            v_new = maxValue(board, depth + 1, max_depth, alpha, beta)
            v = min(v, v_new)
            board[x, y] = 0
            if v <= alpha:
                return v
            beta = min(beta, v)
    return v


def checkmate(board, checkmate_depth=6):
    return maxNode_more(board, 0, checkmate_depth)  # True/False


# def minimax_more_min(board, max_depth=4):
#     v = minValue_more(board, 0, max_depth, -INF, INF)
#     return v

def maxNode_more(board, depth, max_depth):
    global nodes_num
    nodes_num += 1
    v = board.evaluate()
    if v > 9000000:  # TODO: 如何判断赢
        return True
    elif v < -9000000:
        return False
    if depth >= max_depth:
        return False
    for x, y in board.candidate():
        if board.score_1[(x, y)] >= score['BLOCKED_FOUR']:
            board[x, y] = 1
            m = minNode_more(board, depth + 1, max_depth)
            board[x, y] = 0
            if m:  # 可以斩杀
                return True
    return False


def minNode_more(board, depth, max_depth):
    global nodes_num
    nodes_num += 1
    v = board.evaluate()
    if v > 9000000:  # TODO: 如何判断赢
        return True
    elif v < -9000000:
        return False
    if depth >= max_depth:
        return False
    cand = []
    for x, y in board.candidate():
        if board.score_2[(x, y)] + board.score_1[(x, y)] >= score['FOUR']:
            board[x, y] = 2
            m = maxNode_more(board, depth + 1, max_depth)
            board[x, y] = 0
            if m:
                cand.append((x, y))
            else:
                return False
    if cand == []:
        return False
    else:
        return random.choice(cand)

