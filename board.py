import numpy as np
from copy import deepcopy
from enum import Enum

"""
This module implements a two-player Ultimate Tic-Tac-Toe game that can
be played from the command line. The rules of the game can be found
here: https://www.thegamegal.com/2018/09/01/ultimate-tic-tac-toe/.
"""


class State(Enum):
    """
    The State enum represents all of the possible outcomes of a
    two-player game with either a decisive outcome or a draw.
    """
    DRAW = -2
    INCOMPLETE = 0
    O = -1
    X = 1


class UltimateTTT:
    """
    ==============================Description=================================
    UltimateTTT contains all of the functionality for representing and playing
    a game of Ultimate Tic-Tac-Toe.

    ==============================Terminology=================================
    Local Board: A smaller, inner tic-tac-toe board.

    Global Board: The overall game state.

    Outcome: The result of either a local or global board, represented as a
    State value.

    Tile or Cell: One of the 9 spaces on a local board.

    Token: An 'X' or an 'O'

    ==============================Representation==============================
    Tokens:
    X = 1,
    O = -1,
    Empty = 0

    Global board: A 9x9 numpy array initialized to all 0s (empty tiles).

    All operations on local boards will take place through slicing of the
    global array board first. For this reason, some of the methods might
    require global coordinates, specifying one of the 9 local boards, and
    local coordinates, specifying a tile on a local board.

    State: A separate, 3x3 numpy array will be used to keep track of the
    winners of the local games. Each entry will be initialized to
    State.INCOMPLETE.

    Draws: In this implementation, draws can ONLY occur when a board is
    full and there is not a decisive winner. Even if a draw is guaranteed, a
    player sent to an incomplete and unwon local board must play in one of the
    vacant tiles.

    If a local board is drawn, it is counted for neither player. All lines
    containing a drawn local board are invalidated.
    """

    def __init__(self, dim=3):
        self.dim = dim
        self.board = np.zeros((self.dim, self.dim, self.dim, self.dim), dtype=np.int8)
        self.win_board = np.zeros((self.dim, self.dim), dtype=np.int8)    
        self.result = 0
        self.next_board = (None, None)

    def get_outcome(self):
        return self.result

    def compute_outcome(self, board):
        # check rows
        row_array = np.abs(np.sum(board, axis=0))
        max_idx = np.argmax(row_array)
        if row_array[max_idx] == won_num:
            return board[max_idx,0]

        # check cols
        col_array = np.abs(np.sum(board, axis=1))
        max_idx = np.argmax(col_array)
        if col_array[max_idx] == won_num:
            return board[0, max_idx]

        # check diags
        diag_lr = np.abs(np.trace(board))
        if diag_lr == won_num:
            return board[0,0]

        diag_rl = np.abs(np.trace(np.rot90(board)))
        if diag_rl == won_num:
            return board[0,self.dim-1]

        return 0

    def move(self, move_array, player):
        globi, globj, loci, locj = move_array[0], move_array[1], move_array[2], move_array[3]

        self.board[globi, globj, loci, locj] = player

        self.win_board[globi, globj] = self.compute_outcome(self.board[globi, globj, :, :])

        alt_win_board = np.copy(self.win_board)
        alt_win_board[self.win_board == -2] = 0

        self.result = self.compute_outcome(alt_win_board)

        if self.result == 0 and np.all(self.win_board):
            self.result = -2

        self.next_board = (loci, locj)

    def availible_moves_4d(self):
        # all open spots on the board, not caring if a given local board can be legally played on
        availible_moves = self.board == 0

        if self.next_board != (None,None):
            # a 3x3 zero matrix
            zero_board = np.zeros((self.dim, self.dim))
            # the local boards we can't legally play on
            turn_to_zero = np.ones((self.dim, self.dim))

            if self.win_board[self.next_board] == 0:
                # if next_board is incomplete, can only play there
                turn_to_zero[self.next_board] = 0
            else:
                # if next_board is complete, can play in any incomplete board
                turn_to_zero = self.win_board != 0

            # set the value for local boards we can't legally play on to zero
            availible_moves[turn_to_zero.astype(bool)] = zero_board

        return availible_moves

    def availible_moves_numpy(self):
        availible_4d = self.availible_moves_4d()
        return np.argwhere(availible_4d == 1)