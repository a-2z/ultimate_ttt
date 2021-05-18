# Basic setup
import numpy as np
import re
import random
from ai import *
import time
from board import UltimateTTT, State


def parse_input(str):
    return np.array([int(i) for i in re.findall("[0-9]+", str)])

def main():
    ai_v_rand(1, 100)

def _agent_move(game, agent):
    """
    Agent picks a move from available moves in unspecified manner and then
    the move is played in the game
    """
    move = agent.pick_move(game)
    game.move(move)

def agent_play(a1, a2):
    """
    Returns the outcome of a game between two agents (AIs, random players, etc)

    0 means agent 1 lost, 1 means agent 1 won, and 2 means there was a draw.
    """
    game = UltimateTTT()
    players = (a1, a2)
    #randomly pick who goes first
    first = random.randint(0, 1)
    to_move = first
    while game.global_outcome() == State.INCOMPLETE:
        _agent_move(game, players[to_move])
        #flips whose turn it is
        to_move = not to_move
    outcome = game.global_outcome()
    if outcome == State.DRAW:
        return 2
    elif outcome == State.X:
        return int(first != 0)
    else:
        return int(first != 1)

################Playing against real opponents##################################
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
    elif game.global_outcome() == State.O:
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


if __name__ == "__main__":
    main()