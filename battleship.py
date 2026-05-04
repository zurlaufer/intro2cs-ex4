#################################################################
# FILE : battleship.py
# WRITER : Zur Laufer , laufer.zur , 217644186
# EXERCISE : intro2cs ex4 2026
# DESCRIPTION: A simple program that answer all the questions
# STUDENTS I DISCUSSED THE EXERCISE WITH: Elkana Daum
#################################################################

import helper


def init_board(rows, columns):
    board = []
    for i in range(rows):
        board.append([])
        for j in range(columns):
            board[i].append(helper.WATER)
    return board


def valid_ship(board, size, loc):
    if loc[0] + size > len(board) or loc[1] >= len(board[0]) or loc[0] >= len(board):
        return False
    for i in range(size):
        if board[loc[0] + i][loc[1]] != helper.WATER:
            return False
    return True


def legal_location(name):
    name = name.upper()
    if helper.is_cell_name(name):  # checks if helper is point on place in the board
        loc = cell_name_to_loc(name)
        if loc[0] < helper.NUM_ROWS and loc[1] < helper.NUM_COLUMNS:
            return True, loc
    return False, (-1, -1)


def place_ship(board, size, loc):
    for i in range(size):
        board[loc[0] + i][loc[1]] = helper.SHIP
    return board


def cell_name_to_loc(name):
    return (int(name[1:]) - 1, ord(name[0]) - 65)


def get_location(board, size):
    helper.show_board(board)  # shows the board
    prompt = (
        "Enter the wanted position of the ship on the board as a letter to mark "
        "the columns and a number to mark the rows"
    )
    name = helper.get_input(prompt)  # gets the wanted location
    is_legal, loc = legal_location(name)
    if is_legal:
        if valid_ship(board, size, loc):  # places the ship if it able to
            board = place_ship(board, size, loc)
            return board
    # the board didn't return so it calls the function again and explain what the user needs to do
    helper.show_msg("Enter a valid location with enough space for the entire ship")
    return get_location(board, size)


def create_player_board(rows, columns, ship_sizes):
    board = init_board(rows, columns)  # makes the board
    if board == []:
        return board
    for size in ship_sizes:  # for loops of every size of ship
        board = get_location(board, size)  # place the ship
    return board


def create_computer_board(rows, columns, ship_sizes):
    board = init_board(rows, columns)
    if board == []:
        return board
    for size in ship_sizes:
        locations = []
        for i in range(rows):
            for j in range(columns):
                if valid_ship(board, size, (i, j)):
                    locations.append((i, j))
        loc = helper.choose_ship_location(board, size, locations)
        assert valid_ship(board, size, loc)
        board = place_ship(board, size, loc)
    helper.show_board(board)
    return board


def turn(player_board, computer_board, hiden_computer_board):
    helper.show_board(player_board, hiden_computer_board)  # prints the two boards
    player_input = helper.get_input("Enter a location of tropedo target")  # gets torpedo terget
    is_legal, player_torpedo_loc = legal_location(player_input)  # gets player torpedo location
    # checks the location is legal
    while (not is_legal) or hiden_computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] != helper.WATER:
        player_input = helper.get_input("Enter a valid location of tropedo target")
        is_legal, player_torpedo_loc = legal_location(player_input)
    # choose a legal target for the computer torpedo
    locations = []
    for i in range(helper.NUM_ROWS):
        for j in range(helper.NUM_COLUMNS):
            if player_board[i][j] == helper.WATER or player_board[i][j] == helper.SHIP:
                locations.append((i, j))
    computer_torpedo_loc = helper.choose_torpedo_target(player_board, locations)

    # updates the boards
    if player_board[computer_torpedo_loc[0]][computer_torpedo_loc[1]] == helper.SHIP:  # checks if it hit a ship
        player_board[computer_torpedo_loc[0]][computer_torpedo_loc[1]] = helper.HIT_SHIP
    elif player_board[computer_torpedo_loc[0]][computer_torpedo_loc[1]] == helper.WATER:  # checks if it hit the water
        player_board[computer_torpedo_loc[0]][computer_torpedo_loc[1]] = helper.HIT_WATER

    if computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] == helper.SHIP:  # checks if it hit a ship
        computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] = helper.HIT_SHIP
        hiden_computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] = helper.HIT_SHIP
    elif computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] == helper.WATER:  # checks if it hit the water
        computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] = helper.HIT_WATER
        hiden_computer_board[player_torpedo_loc[0]][player_torpedo_loc[1]] = helper.HIT_WATER

    num_of_player_ships = sum(r.count(helper.SHIP) for r in player_board)
    num_of_computer_ships = sum(r.count(helper.SHIP) for r in computer_board)
    if num_of_player_ships * num_of_computer_ships == 0:
        return True
    return False


def main():
    player = {'rows': helper.NUM_ROWS, 'columns': helper.NUM_COLUMNS,
              'ship_sizes': helper.SHIP_SIZES}  # makes player board
    player_board = create_player_board(player['rows'], player['columns'], player['ship_sizes'])
    _ = init_board(player['rows'], player['columns'])
    computer = {'rows': helper.NUM_ROWS, 'columns': helper.NUM_COLUMNS,
                'ship_sizes': helper.SHIP_SIZES}  # makes computer board
    computer_board = create_computer_board(computer['rows'], computer['columns'], computer['ship_sizes'])
    hiden_computer_board = init_board(computer['rows'], computer['columns'])
    if helper.NUM_ROWS == helper.NUM_COLUMNS == 0:
        return

    b = False
    while not b:
        b = turn(player_board, computer_board, hiden_computer_board)
    helper.show_board(player_board, computer_board)
    play_again = helper.get_input("play again?")
    while play_again != 'Y' and play_again != 'N':
        play_again = helper.get_input("play again? answer 'Y' or 'N'")
    if play_again == 'Y':
        main()


if __name__ == "__main__":
    main()
