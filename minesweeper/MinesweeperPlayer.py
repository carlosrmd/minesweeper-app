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
        self._iterative_uncoverer(r, c)
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

    def _iterative_uncoverer(self, r, c):
        cell_queue = [(r, c)]
        self._memo["%s-%s" % (r, c)] = 1
        while cell_queue:
            (current_r, current_c) = cell_queue.pop(0)
            selected_char = self._uncovered_board[current_r][current_c]
            if selected_char == "0":
                self._covered_board[current_r][current_c] = selected_char
                self._covered_cells_count -= 1
                for neighbor_r, neighbor_c in get_valid_neighbors(current_r, current_c, self._rows, self._columns):
                    if "%s-%s" % (neighbor_r, neighbor_c) not in self._memo:
                        rc = "%s-%s" % (neighbor_r, neighbor_c)
                        self._memo[rc] = 1
                        cell_queue.append((neighbor_r, neighbor_c))
            else:
                self._covered_board[current_r][current_c] = selected_char
                self._covered_cells_count -= 1
