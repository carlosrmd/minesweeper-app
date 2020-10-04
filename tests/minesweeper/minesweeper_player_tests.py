import unittest
from minesweeper.MinesweeperPlayer import MinesweeperPlayer
from minesweeper.constants import RESULT_GAME_LOST, RESULT_GAME_VICTORY
from datetime import datetime


class MinesweeperPlayerTestCase(unittest.TestCase):

    def test_minesweeper_player_hard_board_win(self):
        mp = MinesweeperPlayer("", "")
        mp._uncovered_board = [['X', '1', '0', '1', '1', '2', 'X', 'X', '3', 'X', '3', '1', '2', 'X', '1', '0'],
                               ['1', '1', '0', '1', 'X', '2', '2', '2', '3', 'X', '3', 'X', '3', '2', '3', '1'],
                               ['1', '2', '2', '4', '3', '3', '1', '1', '1', '1', '3', '2', '3', 'X', '2', 'X'],
                               ['X', '2', 'X', 'X', 'X', '2', 'X', '2', '1', '1', '2', 'X', '3', '1', '2', '1'],
                               ['1', '2', '4', 'X', '4', '2', '1', '2', 'X', '1', '2', 'X', '4', '2', '2', '1'],
                               ['1', '1', '3', 'X', '2', '0', '0', '1', '1', '1', '1', '2', 'X', 'X', '4', 'X'],
                               ['2', 'X', '2', '1', '1', '0', '0', '0', '0', '0', '0', '1', '4', 'X', '5', 'X'],
                               ['X', '2', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '3', 'X', '4', '1'],
                               ['1', '1', '0', '0', '0', '2', 'X', '2', '0', '0', '0', '0', '2', 'X', '3', '1'],
                               ['0', '0', '0', '0', '0', '2', 'X', '2', '0', '1', '1', '1', '1', '3', 'X', '2'],
                               ['0', '0', '0', '0', '1', '3', '3', '2', '0', '1', 'X', '1', '0', '2', 'X', '2'],
                               ['0', '0', '1', '1', '2', 'X', 'X', '2', '1', '1', '1', '1', '0', '1', '1', '1'],
                               ['0', '0', '1', 'X', '2', '2', '3', 'X', '2', '1', '2', '1', '2', '1', '2', '1'],
                               ['2', '2', '3', '2', '3', '1', '2', '1', '2', 'X', '2', 'X', '2', 'X', '2', 'X'],
                               ['X', 'X', '2', 'X', '3', 'X', '3', '2', '2', '3', '3', '2', '2', '1', '2', '1'],
                               ['2', '2', '2', '1', '3', 'X', 'X', '2', 'X', '2', 'X', '1', '0', '0', '0', '0']]
        mp._covered_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]
        mp._mines_count = 50
        mp._covered_cells_count = 16 * 16
        mp._rows = 16
        mp._columns = 16
        mp._result = ""
        mp._memo = {}
        mp._started_at = datetime.now()
        for row in range(mp._rows):
            for column in range(mp._columns):
                if mp._uncovered_board[row][column] != "X" and mp._covered_board[row][column] == "*":
                    mp.make_move(row, column)
        self.assertEqual(mp._result, RESULT_GAME_VICTORY)

    def test_minesweeper_player_hard_board_defeat(self):
        mp = MinesweeperPlayer("", "")
        mp._uncovered_board = [['X', '1', '0', '1', '1', '2', 'X', 'X', '3', 'X', '3', '1', '2', 'X', '1', '0'],
                               ['1', '1', '0', '1', 'X', '2', '2', '2', '3', 'X', '3', 'X', '3', '2', '3', '1'],
                               ['1', '2', '2', '4', '3', '3', '1', '1', '1', '1', '3', '2', '3', 'X', '2', 'X'],
                               ['X', '2', 'X', 'X', 'X', '2', 'X', '2', '1', '1', '2', 'X', '3', '1', '2', '1'],
                               ['1', '2', '4', 'X', '4', '2', '1', '2', 'X', '1', '2', 'X', '4', '2', '2', '1'],
                               ['1', '1', '3', 'X', '2', '0', '0', '1', '1', '1', '1', '2', 'X', 'X', '4', 'X'],
                               ['2', 'X', '2', '1', '1', '0', '0', '0', '0', '0', '0', '1', '4', 'X', '5', 'X'],
                               ['X', '2', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '3', 'X', '4', '1'],
                               ['1', '1', '0', '0', '0', '2', 'X', '2', '0', '0', '0', '0', '2', 'X', '3', '1'],
                               ['0', '0', '0', '0', '0', '2', 'X', '2', '0', '1', '1', '1', '1', '3', 'X', '2'],
                               ['0', '0', '0', '0', '1', '3', '3', '2', '0', '1', 'X', '1', '0', '2', 'X', '2'],
                               ['0', '0', '1', '1', '2', 'X', 'X', '2', '1', '1', '1', '1', '0', '1', '1', '1'],
                               ['0', '0', '1', 'X', '2', '2', '3', 'X', '2', '1', '2', '1', '2', '1', '2', '1'],
                               ['2', '2', '3', '2', '3', '1', '2', '1', '2', 'X', '2', 'X', '2', 'X', '2', 'X'],
                               ['X', 'X', '2', 'X', '3', 'X', '3', '2', '2', '3', '3', '2', '2', '1', '2', '1'],
                               ['2', '2', '2', '1', '3', 'X', 'X', '2', 'X', '2', 'X', '1', '0', '0', '0', '0']]
        mp._covered_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                             ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]
        mp._mines_count = 50
        mp._covered_cells_count = 16 * 16
        mp._rows = 16
        mp._columns = 16
        mp._result = ""
        mp._memo = {}
        mp._started_at = datetime.now()
        mp.make_move(0, 0)
        self.assertEqual(mp._result, RESULT_GAME_LOST)

    def test_minesweeper_player_easy_board_win(self):
        """
        Testing case where single uncovering can't uncover whole board because there's
        one non-mine cell outside cluster of zeroes
        """

        easy_board = MinesweeperPlayer("", "")
        easy_board._mines_count = 1
        easy_board._covered_cells_count = 10 * 10
        easy_board._rows = 10
        easy_board._columns = 10
        easy_board._result = ""
        easy_board._memo = {}
        easy_board._started_at = datetime.now()

        easy_board._uncovered_board = [["0", "0", "0", "0", "0", "0", "0", "0", "1", "1"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "1", "X"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "1", "1"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]

        easy_board._covered_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]

        easy_board.make_move(0, 0)
        self.assertEqual(easy_board._result, "")
        self.assertEqual(easy_board._covered_board[0][9], "*")
        easy_board.make_move(0, 9)
        self.assertEqual(easy_board._result, RESULT_GAME_VICTORY)

    def test_minesweeper_player_dummy_board_win(self):
        dummy_board = MinesweeperPlayer("", "")
        dummy_board._mines_count = 1
        dummy_board._covered_cells_count = 5 * 5
        dummy_board._rows = 5
        dummy_board._columns = 5
        dummy_board._result = ""
        dummy_board._memo = {}
        dummy_board._started_at = datetime.now()

        dummy_board._uncovered_board = [['0', '0', '0', '0', '0'],
                                       ['0', '1', '1', '1', '0'],
                                       ['0', '1', 'X', '1', '0'],
                                       ['0', '1', '1', '1', '0'],
                                       ['0', '0', '0', '0', '0']]

        dummy_board._covered_board = [['*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*'],
                                     ['*', '*', '*', '*', '*']]
        dummy_board.make_move(0,0)
        self.assertEqual(dummy_board._result, RESULT_GAME_VICTORY)


if __name__ == '__main__':
    unittest.main()
