# Games endpoints

## GET /games

List games for existing user

**Query param** : `user_name`


### Success Response

**Code** : `200 OK`

**Response**


```json
[
    {
        "game_id": "string",
        "status": "string"
    }
]
```

### Not found Response

**Code** : `404 Not Found`

**Response**


```json
{
    "msg": "User not found"
}
```

## POST /games
Create new game for existing user

**Request body:**
```json
{
    "user_id": "string",
    "n_rows": "int",
    "n_cols": "int",
    "n_mines": "int"
}
```
### Success response
**Code** : `200 Ok`

**Response**

```json
{
    "game_id": "string"
}
```

### Bad sizes response
**Code** : `400 Bad request`

**Response**

```json
{
    "msg": "Bad size"
}
```

### User not found response
**Code** : `404 Not found`

**Response**

```json
{
    "msg": "User not found"
}
```


## GET /games/:game_id/state

Get state of existing game.

**Path param** : `game_id`

### Success response
**Code** : `200 Ok`

**Response**

```json
{
    "board": ["string"],
    "status": "string",
    "result": "string"
}
```
**Notes**

* `board` is a list of strings that represents the board as a matrix of characters.
* `status` could be: ACTIVE, PAUSED or FINISHED.
* `result` will be in the response
body only if status is FINISHED.

### Game not found response

**Code** : `404 Not Found`

**Response**

```json
{
    "msg": "Game not found"
}
```

### POST /games/:game_id/:command

Endpoint to interact with existing game. User could make a move, pause or resume the game.

**Path params**

* **game_id**: Id of the game
* **command**: Either `move`, `pause` or `resume`

**Request body: (only for `move` command)**
```json
{
    "row": "int",
    "column": "int",
    "move_type": "int"
}
```
* `row` and `column` determines the position of the affected cell.
* `move_type`: Could be `FLAG`, `QUESTION_MARK` or `CLICK`.

### Success Response

**Code** : `200 OK`

**Response**

State response (same as the `GET /games/:game_id/state` success response).

### Game not found response

**Code** : `404 Not Found`

**Response**

```json
{
    "msg": "Game not found"
}
```

### Invalid position response

Happens if the selected position is outside the board.

**Code** : `400 Bad request`

**Response**

```json
{
    "msg": "Invalid position"
}
```