import numpy as np
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

    def __init__(self, size=3, num_boards=3):
        """
        Creates a fresh instance of the game with an empty board and with
        X to move.
        """
        # set the board size (usually 3)
        self.board_size = size
        # the number of local boards in a row or column
        self.board_num = num_boards
        # make the game board
        self.board = np.zeros((self.board_num*self.board_size,
                               self.board_num*self.board_size))
        # properties of local boards
        self.board_data = np.full((3, 3),
                                  {"num_moves": 0,
                                  "outcome": State.INCOMPLETE})
        # the current player's token
        self.turn = 1
        # the result of the overall game
        self.result = State.INCOMPLETE
        # global coordinates of the local board to play in
        self.next_board: tuple[int, int] = None
        # the sequence of moves played thus far
        self.moves = []

    def __str__(self, pretty_print=True) -> str:
        """
        Returns a string representation of the global board.

        Parameter pretty_print: whether formatting should be added to the
        global board to make it resemble 9 separate tic-tac-toe boards with
        separators in between.
        """
        if pretty_print:
            for row in range(self.board_size):
                for col in range(self.board_size):
                    local_board = self._get_board((row, col))
                    print('\n'.join([''.join(['{:3}'.format(i) for i in r])
                                     for r in local_board]))
                print('---------------------------------------------------')
            return ""
        else:
            stringify = np.vectorize(
                UltimateTTT.str_token, otypes=[np.ndarray])
            return str(stringify(self.board))
        return str(stringify(self.board))

    @staticmethod
    def mark_outcome(board_string: str, outcome: int) -> str:
        """
        Returns a string representing a board with an X through it or a 
        circle around it depending on its outcome.
        """
        rows = board_string.split("\n")
        width, height = len(rows)[0], len(rows)
        if outcome == 0:
            return board_string
        centerx = width // 2
        centery = height // 2
        marker = (centerx - 1) * " " + str_token(outcome) + centerx * " "
        return ([" "]*(centery - 1) + marker + [" "] * centery).join("\n")

    @staticmethod
    def str_local_board(board) -> str:
        """
        Returns a string representing the state of a 3x3 tic-tac board
        """
        state = np.ndarray.flatten(board)
        for i in range(len(state)):
            if state[i] == None:
                state[i] == i
        # horizontal separator
        sep = "---+---+---"
        row = " {} | {} | {} "
        # create a formatted string without the tile values filled in
        unfilled = "\n".join([row, sep] * 2 + [row])
        return unfilled.format(*list(map(Board._str_token, state)))

    @ staticmethod
    def str_token(token: int) -> str:
        """
        Returns the string representation of a token.
        """
        if token == 0:
            return " "
        return "X" if token == 1 else "O"

    def global_outcome(self) -> State:
        """
        Returns the outcome of a global board.
        """
        return self.result

    def local_outcome(self, global_coords) -> State:
        """
        Returns the outcome of a local board.
        """
        return self.board_data[global_coords]["outcome"]

    def set_local_outcome(self, global_coords, outcome) -> None:
        """
        Sets the outcome of a local board to a state
        """
        self.board_data[global_coords]["outcome"] = outcome

    def get_index(self, global_coords, local_coords):
        """
        Returns the index of a tile within the 9x9 board based on its local
        coordinates and the global coordinates of the board that it's in.
        """
        return (global_coords[0] * self.board_num + local_coords[0],
                global_coords[1] * self.board_num + local_coords[1])

    def _get_board(self, global_coords):
        """
        The slice of the global board corresponding to the local board
        identified by global_coords.

        Parameter global_coords: a coordinate in (0, 0)...(2, 2)
        Returns: a board_size x board_size numpy array corresponding to
        the specified local board.
        """
        return self.board[global_coords[0] * self.board_num: global_coords[0] * self.board_num + self.board_size,
                          global_coords[1] * self.board_num: global_coords[1] * self.board_num + self.board_size]

    def _change_turn(self) -> None:
        """
        Sets the turn equal to the other player.
        """
        self.turn *= -1

    def move(self, tile: tuple[tuple[int], tuple[int]]) -> bool:
        """
        Simulates a move on the gameboard based on which player's turn it is.
        Numbering of both local and global spaces starts in the top-left corner
        and proceeds in 0-indexed, row-major order.

        Parameter tile: A tuple of (global_coord, local_coord), which places
        the token of the current player in the corresponding tile.
        """
        if not self.is_legal(tile):
            return False
        else:
            glob, loc = tile[0], tile[1]
            idx = self.get_index(glob, loc)
            # set the board for the opponent to play in
            self.next_board = loc
            # track the overall move history
            self.moves.append(tile)
            # place the appropriate token on the board
            self.board[idx] = self.turn
            self.board_data[glob]["num_moves"] += 1
            self._change_turn()
            board_outcome = self.compute_winner(global_coords=glob)
            total_outcome = self.compute_winner()
            self.set_local_outcome(glob, board_outcome)
            self.result = total_outcome
            return True

    def _tokenize_outcome(self, outcome) -> int:
        """
        Returns the int "token" (-1, 0, or 1) corresponding to the outcome of
        a local board for use in the representation of the global board.
        """
        if outcome == State.DRAW:
            return 0
        else:
            return outcome.value

    def _assemble_global(self):
        """
        Abstracts the global 9x9 board into a 3x3 board, with each tile
        representing the outcome of each local board.

        Returns: A 3x3 numpy array representing a tic-tac-toe board
        """
        glob = np.zeros((3, 3))
        for i in range(self.board_num):
            for j in range(self.board_num):
                # result of a local board is converted into a token
                glob[i, j] = self._tokenize_outcome(self.local_outcome((i, j)))
        return glob

    def compute_winner(self, global_coords=None) -> State:
        """
        Computes the winner of either a local board or the overall game.

        If global_coord is None, the computation is performed for the
        overall game. The 9x9 board will be abstracted into a 3x3 array with
        the outcomes of each local board.

        Returns the State corresponding to an outcome
        """
        board = None
        if global_coords is not None:
            board = self._get_board(global_coords)
            if self.board_data[global_coords]["num_moves"] < 5:
                return State.INCOMPLETE
        else:
            board = self._assemble_global()

        won_num = self.board_size

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

        return State.INCOMPLETE if 0 in board else State.DRAW

    def _legal_global(self, gc) -> bool:
        board_outcome = self.local_outcome(gc) == State.INCOMPLETE
        first_move = self.next_board == None
        # first move or the directed board to move to
        if first_move or (self.next_board == gc and board_outcome):
            return True
        return False

    def is_legal(self, move: tuple[tuple[int], tuple[int]]) -> bool:
        """
        Returns whether or not a move is legal based on the board the player
        has been redirected to. If the player is redirected to a board whose
        outcome is known, the move must be played on an empty tile in any
        of the other eligible boards.

        A move is not legal if the game is over.
        """
        global_coords, local_coords = move[0], move[1]
        if self._legal_global(global_coords):
            return self._get_board(global_coords)[local_coords] == 0
        else:
            return False

    def available_moves(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Returns the list of all moves available to the player.
        """
        available = []

        if self.global_outcome() == State.INCOMPLETE:
            for board in self.available_boards():
                available += map(lambda tile: (board, tile),
                                 self.available_tiles(board))
        return available

    def available_boards(self) -> list[tuple[int, int]]:
        """
        Returns a list of tuples corresponding to the coordinates of local
        boards that can be played in on any given turn.
        """
        available = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self._legal_global((i, j)):
                    available.append((i, j))
        return available

    def available_tiles(self, global_coords) -> list[tuple[int, int]]:
        """
        Return all of the tiles on a specific incomplete board that can be
        moved to.

        Returns: A list of tuples that indicate the vacant spaces on the
        local board (empty if none available).
        """
        available = []
        in_progress = (self.local_outcome(global_coords) == State.INCOMPLETE)
        if in_progress:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self._get_board(global_coords)[i, j] == 0:
                        available.append((i, j))
        return available
