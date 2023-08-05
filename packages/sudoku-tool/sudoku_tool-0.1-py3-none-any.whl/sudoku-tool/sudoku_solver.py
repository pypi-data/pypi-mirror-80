import math


def print_board(boa):
    for row in boa:
        print(*row)


def find_empty(boa):
    n = len(boa)
    for row_idx in range(n):
        for col_idx in range(n):
            if boa[row_idx][col_idx] == 0:
                return row_idx, col_idx
    return None


def valid(boa, row, col, num):
    n = len(boa)
    for i in range(len(boa[row])):
        if col != i and num == boa[row][i]:
            return False

    for i in range(len(boa)):
        if row != i and num == boa[i][col]:
            return False
    step = int(math.sqrt(n))
    start_row = row - row % step
    start_col = col - col % step

    for i in range(start_row,start_row + step):
        for j in range(start_col,start_col + step):
            if boa[i][j] == num and (i,j) != (row,col):
                return False

    return True


def solve_board(boa):
    pos = find_empty(boa)
    if pos is None:
        return True
    row, col = pos
    n = len(boa)
    for num in range(1,n+1):
        if valid(boa,row,col,num):
            boa[row][col] = num

            if solve_board(boa):
                return True

            boa[row][col] = 0

    return False


def am_i_right(boa):
    n = len(boa)
    for row in boa:
        if len(set(row)) != n:
            return False

    for col in range(n):
        set_col = set()
        for row in boa:
            set_col.add(row[col])
        if len(set_col) != n:
            return False

    step = int(math.sqrt(n))
    for start_row in range(0,n-step+1,step):
        for start_col in range(0,n-step+1,step):
            set_box = set()
            for row in range(start_row,start_row+step):
                set_box=set_box.union(set(boa[row][start_col:start_col+step]))
            if len(set_box) != n:
                return False
    return True
