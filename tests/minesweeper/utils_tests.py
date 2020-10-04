import unittest
from minesweeper.utils import generate_board, get_valid_neighbors, board_pretty_printer


class UtilsTestCase(unittest.TestCase):
    def test_generate_board_mines_count(self):
        number_of_mines = 500
        rows = 100
        columns = 100
        new_board = generate_board(rows, columns, number_of_mines)
        self.assertEqual(sum([row.count("X") for row in new_board]), number_of_mines)
        
    def test_generate_board_adjacent_mines(self):
        number_of_mines = 500
        rows = 100
        columns = 100
        new_board = generate_board(rows, columns, number_of_mines)
        for row in range(rows):
            for column in range(columns):
                current_cell = new_board[row][column]
                if current_cell != "X":
                    adjacent_mines = [
                        new_board[neighbor_c][neighbor_r]
                        for neighbor_r, neighbor_c in get_valid_neighbors(row, column, rows, columns)
                        if new_board[neighbor_r][neighbor_c] == "X"
                    ]
                    self.assertEqual(len(adjacent_mines), int(current_cell))


if __name__ == '__main__':
    unittest.main()
