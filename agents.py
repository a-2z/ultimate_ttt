from board import *
import numpy as np
from random import choice

class Agent:
    def __init__(self):
        pass 

    def pick_move(self, game):
        pass

class RandomAgent(Agent):
    def __init__(self):
        pass 

    def pick_move(self, game):
        available_moves = game.available_moves()
        idx = np.random.choice(available_moves.shape[0], 1)[0]
        return available_moves[idx]

        