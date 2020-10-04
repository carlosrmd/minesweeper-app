from minesweeper.utils import get_valid_neighbors, board_pretty_printer
from minesweeper.constants import RESULT_GAME_LOST, RESULT_GAME_VICTORY, STATUS_FINISHED, DATETIME_FORMAT
from bson import ObjectId
from datetime import datetime


class MinesweeperPlayer:

    def __init__(self, game_id, db):
        self._game_id = game_id
        self._db = db
        self._uncovered_board = None
        self._covered_board = None
        self._mines_count = None
        self._covered_cells_count = None
        self._rows = None
        self._columns = None
        self._started_at = None
        self._total_time = None
        self._result = ""
        self._memo = {}

    def load_game_from_db(self):
        json_game = self._db.find_one({"_id": ObjectId(self._game_id)})
        self._started_at = datetime.strptime(json_game["started_at"], DATETIME_FORMAT)
        self._uncovered_board = json_game["board"]["uncovered_board"]
        self._covered_board = json_game["board"]["covered_board"]
        self._mines_count = json_game["board"]["total_mines"]
        self._covered_cells_count = json_game["board"]["covered_cells_count"]
        self._rows = json_game["board"]["total_rows"]
        self._columns = json_game["board"]["total_columns"]

    def save_game_to_db(self):
        update_json = {
            'board.covered_board': self._covered_board,
            'board.covered_cells_count': self._covered_cells_count
        }
        if not self._result == "":
            update_json['result'] = self._result
            update_json['status'] = STATUS_FINISHED
            update_json['total_time'] = self._total_time
        self._db.update_one({'_id': ObjectId(self._game_id)}, {'$set': update_json})

    def make_move(self, r, c):
        self._memo = {}
        if self._covered_board[r][c] != "*":
            return
        if self._uncovered_board[r][c] == 'X':
            self._covered_board[r][c] = 'X'
            self._result = RESULT_GAME_LOST
            self._total_time = (datetime.now() - self._started_at).total_seconds()
            return
        self._recursive_uncoverer(r, c)
        if self._covered_cells_count == self._mines_count:
            self._total_time = (datetime.now() - self._started_at).total_seconds()
            self._result = RESULT_GAME_VICTORY

    def _recursive_uncoverer(self, r, c):
        rc = "%s%s" % (r, c)
        self._memo[rc] = 1
        selected_char = self._uncovered_board[r][c]
        if selected_char == "0":
            self._covered_board[r][c] = selected_char
            self._covered_cells_count -= 1
            for neighbor_r, neighbor_c in get_valid_neighbors(r, c, self._rows, self._columns):
                if "%s%s" % (neighbor_r, neighbor_c) not in self._memo:
                    self._recursive_uncoverer(neighbor_r, neighbor_c)
        else:
            self._covered_board[r][c] = selected_char
            self._covered_cells_count -= 1


if __name__ == '__main__':
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
    mp._mines_count = 9
    mp._covered_cells_count = 16*16
    mp._rows = 16
    mp._columns = 16
    mp._result = ""
    mp._memo = {}
    mp._started_at = datetime.now()
    board_pretty_printer(mp._uncovered_board)
    print("=======================================")
    board_pretty_printer(mp._covered_board)
    print("=======================================")
    print("SELECTING 0, 2")
    print("=======================================")
    mp.make_move(0, 2)
    board_pretty_printer(mp._uncovered_board)
    print("=======================================")
    board_pretty_printer(mp._covered_board)
    print("=======================================")
    print("SELECTING 9, 0")
    print("=======================================")
    mp.make_move(9, 0)
    board_pretty_printer(mp._uncovered_board)
    print("=======================================")
    board_pretty_printer(mp._covered_board)
    print("=======================================")
    print("SELECTING 15, 15")
    print("=======================================")
    mp.make_move(15, 15)
    board_pretty_printer(mp._uncovered_board)
    print("=======================================")
    board_pretty_printer(mp._covered_board)
    print("=======================================")
    print("SELECTING 1, 14")
    print("=======================================")
    mp.make_move(1, 14)
    board_pretty_printer(mp._uncovered_board)
    print("=======================================")
    board_pretty_printer(mp._covered_board)
    print("RESULT IS " + mp._result)

    easy_board = MinesweeperPlayer("", "")
    easy_board._mines_count = 1
    easy_board._covered_cells_count = 5*5
    easy_board._rows = 5
    easy_board._columns = 5
    easy_board._result = ""
    easy_board._memo = {}
    easy_board._started_at = datetime.now()

    easy_board._uncovered_board =  [['0','0','0','0','0'],
                                    ['0','1','1','1','0'],
                                    ['0','1','X','1','0'],
                                    ['0','1','1','1','0'],
                                    ['0','0','0','0','0']]

    easy_board._covered_board =  [['*','*','*','*','*'],
                                    ['*','*','*','*','*'],
                                    ['*','*','*','*','*'],
                                    ['*','*','*','*','*'],
                                    ['*','*','*','*','*']]

    print()
    print("=======================================")
    print("EASY BOARD")
    board_pretty_printer(easy_board._uncovered_board)
    print("=======================================")
    board_pretty_printer(easy_board._covered_board)
    print("=======================================")
    print("SELECTING 0, 2")
    print("=======================================")
    easy_board.make_move(0, 2)
    board_pretty_printer(easy_board._uncovered_board)
    print("=======================================")
    board_pretty_printer(easy_board._covered_board)
    print("RESULT IS " + easy_board._result)

    easy_board = MinesweeperPlayer("", "")
    easy_board._mines_count = 1
    easy_board._covered_cells_count = 10 * 10
    easy_board._rows = 10
    easy_board._columns = 10
    easy_board._result = ""
    easy_board._memo = {}
    easy_board._started_at = datetime.now()

    easy_board._uncovered_board = [["0","0","0","0","0","0","0","0","1","1"],
                                   ["0","0","0","0","0","0","0","0","1","X"],
                                   ["0","0","0","0","0","0","0","0","1","1"],
                                   ["0","0","0","0","0","0","0","0","0","0"],
                                   ["0","0","0","0","0","0","0","0","0","0"],
                                   ["0","0","0","0","0","0","0","0","0","0"],
                                   ["0","0","0","0","0","0","0","0","0","0"],
                                   ["0","0","0","0","0","0","0","0","0","0"],
                                   ["0","0","0","0","0","0","0","0","0","0"],
                                   ["0","0","0","0","0","0","0","0","0","0"]]

    easy_board._covered_board = [['*', '*', '*', '*', '*','*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*','*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                                 ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']
                                 ]

    print()
    print("=======================================")
    print("EASY BOARD BUT NOW LOSING")
    board_pretty_printer(easy_board._uncovered_board)
    print("=======================================")
    board_pretty_printer(easy_board._covered_board)
    print("=======================================")
    print("SELECTING 0, 0")
    print("=======================================")
    easy_board.make_move(0, 0)
    board_pretty_printer(easy_board._uncovered_board)
    print("=======================================")
    board_pretty_printer(easy_board._covered_board)
    print("COVERED COUNT IS " + str(easy_board._covered_cells_count))
    print("=======================================")
    print("SELECTING 1, 9")
    print("=======================================")
    easy_board.make_move(1, 9)
    board_pretty_printer(easy_board._uncovered_board)
    print("=======================================")
    board_pretty_printer(easy_board._covered_board)
    print("RESULT IS " + str(easy_board._result))
