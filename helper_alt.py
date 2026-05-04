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
        row = ''.join(
            print_mapping.get(board[i][j], '? ') for j in range(len(board[i]))
        )
        return str(i + 1).rjust(2) + ' ' + row
    return ''


def show_board(board1, board2=None):
    boards = [board1] if board2 is None else [board1, board2]
    header = "   " + ''.join([chr(j + ord('A')) + ' ' for j in range(len(board1[0]))])
    sep = ' ' * 8
    print(*(header for _ in boards), sep=sep)
    for i in range(max(len(b) for b in boards)):
        print(*(str_row(b, i) for b in boards), sep=sep)


def get_input(msg):
    # Return next scripted input if present (simulate interactive user)
    if hasattr(get_input, "_inputs") and get_input._inputs:
        val = get_input._inputs.pop(0)
        print(msg + val)
        return val
    raise RuntimeError("get_input() called but no scripted inputs available")


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


def set_inputs(lst):
    """Provide a list of string inputs to be returned by `get_input` (FIFO)."""
    get_input._inputs = list(lst)


def clear_inputs():
    get_input._inputs = []


if __name__ == '__main__':
    pass
