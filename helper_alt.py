#!/usr/bin/env python3
"""Alternate deterministic helper for testing.
Provides smaller board and deterministic choices (first valid location).
"""

NUM_ROWS = 4
NUM_COLUMNS = 4
SHIP_SIZES = (3, 2)

WATER = 0
SHIP = 1
HIT_WATER = 2
HIT_SHIP = 3

# Simple print mapping (no color)
print_mapping = {WATER: '. ', SHIP: 'x ', HIT_WATER: 'o ', HIT_SHIP: '* '}


def str_row(board, i):
    if i < len(board):
        return (str(i + 1).rjust(2) + ' ' + ''.join(print_mapping.get(board[i][j], '? ') for j in range(len(board[i]))))
    return ''


def show_board(board1, board2=None):
    boards = [board1] if board2 is None else [board1, board2]
    header = "   " + ''.join([chr(j + ord('A')) + ' ' for j in range(len(board1[0]))])
    sep = ' ' * 8
    print(*(header for _ in boards), sep=sep)
    for i in range(max(len(b) for b in boards)):
        print(*(str_row(b, i) for b in boards), sep=sep)


def get_input(msg):
    raise RuntimeError("get_input() called in non-interactive test helper")


def show_msg(msg):
    print(msg)


def is_cell_name(s):
    return isinstance(s, str) and len(s) >= 2 and s[0].isalpha() and s[1:].isdigit()


def choose_ship_location(board, size, locations):
    """Deterministic: choose the lexicographically smallest location."""
    if not locations:
        raise ValueError("No valid locations")
    return sorted(locations)[0]


def choose_torpedo_target(board, locations):
    if not locations:
        raise ValueError("No valid targets")
    return sorted(locations)[0]


def seed(a):
    pass


if __name__ == '__main__':
    pass
