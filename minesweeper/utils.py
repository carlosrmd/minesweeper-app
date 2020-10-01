import random


def get_valid_neighbors(row: int, column: int, total_rows: int, total_columns: int):
    """
    Get valid neighbors from specified coordinates
    :param row: row coordinate
    :param column: column coordinate
    :param total_rows: limit of rows
    :param total_columns: limit of columns
    :return: valid
    """
    if row + 1 < total_rows:
        yield row + 1, column
        if column - 1 >= 0:
            yield row + 1, column - 1
    if row - 1 >= 0:
        yield row - 1, column
    if column + 1 < total_columns:
        yield row, column + 1
        if row - 1 >= 0:
            yield row - 1, column + 1
    if column - 1 >= 0:
        yield row, column - 1
    if row + 1 < total_rows and column + 1 < total_columns:
        yield row + 1, column + 1
    if row - 1 >= 0 and column - 1 >= 0:
        yield row - 1, column - 1


def generate_random_mines_coordinates(rows: int, columns: int, mines: int):
    """
    Knowing number of rows and columns, generates as many mines as specified in
    parameter mines.
    :param rows: How many rows are in your board
    :param columns: How many columns are in your board
    :param mines: How many mines the user wants
    :return: Yields distinct pairs of coordinates.
    """
    for mine in random.sample(range(rows*columns), mines):
        yield mine // columns, mine % columns


def generate_board(rows: int, columns: int, mines: int):
    """
    Creates new board.
    :param rows: Number of desired rows
    :param columns: Number of desired columns
    :param mines: Number of desired mines
    :return: The board
    """
    board = [[0 for _ in range(columns)] for _ in range(rows)]
    for (r, c) in generate_random_mines_coordinates(rows, columns, mines):
        board[r][c] = 'X'
        for neighbor_r, neighbor_c in get_valid_neighbors(r, c, rows, columns):
            if isinstance(board[neighbor_r][neighbor_c], int):
                board[neighbor_r][neighbor_c] += 1
    return board


def generate_empty_board(rows: int, columns: int):
    return [["0" for _ in range(columns)] for _ in range(rows)]


def board_pretty_printer(board):
    for row in board:
        print(*row, sep=" ")
