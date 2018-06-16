def evaluate(board):
    """Score current board.

    Parameters
    ----------
        board: Current board, instance of `util.Board`
    
    Returns
    -------
        score: Float number of current board score
    """
    raise NotImplementedError("Evaluate function has not been implemented!")
    eval_func = [eval_1, eval_2]
    score = [func(board) for func in eval_func]
    score = sum(score)
    return score

# Helper functions
def eval_1(board):
    return 0

def eval_2(board):
    return 0
