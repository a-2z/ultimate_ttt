from board import *
from agents import *
from heuristics import *
import re

def main():
    print("Press 1 to watch playthrough, press 2 to play AI")
    p_input = input()
    if p_input == "1":
      select_AI_X()
    elif p_input == "2":
      select_AI()
    else:
      print("invalid input")
      main()

def select_AI():
  print("Select piece to play (X or O)")
  player_input = input()
  if player_input == "X":
    player = 1
  elif player_input == "O":
    player = -1
  else:
    print("invalid input")
    select_AI()
  print("Select the AI to play against:")
  print("Press 1 for random, press 2 for MCTS with c = 1, press 3 for MCTS with c = 10, press 4 for MCTS with c 100,")
  print("press 5 for Minmax H1, press 6 for Minmax H2, press 7 for Minmax H3")

  p_input = input()

  if p_input == "1":
    AI_vs_player(RandomAgent(1))
  elif p_input == "2":
    AI_vs_player(TimedMCTSAgent(1, .2, 1))
  elif p_input == "3":
    AI_vs_player(TimedMCTSAgent(1, .2, 10))
  elif p_input == "4":
    AI_vs_player(TimedMCTSAgent(1, .2, 100))
  elif p_input == "5":
    AI_vs_player(TimedMinmaxAgent(1, .1, end_value, plus_heuristic_fun(local_h, global_h, 1)))
  elif p_input == "6":
    AI_vs_player(TimedMinmaxAgent(1, .1, end_value, plus_neg_heuristic_fun(local_h, global_h, 1)))
  elif p_input == "7":
    AI_vs_player(TimedMinmaxAgent(1, .1, end_value, attack_heuristic_fun(local_h, attack_h, 1)))
  else:
    print("wrong input")
    select_AI_X()

def select_AI_X():
  print("Select the AI to play X:")
  print("Press 1 for random, press 2 for MCTS with c = 1, press 3 for MCTS with c = 10, press 4 for MCTS with c 100,")
  print("press 5 for Minmax H1, press 6 for Minmax H2, press 7 for Minmax H3")
  p_input = input()

  if p_input == "1":
    select_AI_O(RandomAgent(1))
  elif p_input == "2":
    select_AI_O(TimedMCTSAgent(1, .2, 1))
  elif p_input == "3":
    select_AI_O(TimedMCTSAgent(1, .2, 10))
  elif p_input == "4":
    select_AI_O(TimedMCTSAgent(1, .2, 100))
  elif p_input == "5":
    select_AI_O(TimedMinmaxAgent(1, .1, end_value, plus_heuristic_fun(local_h, global_h, 1)))
  elif p_input == "6":
    select_AI_O(TimedMinmaxAgent(1, .1, end_value, plus_neg_heuristic_fun(local_h, global_h, 1)))
  elif p_input == "7":
    select_AI_O(TimedMinmaxAgent(1, .1, end_value, attack_heuristic_fun(local_h, attack_h, 1)))
  else:
    print("wrong input")
    select_AI_X()


def select_AI_O(ai_p):
  print("Select the AI to play O:")
  print("Press 1 for random, press 2 for MCTS with c = 1, press 3 for MCTS with c = 10, press 4 for MCTS with c 100,")
  print("press 5 for Minmax H1, press 6 for Minmax H2, press 7 for Minmax H3")
  p_input = input()

  if p_input == "1":
    AI_vs_AI(ai_p, RandomAgent(-1))
  elif p_input == "2":
    AI_vs_AI(ai_p, TimedMCTSAgent(-1, .2, 1))
  elif p_input == "3":
    AI_vs_AI(ai_p, TimedMCTSAgent(-1, .2, 10))
  elif p_input == "4":
    AI_vs_AI(ai_p, TimedMCTSAgent(-1, .2, 100))
  elif p_input == "5":
    AI_vs_AI(ai_p, TimedMinmaxAgent(-1, .1, end_value, plus_heuristic_fun(local_h, global_h, -1)))
  elif p_input == "6":
    AI_vs_AI(ai_p, TimedMinmaxAgent(-1, .1, end_value, plus_neg_heuristic_fun(local_h, global_h, -1)))
  elif p_input == "7":
    AI_vs_AI(ai_p, TimedMinmaxAgent(-1, .1, end_value, attack_heuristic_fun(local_h, attack_h, -1)))
  else:
    print("wrong input")
    select_AI_O(ai_p)


def AI_vs_AI(ai_p, ai_o):
  p_player = ai_p.get_player()

  ais = {p_player:ai_p, ai_o.get_player():ai_o}

  board = Board(3)
  player = 1
  while board.get_outcome() == 0:
    move = ais[player].make_move(board)
    player = -player
    print(move)
    print(board)
    time.sleep(1)

  if board.get_outcome == 1:
    print("X won")
  elif board.get_outcome == -1:
    print("O won")
  else:
    print("tie")

  main()

def parse_input(str):
    parsed = re.findall("[0-9]+", str)
    return np.array([int(parsed[0]), int(parsed[1]), int(parsed[2]), int(parsed[3])])

def get_player_move(board):
  move_input = input()
  move = parse_input(move_input)
  availible_moves = board.availible_moves_numpy()
  found = False
  for i in range(availible_moves.shape[0]):
    if np.all(move == availible_moves[i,:]):
      found = True
      break
  if found:
    return move
  else:
    print("illegal move")
    get_player_move()

def AI_vs_player(ai_o):
  o_player = ai_o.get_player()
  p_player = -o_player

  board = Board(3)
  player = 1
  while board.get_outcome() == 0:
    if player == p_player:
      move = get_player_move(board)
      board.move(move, p_player)
      print(board)
      player = -player
    else:
      move = ai_o.make_move(board)
      print(move)
      print(board)
      player = -player

  if board.get_outcome == p_player:
    print("you won")
  elif board.get_outcome == o_player:
    print("algo won")
  else:
    print("tie")

  main()

if __name__ == "__main__":
    main()