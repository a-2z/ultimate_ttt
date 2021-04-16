import numpy as np
from enum import Enum


class GameState(Enum):
    INCOMPLETE = 0
    DRAW = -2
    O = -1
    X = 1


class Board:

    def __init__(self, size=3, ultimate=True):
        """
        Class constructor for tic-tac-toe board.
        """
        # number of boards (usually 3 x 3)
        self.board_num = size if ultimate else 1
        # size of each board (usually 3 x 3)
        self.board_size = size
        # full big board
        self.board = np.zeros(
            (self.board_num * self.board_size, self.board_num * self.board_size))
        # keeps track of which boards are won and by who
        self.won_boards = np.zeros((self.board_num, self.board_num))
        # X is 1, O is -1
        self.turn = 1
        # keeps track of how many turns have passed
        self.turns_played = 0
        self.result = GameState.INCOMPLETE

    def get_winner(self) -> GameState:
        return self.result

    @staticmethod
    def rep_tile(tile) -> str:
        if tile == 0:
            return " "
        return "X" if tile == 1 else "O"

    def get_index(self, global_coords, local_coords):

        return (global_coords[0] * self.board_num + local_coords[0],
                global_coords[1] * self.board_num + local_coords[1])

    def get_board(self, global_coords):
        """
        return the slice of the global board corresponding to the local board
        identified by global_coords.

        Parameter global_coords: a coordinate in (0, 0)...(2, 2)
        Returns: a board_size x board_size numpy array corresponding to 
        the specified local board.
        """
        return self.board[global_coords[0] * self.board_num:
                          global_coords[0] * self.board_num + self.board_size,
                          global_coords[1] * self.board_num:
                          global_coords[1] * self.board_num + self.board_size]

    def draw_board(self) -> str:
        """
        Returns a string representing the state of the board at a given time.
        """
        sep = "+---"
        row = "| {} "
        multiplier = self.board_size * self.board_num

        vfunc = np.vectorize(self.rep_tile)
        board_rep = vfunc(self.board)
        flat_board = np.ndarray.flatten(board_rep)

        unfilled = "\n".join([row * multiplier, sep * multiplier]
                             * (multiplier - 1) + [row * multiplier])
        return unfilled.format(*list(flat_board))

    def board_won(self, global_coords=(0, 0), win=False) -> int:
        """
        Check if a board was won and returns who won it
        """
        won_num = self.board_size
        board = self.get_board(global_coords)
        if win:
            board = self.won_boards

        # check rows
        row_array = np.sum(board, axis=0)
        max_idx = np.argmax(np.abs(row_array))
        if np.abs(row_array)[max_idx] == won_num:
            return np.sign(row_array[max_idx])

        # check cols
        col_array = np.sum(board, axis=1)
        max_idx = np.argmax(np.abs(col_array))
        if np.abs(col_array)[max_idx] == won_num:
            return np.sign(col_array[max_idx])

        # check diags
        diag_lr = np.trace(board)
        if diag_lr == won_num:
            return np.sign(diag_lr)

        diag_rl = np.trace(np.rot90(board))
        if diag_rl == won_num:
            return np.sign(diag_rl)

        return 0

    def board_drawn(self, global_coords):
        """
        Checks to see if the outcome of a local board is a draw
        """
        return (not self.check_win(board_won) and
                np.all(self.get_board(global_coords)))

    def check_win(self, global_coords) -> int:
        """
        First, see if the board at the given global_coords has been won
        Then, return if someone has won the entire game
        """
        self.won_boards[global_coords[0], global_coords[1]
                        ] = self.board_won(global_coords)

        if self.board_num == 1:
            return self.won_boards[0][0]
        else:
            return self.board_won(win=True)

    def full(self) -> bool:
        """
        Returns if the board is full (game is over)
        """
        return np.all(self.board)

    def next_turn(self): self.turn *= -1

    def available_moves(self, global_coords):
        """
        Return all available moves, considering that the last move directed 
        you to the board specified by global_coords.

        Returns: A list of tuples that indicate the vacant spaces on the 
        local board.
        """
        vacant = []
        loc = self.get_board(global_coords)
        if self.board_won(global_coords):
            return vacant
        for i in range(self.board_size):
            for j in range(self.board_size):
                if loc[i, j] != 0:
                    vacant.append(i, j)
        return vacant

        # TO DO

    def move(self, cell) -> bool:
        """
        Simulates a move on the gameboard based on which player's turn it is.
        Numbering starts in the top-left corner and proceeds in row-major
        order and is 0-indexed.

        Parameter cell: tuple of tuples specifying the coordinates of the board 
        and the loaction on the board.
        """
        # extract global and local position coordinates
        global_x, global_y = cell[0][0], cell[0][1]
        loc_x, loc_y = cell[1][0], cell[1][1]
        global_coords = cell[0]
        local_coords = cell[1]
        (x, y) = self.get_index(global_coords, local_coords)

        if self.won_boards[global_x, global_y] == 0 and self.board[x, y] == 0:
            self.board[x, y] = self.turn

            result = self.check_win(global_coords)
            self.result = GameState(result)
            if result == 0 and self.full():
                self.result = GameState.DRAW
            self.next_turn()

            return True
        else:
            return False
