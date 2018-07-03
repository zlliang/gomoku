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
    'name="Gakoii", '
    'author="Jiancong Gao & Zilong Liang", '
    'version="1.0", '
    'country="China", '
    'www="https://github.com/zlliang/gomoku"'
)

board = util.Board(scale=20)

INF = float("inf")
nodes_num = 0
checkmate_node = 0


def minimax(minimax_depth=5, checkmate_depth=10):
    global nodes_num, checkmate_node
    nodes_num = 0
    checkmate_node = 0
    check_1 = checkmate(board, role=1, checkmate_depth=checkmate_depth)
    # check_2 = checkmate(board, role=2, checkmate_depth=checkmate_depth)
    if check_1:
        return check_1, 1, None, (nodes_num, checkmate_node)
    # elif check_2:
    #     return check_2, 2, None, (nodes_num, checkmate_node)
    else:
        (x, y), v, top5_points = _minimax(depth=minimax_depth)
        return (x, y), v, top5_points, (nodes_num, checkmate_node)


def _minimax(depth):
    x, y, v, top5_points = maxValue(board, 0, depth, -INF, INF, return_pattern=True)
    return (x, y), v, top5_points


def maxValue(board, depth, max_depth, alpha, beta, return_pattern=False):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        return board.evaluate()
    v = -INF
    point_scores = {}
    candidates = board.candidate()
    ## Cut!!!
    # candidates = candidates[:6]
    # if depth <= 2:
    #     candidates = candidates[:5]
    # elif depth <= 4:
    #     candidates = candidates[:4]
    # else:
    #     candidates = candidates[:3]
    if len(candidates) > 3:
        candidates = candidates[:min(10, math.ceil(len(candidates) * (1 / 3 + 1 / (3 * depth + 3))))]
    if depth == 0 and len(candidates) == 1:
        x, y = candidates[0]
        return x, y, board.evaluate(), candidates
    for x, y in candidates:
        board[x, y] = 1
        check_2 = False
        if depth == 0:
            check_2 = checkmate(board, role=2, checkmate_depth=10)
        if check_2:
            v_new = -INF + 1
        else:
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
        return next_x, next_y, v, scores[:5]
    else:
        return v


def minValue(board, depth, max_depth, alpha, beta):
    global nodes_num
    nodes_num += 1
    if depth == max_depth:
        return board.evaluate()
    v = INF
    candidates = board.candidate()
    ## Cut!!!
    candidates = candidates[:6]
    # if depth <= 2:
    #     candidates = candidates[:5]
    # elif depth <= 4:
    #     candidates = candidates[:4]
    # else:
    #     candidates = candidates[:3]
    if len(candidates) > 3:
        candidates = candidates[:min(10, math.ceil(len(candidates) * (1 / 3 + 1 / (3 * depth + 3))))]
    for x, y in candidates:
        board[x, y] = 2
        v_new = maxValue(board, depth + 1, max_depth, alpha, beta)
        v = min(v, v_new)
        board[x, y] = 0
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def checkmate(board, role, checkmate_depth=6):
    return maxNode_more(board, role, 0, checkmate_depth)  # True/False


# def minimax_more_min(board, max_depth=4):
#     v = minValue_more(board, 0, max_depth, -INF, INF)
#     return v

def maxNode_more(board, role, depth, max_depth):
    global checkmate_node
    checkmate_node += 1
    winner = board.win()
    if winner == role:
        return True
    elif winner == 3 - role:
        return False
    if depth >= max_depth:
        return False
    for x, y in board.candidate():
        if role == 1:
            point_role_score = board.score_1[(x, y)]
        elif role == 2:
            point_role_score = board.score_2[(x, y)]
        if point_role_score >= 2 * score['THREE']:
            board[x, y] = role
            m = minNode_more(board, role, depth + 1, max_depth)
            board[x, y] = 0
            if m:
                if depth == 0:  # 可以斩杀
                    return x, y
                else:
                    return True
    return False


def minNode_more(board, role, depth, max_depth):
    global checkmate_node
    checkmate_node += 1
    winner = board.win()
    if winner == role:
        return True
    elif winner == 3 - role:
        return False
    if depth >= max_depth:
        return False
    cand = []
    for x, y in board.candidate():
        if board.score_2[(x, y)] + board.score_1[(x, y)] >= score['BLOCKED_FOUR']:
            board[x, y] = 3 - role  # opponent
            m = maxNode_more(board, role, depth + 1, max_depth)
            board[x, y] = 0
            if m:
                cand.append((x, y))
            else:
                return False
    if cand == []:
        return False
    else:
        return random.choice(cand)


if __name__ == '__main__':
    ## Debug 1
    # board = util.Board(board=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                           [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    #                           [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    #                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]])
    # board.step_count = 10
    # print(checkmate(board))
    # print(minimax())

    # Debug 2
    board = util.Board(scale=20)
    board[9, 6] = 1
    board[10, 6] = 2
    board[8, 7] = 1
    board[9, 7] = 2
    board[10, 7] = 1
    board[7, 8] = 2
    board[8, 8] = 2
    board[9, 8] = 2
    board[10, 8] = 1
    board[11, 8] = 2
    board[7, 9] = 1
    board[8, 9] = 2
    board[9, 9] = 1
    board[10, 9] = 1
    board[11, 9] = 1
    board[12, 9] = 1
    board[8, 10] = 2
    board[13, 9] = 2
