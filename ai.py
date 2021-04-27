#tree class for state
import numpy as np
import re
from board import UltimateTTT, State

#rotation angles based on the first non-central moves
orientations = {
    (0, 0): np.radians(-90),
    (0, 1): None,
    (0, 2): None,
    (1, 0): np.radians(-90),
    (1, 2): np.radians(90),
    (2, 0): np.radians(180),
    (2, 1): np.radians(180),
    (2, 2): np.radians(90)
}

class MoveNode:
    def __init__(self, parent):
        self.children = set()
        self.parent = parent
        self.moves = []
        self.ucb = 0
        self.n_i = 0
        self.wins = 0
        self.value = None

    def insert(self):
        pass 

    def lookup(self, history):
        pass

class Player:
    def __init__(self, turn, num_iters):
        self.game = UltimateTTT()
        #canonical orientations
        self.orientation_set = False
        self.rotate = True
        self.rot_sin, self.rot_cos = 0, 0
        #decision tree for AI
        self.decision_tree = MoveNode()

####################Rotation########################### 
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
        
    def set_orientations(self, move):
        """
        Sets the canonical orientation of the board
        based on the first non-center move on the board.

        This way, variations (rotations) of the same state
        will be combined.
        """
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

####################Play a game###########################
    def play(self, to_play = 1):
        root = MoveNode(None)
        while self.game.result == State.INCOMPLETE:
            if to_play == 1:
                print(str(self.game))
                p_move = parse_input(input("Move: "))
                self.game.move(p_move)
                

            next_move = self.simulate(self.game.moves)
            if self.rotate and not self.orientation_set:
                self.set_orientations(next_move)
            rot_move = self.rotate(next_move)
            self.game.move(next_move)
    
    def get_p_move(self):

    def parse_input(str):
        parsed = re.findall("[0-9]+", str)
        return ((int(parsed[0]), int(parsed[1])), (int(parsed[2]), int(parsed[3])))

    def simulate(self, history):
        """
        Runs simulations of an ultimate Tic-Tac-Toe game for
        num_iters and returns the move with the highest 
        upper confidence bound.
        """
        root = MoveNode(history[0])

# get available moves - make tree from that
# pick random move initially - ucb all set to 0
# keep picking random moves and expanding child nodes
# 
#play all moves in sequence until arrive at root
#orientation: -90
#0, 0, 1, 1
#root = MoveNode(None, history[0])
# increment n_i for root
#self.unexplored = self.game.available_moves()
#for i in unexplored:
#   self.children.add(MoveNode(self, move)   

#
#
#
            
    

