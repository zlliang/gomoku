import random
import util

# Hyper-parameters
depth = 7
gene_num = 20
crossover_num = 10
mutation_num = 2
iterations = 30

infotext = (
    'name="genetic", '
    'author="Jiancong Gao & Zilong Liang", '
    'version="1.0", '
    'country="China", '
    'www="https://github.com/zlliang/gomoku"'
)

board = util.Board(scale=20)

def genetic():
    # 初始化
    genes = initialize_genes()
    for _ in range(10):
        # 适者生存
        genes.sort(key=lambda seq: fitness(board, seq), reverse=True)
        genes = genes[:gene_num//2]
        # 交叉和突变产生子代
        childs = crossover(genes)
        childs = mutation(childs)
        # 合并
        genes = genes + childs
    # if True:  # TODO 停机准则
    genes.sort(key=lambda seq: fitness(board, seq), reverse=True)
    return genes[0][0]

def initialize_genes():
    genes = [[0 for _ in range(depth)] for _ in range(gene_num)]
    for i in range(gene_num):
        for j in range(depth):
            p = random.choice(board.candidate())
            genes[i][j] = p
            if j % 2 == 0:
                board[p[0], p[1]] = 1
            else:
                board[p[0], p[1]] = 2
        for j in range(depth):
            board[genes[i][j][0], genes[i][j][0]] = 0
    return genes
    

def fitness(board, sequence):
    i = 0
    while i < len(sequence):
        if i % 2 == 0:
            board[sequence[i][0], sequence[i][1]] = 1
        else:
            board[sequence[i][0], sequence[i][1]] = 2
        i += 1
    result = board.evaluate()
    for ind in sequence:
        board[ind[0], ind[1]] = 0
    return result

def valid(sequence):
    if len(set(sequence)) < len(sequence):
        return False
    for ind in sequence:
        if board[ind[0], ind[1]] != 0:
            return False
    return True

def crossover(genes):
    childs = list()
    i = 0
    while i < crossover_num:
        two_seq = random.sample(genes, 2)
        seq1, seq2 = _crossover(two_seq)
        if not valid(seq1) or not valid(seq2):
            continue
        childs.append(seq1)
        childs.append(seq2)
        i += 1
    return childs[:gene_num//2]

def _crossover(two_seq):
    seq1 = two_seq[0]
    seq2 = two_seq[1]
    point = random.randint(1, depth-1)
    temp11 = seq1[:point]
    temp12 = seq1[point:]
    temp21 = seq2[:point]
    temp22 = seq2[point:]
    seq1 = temp11 + temp22
    seq2 = temp21 + temp12
    return seq1, seq2

def mutation(genes):
    i = 0
    while i < mutation_num:
        index = random.randint(0, len(genes)-1)
        seq = _mutation(genes[index])
        if not valid(seq):
            continue
        genes[index] = seq
        i += 1
    return genes

def _mutation(seq):
    point = random.randint(0, depth-1)
    position = random.choice(board.candidate())
    seq[point] = position
    return seq
