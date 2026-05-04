import sys
import importlib

# Load helper_alt as 'helper' so battleship imports the alternate helper
import helper_alt
sys.modules['helper'] = helper_alt

# Now import battleship fresh
import battleship
importlib.reload(battleship)


def count_ships(board):
    return sum(r.count(helper_alt.SHIP) for r in board)


def run_tests():
    rows, cols = helper_alt.NUM_ROWS, helper_alt.NUM_COLUMNS
    ship_sizes = helper_alt.SHIP_SIZES

    b = battleship.init_board(rows, cols)
    assert len(b) == rows and len(b[0]) == cols, "init_board shape mismatch"

    comp = battleship.create_computer_board(rows, cols, ship_sizes)
    # Count ship cells
    total_ship_cells = sum(ship_sizes)
    found = count_ships(comp)
    print("Expected ship cells:", total_ship_cells, "found:", found)
    assert found == total_ship_cells, "create_computer_board did not place correct ship cells"

    # Test valid_ship on a known placement location
    loc = (0, 0)
    ok = battleship.valid_ship(b, ship_sizes[0], loc)
    print("valid_ship at", loc, "for size", ship_sizes[0], "->", ok)

    print('All tests with helper_alt passed.')


if __name__ == '__main__':
    # Also test interactive flow of create_player_board using scripted inputs
    # Script inputs: place first ship at A1 (size 3), second ship at B1 (size 2)
    helper_alt.set_inputs(['A1', 'B1'])
    player_board = battleship.create_player_board(helper_alt.NUM_ROWS, helper_alt.NUM_COLUMNS, helper_alt.SHIP_SIZES)
    # verify that player_board has correct ship cells
    total_ship_cells = sum(helper_alt.SHIP_SIZES)
    found = sum(r.count(helper_alt.SHIP) for r in player_board)
    print(f"Player board ship cells: expected {total_ship_cells}, found {found}")
    assert found == total_ship_cells, "create_player_board did not place ships correctly with scripted inputs"
    run_tests()
