def evaluate(board):
    """Score current board.

    Parameters
    ----------
        board: Current board, instance of `util.Board`
    
    Returns
    -------
        score: Float number of current board score
    """
    # raise NotImplementedError("Evaluate function has not been implemented!")
    eval_func = [huo4, huo3]
    score = [func(board) for func in eval_func]
    score = sum(score)
    return score

# Helper functions
def huo4(board):
    base = 90
    score = 0
    for pattern in board.pattern('6'):
        if pattern == [0, 1, 1, 1, 1, 0]:
            score += base
        elif pattern == [0, 2, 2, 2, 2, 0]:
            score -= base
    return score

def huo3(board):
    base = 50
    score = 0
    for pattern in board.pattern('5'):
        if pattern == [0, 1, 1, 1, 0]:
            score += base
        elif pattern == [0, 2, 2, 2, 0]:
            score -= base
    return score
