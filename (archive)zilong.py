# 用法说明
# 为获取下一步动作，调用 getAction(n, pattern_dict, xrange, yrange)
# n 代表深度
# pattern_dict 为当前棋局，xrange yrange 分别为目前我们容许AI下子的范围（可迭代的对象）
#
# 需要您实现的函数：
# forced_move = find_forced_move(pattern_dict, player) 返回的形式和原来一样
# new_pattern_dict = updatePatternDict(pattern_dict, x, y, value)
# value = evaluate(pattern_dict) 估计当前局面的分数

class Node:
    def __init__(self, pattern_dict, player = 1, successor = [], isLeaf = False, value = None):
        self.pattern_dict = pattern_dict
        self.player = 'max' if player = 1 else 'min'
        self.successor = successor
        self.isLeaf = isLeaf
        self.value = value
        self.visited = False

def constructTree(n, pattern_dict, xrange, yrange, player = 1):
    node = Node(pattern_dict=pattern_dict, player=player)
    successors = {}
    if n == 1:
        forced_move = find_forced_move(pattern_dict, player)
        if forced_move:
            position = forced[0]
            blanks = find_blank(forced[1])
            x, y = find_next_position(position, random.choice(blanks))
            nextPlayer = 2 if player == 1 else 1
            successors.update({(x, y): Node(updatePatternDict(pattern_dict, x, y, player), player=nextPlayer, isLeaf=True,value=evaluate(pattern_dict))})
        else:
            for x in xrange:
                for y in yrange:
                    if not pattern_dict[5][(x, y, 'v')]:  # TODO
                        successors.update({(x, y): Node(updatePatternDict(pattern_dict, x, y, player), player=nextPlayer, isLeaf=True,value=evaluate(pattern_dict))})
    else:
        forced_move = find_forced_move(pattern_dict, player)
        if forced_move:
            position = forced[0]
            blanks = find_blank(forced[1])
            x, y = find_next_position(position, random.choice(blanks))
            nextPlayer = 2 if player == 1 else 1
            successors.update({(x, y): constructTree(n-1, updatePatternDict(pattern_dict, x, y, player), xrange, yrange, player = nextPlayer)
        else:
            for x in xrange:
                for y in yrange:
                    if not pattern_dict[5][(x, y, 'v')]:  # TODO
                        successors.update({(x, y): constructTree(n-1, updatePatternDict(pattern_dict, x, y, player), xrange, yrange, player = nextPlayer)
    node.successor = successors
    return node

def getAction(n pattern_dict, xrange, yrange):
    node = constructTree(n, pattern_dict, xrange, yrange)
    alpha = float("-inf")
    beta = float("inf")
    pair = ((None, None), node)
    return maxPair(pair, alpha, beta)[0]


def maxPair(pair, alpha, beta):
    action = pair[0]
    node = pair[1]
    if node.isLeaf:
        node.visited = True
        return pair
    v = float("-inf")
    vPair = None
    for a in node.successor.items():
        minPairNext = minPair(pair, alpha, beta)
        if minPairNext[1].value > v:
            v = minPairNext[1].value
            vPair = minPairNext
        if v >= beta:
            return vPair
        alpha = max([alpha, v])
    return vPair


def minPair(pair, alpha, beta):
    action = pair[0]
    node = pair[1]
    if node.isLeaf:
        node.visited = True
        return pair
    v = float("inf")
    vPair = None
    for a in node.successor.items():
        maxPairNext = maxPair(a, alpha, beta)
        if maxPairNext[1].value < v:
            v = maxPairNext[1].value
            vPair = maxPairNext
        if v <= alpha:
            return vPair
        beta = min([beta, v])
    return vPair
