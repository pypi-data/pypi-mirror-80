import math
import random
from .sudoku_solver import print_board,solve_board,am_i_right


def random_list(n):
    w = [0]*n
    for j in range(n):
        w[j] = j + 1
    for j in range(n-1, -1, -1):
        num = random.randint(0, n-1)
        w[num], w[j] = w[j], w[num]
    return w


def fill_box(boa, row, col):
    n = len(boa)
    step = int(math.sqrt(n))
    start_row = row - row % step
    start_col = col - col % step
    w = random_list(n)
    for i in range(step):
        boa[start_row+i][start_col:start_col+step] = w[i*step:(i+1)*step]


def random_board_generator(n):
    board = []
    for i in range(n):
        z = []
        for j in range(n):
            z.append(0)
        board.append(z)
    step = int(math.sqrt(n))
    for i in range(0,n,step):
        fill_box(board,i,i)
    solve_board(board)
    print_board(board)
    for i in range(n):
        for j in range(n):
            if random.random() < 0.5:
                board[i][j] = 0
    return board