def evaluate(board):
    """Score current board.

    Parameters
    ----------
    board: Current board, instance of `util.Board`
    
    Returns
    -------
    score: Float number of current board score
    """
    eval_func = [check2, check3, check4]
    score = [func(board) for func in eval_func]
    score = sum(score)
    return score

def check2(board):
    """死2，活2"""
    score = 0
    s_si2 = 1
    p_si2 = [[2, 1, 1, 0], [0, 1, 1, 2]]
    p_si2_ = [[1, 2, 2, 0], [0, 2, 2, 1]]
    s_huo2 = 3
    p_huo2 = [0, 1, 1, 0]
    p_huo2_ = [0, 2, 2, 0]
    for p in board.pattern('4'):
        if p in p_si2:
            score += s_si2
        elif p in p_si2_:
            score -= s_si2
        elif p == p_huo2:
            score += s_huo2
        elif p == p_huo2_:
            score -= s_huo2
    return score

def check3(board):
    """死3，活3"""
    score = 0
    s_si3 = 7
    p_si3 = [[2, 1, 1, 1, 0], [0, 1, 1, 1, 2]]
    p_si3_ = [[1, 2, 2, 2, 0], [0, 2, 2, 2, 1]]
    s_huo3 = 63
    p_huo3 = [0, 1, 1, 1, 0]
    p_huo3_ = [0, 2, 2, 2, 0]
    for p in board.pattern('5'):
        if p in p_si3:
            score += s_si3
        elif p in p_si3_:
            score -= s_si3
        elif p == p_huo3:
            score += s_huo3
        elif p == p_huo3_:
            score -= s_huo3
    return score

def check4(board):
    """冲4，活4"""
    score = 0
    s_chong4 = 31
    p_chong4 = [[2, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 2]]
    p_chong4_ = [[1, 2, 2, 2, 2, 0], [0, 2, 2, 2, 2, 1]]
    s_huo4 = 511
    p_huo4 = [0, 1, 1, 1, 1, 0]
    p_huo4_ = [0, 2, 2, 2, 2, 0]
    for p in board.pattern('6'):
        if p in p_chong4:
            score += s_chong4
        elif p in p_chong4_:
            score -= s_chong4
        elif p == p_huo4:
            score += s_huo4
        elif p == p_huo4_:
            score -= s_huo4
    return score
