import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG


pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


## ZILONG
tuple_dict = {}

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

for n in [5, 6]:
    tuple_dict_temp = {}
    for direction in ['v', 'h', 'rd']:
        tuple_dict_temp.update({(x, y, direction): [0, 0, 0, 0, 0] for x in range(MAX_BOARD-(n-1)) for y in range(MAX_BOARD-(n-1))})
    tuple_dict_temp.update({(x, y, 'ld'): [0, 0, 0, 0, 0] for x in range(n-1, MAX_BOARD) for y in range(MAX_BOARD-(n-1))})
    tuple_dict[n] = tuple_dict_temp

def updateTupleDict(x, y, value):
    for n in [5, 6]:
        xFrom = max(x-(n-1), 0)
        xTo = min(x+(n-1), MAX_BOARD-1) - (n-1)
        yFrom = max(y-(n-1), 0)
        yTo = min(y+(n-1), MAX_BOARD-1) - (n-1)
        for xx in range(xFrom, xTo+1):
            tuple_dict[n][(xx , y, 'v')][x-xx] = value
            if (xx, xx+y-x, 'rd') in tuple_dict[n]:
                tuple_dict_[n][(xx, xx+y-x, 'rd')][x-xx] = value
        for yy in range(yFrom, yTo+1):
            tuple_dict[n][(x, yy, 'h')][y-yy] = value
            if (x+y-yy, yy, 'ld') in tuple_dict[n]:
                tuple_dict[n][(x+y-yy, yy, 'ld')][y-yy] = value



def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
        updateTupleDict(x, y, 1)
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
        updateTupleDict(x, y, 2)
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
        updateTupleDict(x, y, 3)
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    if pp.terminateAI:
        return
    i = 0
    while True:
        x = random.randint(0, pp.width)
        y = random.randint(0, pp.height)
        i += 1
        if pp.terminateAI:
            return
        if isFree(x, y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(x, y)


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()
