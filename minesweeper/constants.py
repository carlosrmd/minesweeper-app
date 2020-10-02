# Actions
PAUSE_GAME = "pause"
RESUME_GAME = "resume"
END_GAME = "end"
MOVE = "move"

# Statuses
STATUS_PAUSED = "PAUSED"
STATUS_ACTIVE = "ACTIVE"
STATUS_FINISHED = "FINISHED"

# Results
RESULT_FINISHED_BY_USER = "Finished by user"
RESULT_GAME_LOST = "Game lost"
RESULT_GAME_VICTORY = "Victory!"

MOVE_RED_FLAG = "FLAG"
MOVE_QUESTION_MARK = "QUESTION_MARK"
MOVE_CLICK = "CLICK"

flag_cell = {
    MOVE_RED_FLAG: "F",
    MOVE_QUESTION_MARK: "Q"
}

MSG_MISSING_FIELDS = "Error: missing required fields."
MSG_GAME_NOT_FOUND = "Error: game not found."
MSG_COMMAND_UNRECOGNIZED = "Error: command unrecognized."
MSG_USER_ALREADY_EXISTS = "Error: user name already exists."

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
