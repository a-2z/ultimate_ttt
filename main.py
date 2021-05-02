
# Basic setup
import numpy as np
import re
import random
from ai import *
import time
from board import UltimateTTT, State


def parse_input(str):
    parsed = re.findall("[0-9]+", str)
    return ((int(parsed[0]), int(parsed[1])), (int(parsed[2]), int(parsed[3])))

def main():
    tester()

def random_v_random():
    avg_time = []
    for _ in range(10000):
        t0 = time.time()
        game = UltimateTTT()
        while game.global_outcome() == State.INCOMPLETE:
            game.move(random.choice(game.available_moves()))
        t1 = time.time()
        avg_time.append(t1 - t0)
    return sum(avg_time) / len((avg_time))

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
            if random_turn == 1:
                game.move(random.choice(game.available_moves()))
                ai_move = ai.pick_move(game)
                game.move(ai_move)
            elif random_turn == -1:
                ai_move = ai.pick_move(game)
                game.move(ai_move)
                game.move(random.choice(game.available_moves()))
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
        availible_moves = game.availible_moves_numpy()
        print(availible_moves)
        choice = np.random.choice(availible_moves.shape[0], 1)[0]
        mov = availible_moves[choice]
        mv = ((mov[0], mov[1]), (mov[2], mov[3]))
        game.move(mv)
        print(game.__str__(pretty_print=True))
    print(game.global_outcome())
    if input("Play again (y/n)? ") == "y":
        tester()

if __name__ == "__main__":
    main()
