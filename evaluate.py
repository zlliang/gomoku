def evaluate(board):
    """Score current board.

    Parameters
    ----------
    board: Current board, instance of `util.Board`
    
    Returns
    -------
    score: Float number of current board score
    """
    eval_func = [huo4, huo3]
    score = [func(board) for func in eval_func]
    score = sum(score)


def huo4(board):
    """
    [0, *, *, *, *, 0]
    """
    base = 90
    score = 0
    p = [0, 1, 1, 1, 1, 0]
    p_ = [0, 2, 2, 2, 2, 0]
    for pattern in board.pattern('6'):
        if pattern == p:
            score += base
        elif pattern == p_:
            score -= base
    return score

def chong4(board):
    """
    [~, *, *, *, *, 0]
    """
    base = 60
    score = 0
    p1 = [2, 1, 1, 1, 1, 0]
    p2 = [0, 1, 1, 1, 1, 2]
    p1_ = [1, 2, 2, 2, 2, 0]
    p2_ = [0, 2, 2, 2, 2, 1]
    for pattern in board.pattern('6'):  # TODO: Merge
        if pattern == p1 or pattern == p2:
            score += base
        elif pattern == p1_ or pattern == p2_:
            score -= base
    return score

def huo3(board):
    """
    [0, *, *, *, 0]
    """
    base = 50
    score = 0
    p = [0, 1, 1, 1, 0]
    p_ = [0, 2, 2, 2, 0]
    for pattern in board.pattern('5'):
        if pattern == p:
            score += base
        elif pattern == p_:
            score -= base
    return score

def tiao3(board):
    """[0, 1, 1, 0, 1, 0]"""
    base = 60
    score = 0
    p1 = [0, 1, 1, 0, 1, 0]
    p2 = [0, 1, 0, 1, 1, 0]
    p1_ = [0, 2, 2, 0, 2, 0]
    p2_ = [0, 2, 0, 2, 2, 0]
    for pattern in board.pattern('6'):
        if pattern in [p1, p2]:
            score += base
        elif pattern in [p1_, p2_]:
            score -= base
    return score

def lian3(board):
    """
    [0, 0, 0, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, *, 0]
    [0, 0, 0, 0, *, 0, 0]
    [0, *, *, *, 0, 0, 0]
    [0, 0, 0, 0, 0, 0, 0]
    """
    base = 200
    score = 0
    # p1 = [[6, 6, 6, 6, 6, 6, 0],
    #       [6, 6, 6, 6, 6, 1, 6],
    #       [6, 6, 6, 6, 1, 6, 6],
    #       [0, 1, 1, 1, 0, 6, 6],
    #       [6, 6, 0, 6, 6, 6, 6]]
    # p2 = [[0, 6, 6, 6, 6, 6, 6],
    #       [6, 1, 6, 6, 6, 6, 6],
    #       [6, 6, 1, 6, 6, 6, 6],
    #       [6, 6, 0, 1, 1, 1, 0],
    #       [6, 6, 6, 6, 0, 6, 6]]
    # p3 = [[6, 6, 6, 6, 0, 6, 6],
    #       [6, 6, 0, 1, 1, 1, 0],
    #       [6, 6, 1, 6, 6, 6, 6],
    #       [6, 1, 0, 6, 6, 6, 6],
    #       [0, 6, 6, 6, 0, 6, 6]]
    # p4 = [[6, 6, 0, 6, 6, 6, 6],
    #       [0, 1, 1, 1, 0, 6, 6],
    #       [6, 6, 6, 6, 1, 6, 6],
    #       [6, 6, 6, 6, 6, 1, 0],
    #       [6, 6, 6, 6, 0, 6, 0]]
    for pattern in board.pattern('7x5'):
        res = huo3(pattern)  # TODO
        if res >= 100:
            score += base
        elif res <= 100:
            score -= base
    return score
