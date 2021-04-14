import numpy as np
from enum import Enum


class GameState(Enum):
    INCOMPLETE = 0
    DRAW = 1
    O = 2
    X = 3


class Board:

    def __init__(self) -> None:
        """
        Class constructor for a single tic-tac-toe board.
        """
        # initialize an empty 3x3 array
        self.board = np.full((3, 3), None)
        # X is True, O is false
        self.turn = True
        # keeps track of how many turns have passed
        self.turns_played = 0
        self.result = GameState.INCOMPLETE

    def get_winner(self) -> GameState:
        return self.result

    @staticmethod
    def _rep_tile(tile) -> str:
        if tile is None:
            return " "
        return "X" if tile else "O"

    def draw_board(self) -> str:
        """
        Returns a string representing the state of the board at a given time.
        """
        state = np.ndarray.flatten(self.board)
        for i in range(len(state)):
            if state[i] == None:
                state[i] == i
        # horizontal separator
        sep = "---+---+---"
        row = " {} | {} | {} "
        # create a formatted string without the tile values filled in
        unfilled = "\n".join([row, sep] * 2 + [row])
        return unfilled.format(*list(map(Board._rep_tile, state)))

    def _is_won(self) -> bool:
        """
        Returns a GameState value
        Precondition: None
        """
        # Not enough turns to win
        if self.turns_played < 6:
            return False

        # checks if any rows or columns have been won
        for index, row in enumerate(self.board):
            col = [i for i in self.board[:, index]]
            if (len(set(row)) > 1 or len(set(col)) > 1):
                continue
            elif row[index] is not None:
                return True

        # checks if any diagonals have been won
        lr_diagonal = [self.board[0, 0], self.board[1, 1], self.board[2, 2]]
        rl_diagonal = [self.board[2, 0], self.board[1, 1], self.board[0, 2]]
        if len(set(lr_diagonal)) > 1 or len(set(rl_diagonal)) > 1:
            return False
        return self.board[1, 1] is not None

    def move(self, cell: tuple[int, int]) -> bool:
        """
        Simulates a move on the gameboard based on which player's turn it is.
        Numbering starts in the top-left corner and proceeds in row-major
        order and is 0-indexed.

        Parameter cell: The coordinate of the space to play in; must be
        between (0,0) and (2,2)
        Returns: True if the move was successful and False otherwise
        """
        if self.board[cell] is None and self.result == GameState.INCOMPLETE:
            self.board[cell] = self.turn
            self.turn = not self.turn
            if self._is_won():
                self.result = GameState.X if self.turn else GameState.O
            if self.turns_played == 9:
                self.result = GameState.DRAW
            return True
        return False
