def find_forced_move():
    '''
    If detect 4 in a row, break and return (position,pattern).
    Else, if there are 3 in a row, random return one.
    Or if there is no forced move, return None.
    '''
    alive_list = []
    for i in tuple_dict[5].items():
        if i[1] == [2, 2, 0, 2, 2]:
            return i
        if i[1] == [0, 2, 2, 2, 0]:
            alive_list.append(i)
    for i in tuple_dict[6].items():
        if i[1] == [1, 2, 2, 2, 2, 0] or i[1] == [0, 2, 2, 2, 2, 1]:
            return i
        if i[1] == [0, 2, 2, 0, 2, 0] or i[1] == [0, 2, 0, 2, 2, 0]:
            alive_list.append(i)
    if len(alive_list) > 0:
        return random.choice(alive_list)
    else:
        return None


def find_next_position(pattern, step):
    x, y, dir = pattern
    if dir == 'h':
        return (x + step, y)
    elif dir == 'v':
        return (x, y + step)
    elif dir == 'rd':
        return (x + step, y + step)
    elif dir == 'ld':
        return (x - step, y + step)
    else:
        pp.pipeOut("Error Direction")


def find_blank(seq):
    blanks = []
    for i in range(len(seq)):
        if not seq[i]:
            blanks.append(i)
    return blanks


def brain_turn_baseline():
    if pp.terminateAI:
        return
    forced = find_forced_move()
    if forced is not None:
        position = forced[0]
        blanks = find_blank(forced[1])
        x, y = find_next_position(position, random.choice(blanks))
        pp.do_mymove(x, y)
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
