from board import *
import numpy as np
import time
import random

class Agent(object):
  def get_player(self):
    raise NotImplementedError

  def make_move(self, board):
    raise NotImplementedError

  def reset(self):
    pass

class RandomAgent(Agent):
  def __init__(self, player):
    self.player = player

  def get_player(self):
    return self.player

  def make_move(self, board):
    potential_moves = board.availible_moves_numpy()
    choice = np.random.choice(potential_moves.shape[0], 1)[0]
    move = potential_moves[choice]
    board.move(move, self.player)
    return move

class TimedMinmaxAgent(Agent):
  def __init__(self, player, max_time, end_value, heuristic):
    self.player = player
    self.max_time = max_time
    self.end_value = end_value
    self.heuristic = heuristic

  def get_player(self):
    return self.player

  def make_move(self, board):
    s_time = time.time()
    depth = 0
    while (time.time() - s_time) < self.max_time:
      depth += 1
      alpha = float("-inf")
      beta = float("inf")
      score, best_move = self.maximize(board.copy(), alpha, beta, depth, None)
    board.move(np.asarray(best_move), self.player)
    return best_move

  def maximize(self, board, alpha, beta, depth, move):

    # leaf node
    # finished playthrough
    if board.result != 0:
      result_score = self.end_value(board.result) * self.player
      board.undo_move(move)
      return result_score, None
    # reached determined max depth
    elif depth == 0:
      board_score = self.heuristic(board) * self.player
      board.undo_move(move)
      return board_score, None

    # not leaf node
    a, b = alpha, beta

    best_val = float('-inf')
    best_move = None
    valid_moves = board.availible_moves_numpy()
    for i in range(valid_moves.shape[0]):
      made_move = (valid_moves[i,0], valid_moves[i,1], valid_moves[i,2], valid_moves[i,3])
      board.move(made_move, -self.player)
      move_val, min_move = self.minimize(board, a, b, depth-1, made_move)

      # maximize out of options
      if move_val > best_val:
        best_val = move_val
        best_move = made_move

      # beta pruning
      if best_val >= b:
        board.undo_move(move)
        return best_val, best_move

      a = max(a, move_val)
    
    board.undo_move(move)
    return best_val, best_move
    
  def minimize(self, board, alpha, beta, depth, move):

    # leaf node
    # finished playthrough
    if board.result != 0:
      result_score = self.end_value(board.result) * self.player
      board.undo_move(move)
      return result_score, None
    # reached determined max depth
    elif depth == 0:
      board_score = self.heuristic(board) * self.player
      board.undo_move(move)
      return board_score, None

    # not leaf node
    a, b = alpha, beta

    best_val = float('inf')
    best_move = None
    valid_moves = board.availible_moves_numpy()
    for i in range(valid_moves.shape[0]):
      made_move = (valid_moves[i,0], valid_moves[i,1], valid_moves[i,2], valid_moves[i,3])
      board.move(made_move, self.player)
      move_val, max_move = self.maximize(board, a, b, depth-1, made_move)

      # minimize out of options
      if move_val < best_val:
        best_val = move_val
        best_move = made_move

      # alpha pruning
      if best_val <= a:
        board.undo_move(move)
        return best_val, best_move

      b = min(b, move_val)
    
    board.undo_move(move)
    return best_val, best_move

class TimedMCTSAgent(Agent):
  def __init__(self, player, max_time, c):
    self.player = player
    self.max_time = max_time
    self.c = c
    self.root = None

  def get_player(self):
    return self.player

  def make_move(self, board):
    time_s = time.time()

    if self.root == None:
      self.root = Node(-self.player, board.copy(), None, self.c, None)
    else:
      found = False
      for child in self.root.children:
        if np.all(child.board.get_state() == board.get_state()):
          found = True
          self.root = child
          break
      if not found:
        self.root = Node(-self.player, board.copy(), None, self.c, None)
    while (time.time() - time_s) < self.max_time:
      selected_node = self.root.select_node()
      expanded_node = selected_node.expand_node()
      expanded_node.playout()

    best_uct = -1
    best_child = None
    for child in self.root.children:
      child_uct = child.uct()
      if child_uct > best_uct:
        best_child = child
        best_uct = child_uct

    self.root = best_child

    if best_child == None:
      potential_moves = board.availible_moves_numpy()
      choice = np.random.choice(potential_moves.shape[0], 1)[0]
      move = potential_moves[choice]
    else:
      move = best_child.move
    board.move(move, self.player)
    return move

  def reset(self):
    self.root = None

class Node():
  def __init__(self, player, board, move, c, parent):
    # who made the last move
    self.player = player
    self.board = board
    self.move = move
    self.c = c
    self.parent = parent
    self.wins = 0
    self.losses = 0
    self.ties = 0
    self.visits = 0
    self.is_leaf = True
    self.children = []

  def uct(self):
    if self.visits == 0:
      return float("inf")

    n = self.visits
    w = self.wins
    t = self.ties * .5
    N = self.parent.visits

    return (w+t)/n + self.c * np.sqrt(np.log(N)/n)

  # traverses the tree to find the next node to do a game from
  def select_node(self):
    if self.is_leaf:
      selection = self
    else:
      max_uct = -1
      next_node = None
      for child in self.children:
        child_uct = child.uct()
        if child_uct > max_uct:
          next_node = child
          max_uct = child_uct
      selection = next_node.select_node()

    return selection

  def expand_node(self):
    if self.board.result != 0:
      return self
    elif self.visits == 0:
      return self
    else:
      self.is_leaf = False
      valid_moves = self.board.availible_moves_numpy()
      for i in range(valid_moves.shape[0]):
        child_player = -self.player
        child_board = self.board.copy()
        child_board.move(valid_moves[i,:], child_player)
        child_node = Node(child_player, child_board, valid_moves[i,:], self.c, parent=self)
        self.children.append(child_node)

      return random.choice(self.children)

  def playout(self):
    board = self.board.copy()
    player = -self.player
    while board.result == 0:
      valid_moves = board.availible_moves_numpy()
      player = -player
      choice = np.random.choice(valid_moves.shape[0], 1)[0]
      selected_move = valid_moves[choice]
      board.move(selected_move, player)

    self.backpropogate(board.result)

  def backpropogate(self, winner):
    curr_node = self
    while curr_node is not None:
      curr_node.visits +=1
      if winner == -2:
        curr_node.ties += 1
      elif curr_node.player == winner:
        curr_node.wins += 1
      else:
        curr_node.losses += 1
      curr_node = curr_node.parent