import numpy as np

def end_value(outcome):
  if outcome == -2:
    return 0
  return 100000

def plus_heuristic_fun(local_heuristic, global_heuristic, player):
  heuristic_state = np.zeros((3,3,3,3))
  for i in range(3):
    for j in range(3):
      heuristic_state[i,j,:,:] = local_heuristic
  def fun(board):
    state = board.get_state()
    state[state == -player] = 0
    win_board = board.get_win_board()
    win_board[np.logical_or(win_board == player, win_board == -2)] = 0
    return np.sum(heuristic_state * state) + np.sum(global_heuristic * win_board)
  return fun

def plus_neg_heuristic_fun(local_heuristic, global_heuristic, player):
  heuristic_state = np.zeros((3,3,3,3))
  for i in range(3):
    for j in range(3):
      heuristic_state[i,j,:,:] = local_heuristic
  def fun(board):
    state = board.get_state()
    win_board = board.get_win_board()
    win_board[win_board == -2] = .5 * player
    return np.sum(heuristic_state * state) + np.sum(global_heuristic * win_board)
  return fun

def attack_heuristic_fun(local_heuristic, attack_heuristic, player):
  heuristic_state = np.zeros((3,3,3,3))
  for i in range(3):
    for j in range(3):
      heuristic_state[i,j,:,:] = local_heuristic
  def fun(board):
    state = board.get_state()
    win_board = board.get_win_board()

    win_board[win_board == -2] = 0

    row_array = np.sum(win_board, axis=0)
    col_array = np.sum(win_board, axis=1)
    diag_lr = np.trace(win_board)
    diag_rl = np.trace(np.rot90(win_board))

    sum = 0

    for i in range(row_array.shape[0]):
      if np.abs(row_array[i]) == 1:
        sum += attack_heuristic[0] * row_array[i]
      elif np.abs(row_array[i]) == 2:
        sum += attack_heuristic[1] * row_array[i]

    for i in range(col_array.shape[0]):
      if np.abs(col_array[i]) == 1:
        sum += attack_heuristic[0] * col_array[i]
      elif np.abs(col_array[i]) == 2:
        sum += attack_heuristic[1] * col_array[i]

    if np.abs(diag_lr) == 1:
      sum += attack_heuristic[0] * diag_lr
    elif np.abs(diag_lr) == 2:
      sum += attack_heuristic[1] * diag_lr

    if np.abs(diag_rl) == 1:
      sum += attack_heuristic[0] * diag_rl
    elif np.abs(diag_rl) == 2:
      sum += attack_heuristic[1] * diag_rl

    return np.sum(heuristic_state * state) + sum
  return fun

local_h = np.array([[2,1,2],[1,3,1],[2,1,2]])
global_h = np.array([[8,6,8],[6,10,6],[8,6,8]])
attack_h = np.array([4,5])