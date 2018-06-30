import util
import copy
from math import sqrt, log
import random
import time

board = util.Board(scale=20)

# Hyper-parameters
confidence = 1.96
max_actions = 1000
max_time = 5.0
max_depth = 1

# Variants
plays = {}
wins = {}
role_turn = [1, 2]


def mcts(role=role_turn[0]):
    global plays, wins

    candidates = board.candidate()
    print(candidates)
    if len(candidates) == 1:
        return candidates[0]

    plays = {}
    wins = {}
    simulations = 0
    begin_time = time.time()
    while time.time() - begin_time < max_time:
        simulate(copy.deepcopy(board), copy.deepcopy(role_turn))
        simulations += 1
    
    print("Total simulations: ", simulations)
    print("Maximum depth: ", max_depth)

    x, y = select_best_move(candidates)
    return x, y

def simulate(board, role_turn):
    global plays, wins, max_depth
    
    candidates = board.candidate()
    role = get_role(role_turn)
    visited_states = set()
    winner = False
    expand = True

    # Simulation
    for t in range(1, max_actions + 1):
        # Selection
        if all(plays.get((role, move)) for move in candidates):
            log_total = log(sum(plays[(role, move)] for move in candidates))
            value, move = max(
                ((wins[(role, move)] / plays[(role,move)]) + sqrt(confidence*log_total / plays[(role, move)]), move)
            for move in candidates)
        else:
            move = random.choice(candidates)
        board[move[0], move[1]] = role

        # Expand
        if expand and (role, move) not in plays:
            expand = False
            plays[(role, move)] = 0
            wins[(role, move)] = 0
            if t > max_depth:
                max_depth = t
        
        visited_states.add((role, move))
        win = board.win()
        if win != False:
            break
        
        role = get_role(role_turn)
    
    # Back-propagation
    for r, move in visited_states:
        if (r, move) not in plays:
            continue
        plays[(r, move)] += 1
        if r == win:
            wins[(r, move)] += 1

def get_role(role_turn):
    p = role_turn.pop(0)
    role_turn.append(p)
    return p

def select_best_move(candidates):
    percent_wins, move = max(
        (wins.get((1, move), 0) / plays.get((1, move), 1), move)
    for move in candidates)
    return move
