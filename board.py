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
        # self.board = np.zeros((self.dim ** 2, self.dim ** 2))
        self.board = np.zeros((self.dim, self.dim, self.dim, self.dim))
        # properties of local boards
        self.num_moves = np.zeros((self.dim, self.dim))
        self.win_board = np.full((self.dim, self.dim), State.INCOMPLETE)                      
        # the current player's token
        self.turn = 1
        # the result of the overall game
        self.result = State.INCOMPLETE
        # global coordinates of the local board to play in
        self.next_board: tuple[int, int] = None
        # the sequence of moves played thus far
        self.moves = []

    def set_state(self, reference):
        """
        Modifies the game state to mirror a reference state in place.

        This is useful for creating copies without having to create entirely
        new objects.
        """
        self.board = reference.board.copy() 
        self.num_moves = reference.num_moves
        self.win_board = reference.win_board.copy() 
        self.turn = reference.turn
        self.result = deepcopy(reference.result)
        self.next_board = reference.next_board
        self.moves = deepcopy(reference.moves)

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

            unfilled = "\n".join(self.dim * ([multiplier * sep, self.dim * (row + (self.dim-1) * row_clear)] + (self.dim-1) * [self.dim * (sep_clear + (self.dim-1) * clear), self.dim * (row + (self.dim-1) * row_clear)]))
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
        Returns the board as a two dimensional array, as opposed to a 4 dimensional one
        """
        return _flatten_board(self.board).reshape((self.dim,self.dim))

    def _mark_outcome(self, board_rep):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.win_board[i,j] == State.DRAW:
                    board_rep[i,j,:,:] = np.array([["|","-"," "],["|", " ", "]"],["|","-"," "]])
                elif self.win_board[i,j] == State.X:
                    board_rep[i,j,:,:] = np.array([["\\"," ","/"],[" ", "X", " "],["/"," ","\\"]])
                elif self.win_board[i,j] == State.O:
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
        return self.win_board[global_coords]

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
            glob, loc = tile[0], tile[1]
            # set the board for the opponent to play in
            self.next_board = loc
            # track the overall move history
            self.moves.append(tile)
            # place the appropriate token on the board (if indices in range)
            try:
                self.board[glob[0], glob[1], loc[0], loc[1]] = self.turn
            except:
                return False

            self.num_moves[glob] += 1
            self._change_turn()

            # compute winning stuff
            self.win_board[glob] = self._compute_winner(glob)
            self.result = self._compute_winner()

            return True

    def _outcome_to_num(self, state):
        if state == State.DRAW or state == State.INCOMPLETE:
            return 0
        elif state == State.X:
            return 1
        else:
            return -1

    def _compute_winner(self, global_coords=None) -> State:
        """
        Computes the winner of either a local board or the overall game.

        If global_coord is None, the computation is performed for the
        overall game. The 9x9 board will be abstracted into a 3x3 array with
        the outcomes of each local board.

        Returns the State corresponding to an outcome
        """
        vfunc = np.vectorize(self._outcome_to_num)

        board = vfunc(self.win_board) if global_coords == None else self.board[global_coords[0],global_coords[1],:,:]

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
        if diag_lr == won_num:
            return State(np.sign(diag_lr))

        diag_rl = np.trace(np.rot90(board))
        if diag_rl == won_num:
            return State(np.sign(diag_rl))

        if np.all(board) or (global_coords == None and not np.any(self.win_board == State.INCOMPLETE)):
            return State.DRAW
        else:
            return State.INCOMPLETE

    def _legal_global(self, gc) -> bool:
        if self.next_board == None:
            return True
        elif self.win_board[gc[0],gc[1]] != State.INCOMPLETE:
            return False
        else:
            if gc == self.next_board:
                return True
            else:
                return False if self.win_board[self.next_board[0], self.next_board[1]] == State.INCOMPLETE else True

    def _is_legal(self, move) -> bool:
        """
        Returns whether or not a move is legal based on the board the player
        has been redirected to. If the player is redirected to a board whose
        outcome is known, the move must be played on an empty tile in any
        of the other eligible boards.

        A move is not legal if the game is over.
        """
        global_coords, local_coords = move[0], move[1]
        if self._legal_global(global_coords):
            return self.board[global_coords[0], global_coords[1], local_coords[0], local_coords[1]] == 0
        else:
            return False

    def available_moves(self):
        """
        Returns the list of all moves available to the player.
        """
        available = []

        if self.result == State.INCOMPLETE:
            for board in self.available_boards():
                available += map(lambda tile: (board, tile),
                                 self.available_tiles(board))
        return available

    def available_boards(self):
        """
        Returns a list of tuples corresponding to the coordinates of local
        boards that can be played in on any given turn.
        """
        available = []
        for i in range(self.dim):
            for j in range(self.dim):
                if self._legal_global((i, j)):
                    available.append((i, j))
        return available

    def available_tiles(self, global_coords):
        """
        Return all of the tiles on a specific incomplete board that can be
        moved to.

        Returns: A list of tuples that indicate the vacant spaces on the
        local board (empty if none available).
        """
        available = []
        if self.win_board[global_coords] == State.INCOMPLETE:
            for i in range(self.dim):
                for j in range(self.dim):
                    if self.board[global_coords[0], global_coords[1], i, j] == 0:
                        available.append((i, j))
        return available
