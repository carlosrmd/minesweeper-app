# minesweeper-app

## Application description

Simple RESTful API server for the well-known minesweeper game. This server contains endpoints that allow clients create users, start games on behalf of some user and play the game. Games can be started, paused, resumed, played and finished.

The base public URL for interacting with the server is the following: http://34.72.16.104

There are two main API categories:

* Games API, with documentation at [/docs/games.md](https://github.com/carlosrmd/minesweeper-app/blob/master/docs/games.md)

* Users API, with documentation at [/docs/users.md](https://github.com/carlosrmd/minesweeper-app/blob/master/docs/users.md)

##### A common flow for a client's implementation would be the following:

* Show the player the list of registered users with endpoint `GET /users` 
* Allow player to select one of those users or create a new one with endpoint `POST /users`
* Once player is identified, show the list of all games registered in the system associated with the player's selected user with endpoint `GET /games?user_id=:user_id`. The interface would be able to show the current status of those games (paused or finished). Finished games have information about how they ended (victory, game lost or finished by user) and total spent time, so it could be showed.
* Allow player to select game to continue playing. The interface should not allow the user to select non-finished games since they can't be played and are there only for history purposes.
* Allow player to start a new game with endpoint `POST /games` with number of rows, number of columns and amount of mines in the body request.
* When a game is selected the interface can use the endpoint `GET /games/:game_id/state` to fetch the game's board and show it to the user.
* Allow player to interact with selected game by perform actions on specific cells, such as click on them or flag them, with the help of endpoint `PUT /games/:game_id/:action` and (row, column) coordinates on body request. The response of mentioned endpoint will be the new state of the game with the updated board after the action taken.
* Notice the player when its actions finish the game, like uncovering all non-mines cells or click on one mine cell.
* Allow the player to pause the game and stop playing or manually end the game and go back to the game's list view.

Library for integrating with Java minesweeper games projects: [minesweeper-client](https://github.com/carlosrmd/minesweeper-client)

-------------------
## Implementation notes

### Tech stack
Main used tools were [Python](https://www.python.org/) as programming language, [Flask](https://flask.palletsprojects.com/en/1.1.x) as web server framework and [MongoDB](https://www.mongodb.com/what-is-mongodb) as database.

### Algorithm's design
Algorithms were needed to perform the two main tasks: *Generate new board* with given parameters and *perform cell uncovering* for given board and (row, column) coordinates

##### Generating new board
At first stage, new boards are represented as list of lists of integers, initializated by zeroes. The first problem encountered was how to select n random distinct mine's coordinates in the new board, that looks like this (for a 3x3 board):

||||
|---|---|---|
| 0 | 0 | 0 |
| 0 | 0 | 0 |
| 0 | 0 | 0 |

The solution was to implement algorithm `generate_board(rows: int, columns: int, mines: int)` and `generate_random_mines_coordinates(rows: int, columns: int, mines: int)`.

The logic in random mines generation was to abstract the board as a enumeration of cells from `0` to `(rows * columns) - 1`, the following table shows this numeric representation of cells, where the number between parenthesis is the enumeration each cell receives:

||||
|---|---|---|
| 0 (0) | 0 (1) | 0 (2) |
| 0 (3) | 0 (4) | 0 (5) |
| 0 (6) | 0 (7) | 0 (8) |

Next step is select as many distinct numbers as mines the board needs. Let's say the previous board need two mines, the `generate_random_mines_coordinates` would receive the parameters and randomly select, for instance, number 3 and 7 from range `[0, 3*3-1]` and convert those numbers to (row, column) pair coordinates for the 4th and 8th mines in the board, which would be (1, 0) and (2, 1).

||||
|---|---|---|
| 0 | 0 | 0 |
| 0<- | 0 | 0 |
| 0 | 0<- | 0 |

Method `generate_random_mines_coordinates` works as a python [generator](https://en.wikipedia.org/wiki/Generator_(computer_programming)) used by `generate_board` so at the same time it's generating the random coordinates, method `generate_board` is inserting the new mines in the board by marking it as a mine and incrementing by one the value of every non-mine adjacent cell.

The result board would be:
||||
|---|---|---|
| 1 | 1 | 0 |
| X | 2 | 1 |
| 2 | X | 1 |

This algorithm generates the mines and insert them in the board in *O(total_mines)* time. At the end, the board is converted to a list of lists of characters since it becomes immutable.


##### Uncovering cells

A fully covered board is a list of lists of asterisks. If the cell the player selected for uncovering is not a mine, the algorithm `recursive_uncoverer(row: int, column: int)` will be called and will start replacing the asterisks for the actual vaules of the cell recursively. The base case is the uncovered cell is not the characer '0', the recursive case is the uncovered cell is a '0' and it will execute `recursive_uncoverer` for every adjacent cell.

The algorithm uses the dynamic programming technique [memoization](https://en.wikipedia.org/wiki/Memoization) in order to avoid method calls on already uncovered cells. The uncovering process is done in *O(total_cells)* time.

The result algorithms looks like this in pseudo-python:

```python
def recursive_uncoverer(row, col):
    memo.add(row, col)
    selected_char = uncovered_board[row][col]
    if selected_char == "0":
        # Recursive case, keep uncovering
        covered_board[row][col] = selected_char
        for adj_r, adj_c in get_adjacents():
            if (adj_r,adj_c) not in memo:
                recursive_uncoverer(adj_r, adj_c)
    else:
        # Base case, no need to keep uncovering
        covered_board[row][col] = selected_char
        
```

##### UPDATE

The recursive implementation was having Max recurssion problems while processing big boards (>10,000 cells) with few mines (lots of zeroes) so an iterative version was created and added to the `MinesweeperPlayer` class in order to avoid such problems. This version works similar but uses a queue approach to process cells and keeps the memoization to avoid repeating work.

The iterative version in pseudo-python looks like this:

```python
def recursive_uncoverer(row, col):
    queue.add(row, col)
    memo.add(row, col)
    while queue.not_empty():
        current_row, current_col = queue.pop(0)
        selected_char = uncovered_board[current_row][current_col]
        if selected_char == "0":
            covered_board[current_row][current_col] = selected_char
            for adj_r, adj_c in get_adjacents():
                if (adj_r,adj_c) not in memo:
                    memo.add(adj_r, adj_c)
                    queue.add(adj_r, adj_c)
        else:
            covered_board[current_row][current_col] = selected_char
```

### Server deployment

##### Current deployment

Server is deployed to GCP's [compute engine](https://cloud.google.com/compute) service. Configured to use python's [uWSG](https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/) as web server interface with [nginx](https://nginx.org/en/). MongoDB is running locally on the instance.

##### Deployment alternatives

A serverless solution would be using AWS [API Gateway](https://aws.amazon.com/api-gateway/), triggering [lambdas](https://aws.amazon.com/lambda/features/) that perform calls to a [DocumentDB](https://aws.amazon.com/documentdb/) instance, since all the operations the API currently performs are stateless.
