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
        return np.random.choice(available_moves)

        