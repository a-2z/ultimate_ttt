
# Basic setup
import numpy as np
import re
import random
from ai import *
import time
from board import UltimateTTT, State


def parse_input(str):
    parsed = re.findall("[0-9]+", str)
    return np.array([int(parsed[0]), int(parsed[1]), int(parsed[2]), int(parsed[3])])

def make_random_move(game):
    availible_moves = game.availible_moves_numpy()
    choice = np.random.choice(availible_moves.shape[0], 1)[0]
    mov = availible_moves[choice]
    game.move(mov)
    return mov

def main():
    ai_v_rand(1, 100)

def ai_v_rand(difficulty, c):
    WDL = [0, 0, 0]
    game_time = 0
    t0 = time.time()
    game = UltimateTTT()
    # random is O, ai is X
    random_turn = -1
    ai = MCTS(turn=-random_turn, difficulty=difficulty, ucb_c=c)
    while game.global_outcome() == State.INCOMPLETE:
        make_random_move(game)
        ai_move = ai.pick_move(game)
        game.move(ai_move)
    if game.global_outcome() == State.DRAW:
        WDL[1] += 1
    elif game.global_outcome().value == random_turn:
        WDL[2] += 1
    else:
        WDL[0] += 1
    t1 = time.time()
    game_time = t1 - t0
    print(WDL, game_time)
    return WDL, game_time

def random_v_random():
    avg_time = []
    for _ in range(10000):
        t0 = time.time()
        game = UltimateTTT()
        while game.global_outcome() == State.INCOMPLETE:
            make_random_move(game)
        t1 = time.time()
        avg_time.append(t1 - t0)
    average = sum(avg_time) / len((avg_time))
    print(average)
    return average

def get_turn():
    """
    Return the turn of a player based on an input
    """
    player_turn = 0
    while player_turn == 0:
        player_choice = input("X or O (enter x or o): ").lower()
        if player_choice == 'x':
            player_turn = 1 
        elif player_choice == 'o':
            player_turn = -1
    return player_turn

def play_ai():
    #create an AI and print the original board
    game = UltimateTTT()
    print(game.win_board)
    player_turn = get_turn()
    ai = MCTS(turn=-player_turn)
    
    while game.global_outcome() == State.INCOMPLETE:
        #get input from both the user and the AI
        make_moves(game, ai, player_turn)
    print(game.global_outcome())
    if input("Play again (y/n)? ") == "y":
        play_ai()


def play_random():
    WDL = [0, 0, 0]
    game = UltimateTTT()
    random_turn = get_turn()
    ai = MCTS(turn=-random_turn)
    for _ in range(1):
        while game.global_outcome() == State.INCOMPLETE:
            print("made move")
            if random_turn == 1:
                make_random_move(game)
                ai_move = ai.pick_move(game)
                game.move(ai_move)
            elif random_turn == -1:
                ai_move = ai.pick_move(game)
                game.move(ai_move)
                make_random_move(game)
        if game.global_outcome() == State.DRAW:
            WDL[1] += 1
        elif game.global_outcome().value == random_turn:
            WDL[2] += 1
        else:
            WDL[0] += 1
        game = UltimateTTT()
    print ("AI Wins: {0}, Draws: {1}, Losses: {2}".format(*WDL))

def make_moves(game, ai, player_turn):
    if player_turn == 1:
        print(str(game))
        legal = False
        while not legal:
            p_move = parse_input(input("Move: "))
            legal = game.move(p_move)
        print(str(game))
        ai_move = ai.pick_move(game)
        game.move(ai_move)
    elif player_turn == -1:
        print(str(game) + '\n')
        ai_move = ai.pick_move(game)
        game.move(ai_move)
        print(str(game))
        legal = False
        while not legal:
            p_move = parse_input(input("Move: "))
            legal = game.move(p_move)

def tester():
    game = UltimateTTT()
    mov = None
    print(game.__str__(pretty_print=True))
    while game.global_outcome() == State.INCOMPLETE:
        mov = make_random_move(game)
        print(mov)
        print(game.__str__(pretty_print=True))
    print(game.global_outcome())
    if input("Play again (y/n)? ") == "y":
        tester()

if __name__ == "__main__":
    main()