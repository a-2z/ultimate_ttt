import numpy as np

# 0 -> incomplete
# 1 -> X win
# -1 -> O win
# -2 -> draw

class Board():
    def __init__(self, dim=3):
        self.dim = dim
        self.board = np.zeros((self.dim, self.dim, self.dim, self.dim), dtype=np.int8)
        self.win_board = np.zeros((self.dim, self.dim), dtype=np.int8)    
        self.result = 0
        self.next_board = (None, None)

    def copy(self):
        new_board = Board(self.dim)
        new_board.board = np.copy(self.board)
        new_board.win_board = np.copy(self.win_board)
        new_board.result = self.result
        new_board.next_board = self.next_board
        return new_board

    def undo_move(self, move):
        if move == None:
            pass
        else:
            glob = (move[0], move[1])
            self.board[move] = 0
            self.win_board[glob] = 0
            self.result = 0

    def flatten_board(self, board):
        flat = np.zeros(0)
        for i in range(self.dim):
            for k in range(self.dim):
                flat = np.concatenate((flat, board[i,:,k,:]), axis=None)

        return flat

    def twoD_rep(self):
        return self.flatten_board(self.board).reshape((self.dim**2,self.dim**2))

    def get_outcome(self):
        return self.result

    def get_state(self):
        return np.copy(self.board)

    def get_win_board(self):
        return np.copy(self.win_board)

    def compute_outcome(self, board):

        # check cols
        row_array = np.abs(np.sum(board, axis=0))
        max_idx = np.argmax(row_array)
        # print("col", row_array, max_idx)
        if row_array[max_idx] == self.dim:
            return board[0, max_idx]

        # check rows
        col_array = np.abs(np.sum(board, axis=1))
        max_idx = np.argmax(col_array)
        # print("row", col_array, max_idx)
        if col_array[max_idx] == self.dim:
            return board[max_idx, 0]

        # check diags
        diag_lr = np.abs(np.trace(board))
        # print("diag", diag_lr)
        if diag_lr == self.dim:
            return board[0,0]

        diag_rl = np.abs(np.trace(np.rot90(board)))
        # print("diag", diag_rl)
        if diag_rl == self.dim:
            return board[0,self.dim-1]

        return -2 if np.all(board) else 0

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

    def available_moves_4d(self):
        # all open spots on the board, not caring if a given local board can be legally played on
        available_moves = self.board == 0

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
            available_moves[turn_to_zero.astype(bool)] = zero_board

        return available_moves

    def available_moves_numpy(self):
        available_4d = self.available_moves_4d()
        return np.argwhere(available_4d == 1)