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

    def __init__(self, dim=3, extra=3):
        """
        Creates a fresh instance of the game with an empty board and with
        X to move.
        """
        # set dimensions of global board and local boards (they are the same dimensions)
        self.dim = dim
        # make the game board
        self.board = np.zeros((self.dim, self.dim, self.dim, self.dim))
        self.win_board = np.zeros((self.dim, self.dim))                     
        # the current player's token
        self.turn = 1
        # the result of the overall game
        self.result = State.INCOMPLETE
        # global coordinates of the local board to play in
        self.next_board = None
        self.last_move = np.zeros(4) - 1

    def set_state(self, reference):
        """
        Modifies the game state to mirror a reference state in place.

        This is useful for creating copies without having to create entirely
        new objects.
        """
        self.board = reference.board.copy()
        self.win_board = reference.win_board.copy() 
        self.turn = reference.turn
        self.result = deepcopy(reference.result)
        self.next_board = reference.next_board
        self.last_move = reference.last_move

    def __str__(self, pretty_print=True) -> str:
        """
        Returns a string representation of the global board.

        Parameter pretty_print: whether formatting should be added to the
        global board to make it resemble 9 separate tic-tac-toe boards with
        separators in between.
        """
        if pretty_print:
            sep = "+---"
            row = "| {} "
            sep_clear = "+   "
            clear = "    "
            row_clear = "  {} "

            multiplier = self.dim * self.dim

            vfunc = np.vectorize(self._str_token)
            board_rep = vfunc(self.board)
            board_rep = self._mark_outcome(board_rep)

            flat_board = self._flatten_board(board_rep)

            unfilled = "\n".join(self.dim * ([multiplier * sep, 
            self.dim * (row + (self.dim-1) * row_clear)] + (self.dim-1) * 
            [self.dim * (sep_clear + (self.dim-1) * clear), 
            self.dim * (row + (self.dim-1) * row_clear)]))
            return unfilled.format(*list(flat_board))
        else:
            stringify = np.vectorize(UltimateTTT.str_token, otypes=[np.ndarray])
            return str(stringify(self.board))

    def _flatten_board(self, board):
        flat = np.zeros(0)
        for i in range(self.dim):
            for k in range(self.dim):
                flat = np.concatenate((flat, board[i,:,k,:]), axis=None)
        return flat

    def twoD_rep(self):
        """
        Returns the board as a two dimensional array, 
        as opposed to a 4 dimensional one
        """
        return _flatten_board(self.board).reshape((self.dim,self.dim))

    def _mark_outcome(self, board_rep):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.win_board[i,j] == -2:
                    board_rep[i,j,:,:] = np.array([["|","-"," "],["|", " ", "]"],["|","-"," "]])
                elif self.win_board[i,j] == 1:
                    board_rep[i,j,:,:] = np.array([["\\"," ","/"],[" ", "X", " "],["/"," ","\\"]])
                elif self.win_board[i,j] == -1:
                    board_rep[i,j,:,:] = np.array([["/","-","\\"],["|", " ", "|"],["\\","-","/"]])
        return board_rep

    @ staticmethod
    def _str_token(token: int) -> str:
        """
        Returns the string representation of a token.
        """
        if token == 0:
            return " "
        return "X" if token == 1 else "O"

    def get_board():
        return self.board

    def global_outcome(self) -> State:
        """
        Returns the outcome of a global board.
        """
        return self.result

    def local_outcome(self, global_coords) -> State:
        """
        Returns the outcome of a local board.
        """
        return State(self.win_board[global_coords])

    def _set_local_outcome(self, global_coords, outcome) -> None:
        """
        Sets the outcome of a local board to a state
        """
        self.win_board[global_coords] = outcome

    def _change_turn(self) -> None:
        """
        Sets the turn equal to the other player.
        """
        self.turn *= -1

    def move(self, tile) -> bool:
        """
        Simulates a move on the gameboard based on which player's turn it is.
        Numbering of both local and global spaces starts in the top-left corner
        and proceeds in 0-indexed, row-major order.

        Parameter tile: A tuple of (global_coord, local_coord), which places
        the token of the current player in the corresponding tile.
        """

        if not self._is_legal(tile):
            return False
        else:
            self.last_move = tile
            globi, globj, loci, locj = tile[0], tile[1], tile[2], tile[3]
            # set the board for the opponent to play in
            self.next_board = (loci, locj)
            # place the appropriate token on the board (if indices in range)
            try:
                self.board[globi, globj, loci, locj] = self.turn
            except:
                return False

            self._change_turn()

            # compute winning stuff
            self.win_board[globi,globj] = self._compute_winner_local_board((globi, globj))
            self.result = State(self._compute_winner_win_board())

            return True

    def _winboard_to_computable(self):
        """ 
        Makes a copy of the win_board where draws are of value 0
        """
        # make a copy because we dont want to edit the actual win_board
        new_win_board = np.copy(self.win_board)
        # set to 0 whereever it is a draw
        new_win_board[self.win_board == -2] = 0
        return new_win_board

    def _compute_winner_win_board(self):
        """ 
        Returns the value of the state of the win board
        """

        board = self._winboard_to_computable()
        won_num = self.dim

        # check rows
        row_array = np.sum(board, axis=0)
        max_idx = np.argmax(np.abs(row_array))
        if np.abs(row_array)[max_idx] == won_num:
            return State(np.sign(row_array[max_idx]))

        # check cols
        col_array = np.sum(board, axis=1)
        max_idx = np.argmax(np.abs(col_array))
        if np.abs(col_array)[max_idx] == won_num:
            return State(np.sign(col_array[max_idx]))

        # check diags
        diag_lr = np.trace(board)
        if np.abs(diag_lr) == won_num:
            return State(np.sign(diag_lr))

        diag_rl = np.trace(np.rot90(board))
        if np.abs(diag_rl) == won_num:
            return State(np.sign(diag_rl))

        if np.all(self.win_board):
            return -2
        else:
            return 0

    def _compute_winner_local_board(self, global_coords):
        """
        Returns the value of the state of the local board corresponding to global coordinates
        """
        won_num = self.dim
        i = global_coords[0]
        j = global_coords[1]

        # check rows
        row_array = np.sum(self.board[i,j,:,:], axis=0)
        max_idx = np.argmax(np.abs(row_array))
        if np.abs(row_array)[max_idx] == won_num:
            return np.sign(row_array[max_idx])

        # check cols
        col_array = np.sum(self.board[i,j,:,:], axis=1)
        max_idx = np.argmax(np.abs(col_array))
        if np.abs(col_array)[max_idx] == won_num:
            return np.sign(col_array[max_idx])

        # check diags
        diag_lr = np.trace(self.board[i,j,:,:])
        if diag_lr == won_num:
            return np.sign(diag_lr)

        diag_rl = np.trace(np.rot90(self.board[i,j,:,:]))
        if diag_rl == won_num:
            return np.sign(diag_rl)

        if np.all(self.board[i,j,:,:]):
            return -2
        else:
            return 0

    def _legal_global(self, gc) -> bool:
        """
        Returns whether or not a local board can be played on
        """
        if self.next_board == None:
            return True
        elif self.win_board[gc[0],gc[1]] != 0:
            return False
        else:
            if gc == self.next_board:
                return True
            else:
                return False if self.win_board[self.next_board[0], self.next_board[1]] == 0 else True

    def _is_legal(self, move) -> bool:
        """
        Returns whether or not a move is legal based on the board the player
        has been redirected to. If the player is redirected to a board whose
        outcome is known, the move must be played on an empty tile in any
        of the other eligible boards.

        A move is not legal if the game is over.
        """
        globi, globj, loci, locj = move[0], move[1], move[2], move[3]
        if self._legal_global((globi, globj)):
            return self.board[globi, globj, loci, locj] == 0
        else:
            return False

    def available_moves_4d(self):
        """
        Returns a 3x3x3x3 array where a 1 means a move can be played in that location, and a 0 means it can't
        """
        
        # all open spots on the board, not caring if a given local board can be legally played on
        available_moves = self.board == 0

        if self.next_board != None:
            (next_globi, next_globj) = self.next_board
            # a 3x3 zero matrix
            zero_board = np.zeros((self.dim, self.dim))
            # the local boards we can't legally play on
            turn_to_zero = np.ones((self.dim, self.dim))

            if self.win_board[next_globi, next_globj] == 0:
                # if next_board is incomplete, can only play there
                turn_to_zero[next_globi, next_globj] = 0
            else:
                # if next_board is complete, can play in any incomplete board
                turn_to_zero = self.win_board != 0

            # set the value for local boards we can't legally play on to zero
            available_moves[turn_to_zero.astype(bool)] = zero_board

        return available_moves

    def available_moves(self):
        """
        Returns a nx4 array indicating the coordinates of all the available moves, where n is the number of available moves
        """
        available_4d = self.available_moves_4d()
        return np.argwhere(available_4d == 1)