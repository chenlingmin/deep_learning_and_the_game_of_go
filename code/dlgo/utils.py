from dlgo import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: " . ",
    gotypes.Player.black: ' ● ',
    gotypes.Player.white: ' ୦ ',
}


def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))


def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print("%s%d %s" % (bump, row, ''.join(line)))
    print('    ' + '  '.join(COLS[:board.num_cols]))

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)


def print_board_plus(board):
    """显示局面"""

    num_rows = board.num_rows
    num_cols = board.num_cols

    for row in range(num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            if stone == gotypes.Player.black:
                chessman = ' ● '
            elif stone == gotypes.Player.white:
                chessman = ' ୦ '
            else:
                if row == num_rows:
                    if col == num_cols:
                        chessman = '─┐ '
                    elif col == 1:
                        chessman = ' ┌─'
                    else:
                        chessman = '─┬─'
                elif row == 1:
                    if col == num_cols:
                        chessman = '─┘ '
                    elif col == 1:
                        chessman = ' └─'
                    else:
                        chessman = '─┴─'
                elif col == num_cols:
                    chessman = '─┤ '
                elif col == 1:
                    chessman = ' ├─'
                else:
                    chessman = '─┼─'
            print('\033[0;30;43m' + chessman + '\033[0m', end='')
        print("%s%d" % (bump, row))
    print(' ' + '  '.join(COLS[:board.num_cols]))
