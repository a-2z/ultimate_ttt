#tree class for state
import numpy as np
import board

orientations = {
    (0, 0): np.radians(-90),
    (0, 1): None
    (0, 2): None
    (1, 0): np.radians(-90)
    (1, 2): np.radians(90)
    (2, 0): np.radians(180)
    (2, 1): np.radians(180)
    (2, 2): np.radians(90)
}

class MoveNode:
    def __init__(self, parent):
        self.children = set()
        self.parent = parent
        self.moves = []
        self.ucb = 0
        self.n_i = 0

    def insert(self):
        pass 

    def lookup(self, history):
        pass

class Player:

    def rotate(self, move):
        """
        rotates a move given in (global_coords, local_coords)
        to some canonical direction given by the first
        non-central move
        """
        if not self.rotate:
            return move
        glob_x, loc_x = move[0][0] - 1, move[1][0] - 1
        glob_y, loc_y = move[0][1] - 1, move[1][1] - 1

        #rotate the indices in the x
        glob_x_prime = -glob_y * self.rot_sin + glob_x * self.rot_cos
        loc_x_prime = -loc_y * self.rot_sin + loc_x * self.rot_cos
        #rotate the indices in the y
        glob_y_prime = glob_y * self.rot_cos + glob_x * self.rot_sin
        loc_y_prime =  loc_y * self.rot_cos + loc_x * self.rot_sin

        #reconstruct the move
        new_glob = (round(glob_x_prime + 1), round(glob_y_prime + 1))
        new_loc = (round(loc_x_prime + 1), round(loc_y_prime + 1))
        return ((new_glob, new_loc))


    def __init__(self, turn):
        self.orientation_set = False
        self.rotate = True
        #create an instance of the game
        self.game = UltimateTTT()
        self.decision_tree = MoveNode()
        self.rot_sin, self.rot_cos = 0, 0
        
    def set_orientations(self, move):
        if move[0] == (1, 1):
            if move[1] == (1, 1): 
                return
            else:
                angle = orientations[move[1]]
                if angle is None:
                    self.no_rotate = True
                    return
                self.rot_sin = np.sin(angle)
                self.rot_cos = np.cos(angle)
                self.orientation_set = True
        else:
            angle = orientations[move[0]]
            if angle is None:
                    self.no_rotate = True
                    return
            self.rot_sin = np.sin(angle)
            self.rot_cos = np.cos(angle)
            self.orientation_set = True

    def play(self):
        while game.result == State.INCOMPLETE:
            next_move = self.simulate(game.moves)
            if rotate and not self.orientation_set:
                self.set_orientations(next_move)
            next_move = self.rotate(next_move)



"""
x |  |             
==========
  |   |      ===>   
============
  |   |
"""

#each node is just one move
#also store all available moves 
#


