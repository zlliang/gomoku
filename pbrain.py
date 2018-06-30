# Python Piskvork framework
# This is a modified version of pbrain agent, compatible with Piskvork manager.
# Author: @stranskyjan: https://github.com/stranskyjan/pbrain-pyrandom/
# Modified: @zlliang: https://github.com/zlliang/gomoku/

import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

# Our agent
import agent as agent

# import genetic as agent
# import mcts as agent

pp.infotext = agent.infotext
MAX_BOARD = 20


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
            agent.board[x, y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    cond1 = x >= 0 and y >= 0
    cond2 = x < pp.width and y < pp.height
    cond3 = agent.board[x, y] == 0
    return all([cond1, cond2, cond3])


def brain_my(x, y):
    if isFree(x, y):
        agent.board[x, y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        agent.board[x, y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        agent.board[x, y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    cond1 = x >= 0 and y >= 0
    cond2 = x < pp.width and y < pp.height
    cond3 = agent.board[x, y] != 0
    if all([cond1, cond2, cond3]):
        agent.board[x, y] = 0
        return 0
    return 2


# brain_turn should be implemented in specific agents
def brain_turn():
    if pp.terminateAI:
        return
    x, y, top5_points, nodes_num = agent.minimax()
    pp.do_mymove(x, y)
    # print("Search Nodes Expanded:{}".format(nodes_num)+str(top5_points))


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
        c = str(agent.board[x, y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "/tmp/pbrain-pyrandom.log"
# ...and clear it initially
with open(DEBUG_LOGFILE,"w") as f:
	pass

# define a function for writing messages to the file
def logDebug(msg):
	with open(DEBUG_LOGFILE,"a") as f:
		f.write(msg+"\n")
		f.flush()

# define a function to get exception traceback
def logTraceBack():
	import traceback
	with open(DEBUG_LOGFILE,"a") as f:
		traceback.print_exc(file=f)
		f.flush()
	raise

# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
def brain_turn():
	logDebug("some message 1")
	try:
		logDebug("some message 2")
		1. / 0. # some code raising an exception
		logDebug("some message 3") # not logged, as it is after error
	except:
		logTraceBack()
"""
######################################################################

# Overwrite functions in pisqpipe module
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

if __name__ == "__main__":
    pp.main()
