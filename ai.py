from board import UltimateTTT, State
from math import log, sqrt
import random
import copy

class MoveNode:
    """
    Represents a move in an ultimate Tic-Tac-Toe game.
    When ancestors are taken into account, the node
    represents the history/state of a Tic-Tac-Toe game thus far.
    """
    def __init__(self, move, parent = None, children = [], ucb_c = 2):
        """
        Initializes a move node in a decision tree.

        By default, the node is a root.
        """
        self.parent = parent
        self.children = children
        self.move = move
        self.n = 0
        self.wins = 0
        #a hyperparameter used for computing the UCB
        self.c = ucb_c

    def compute_ucb(self):
        """
        Returns the upper confidence bound
        of a MoveNode. 

        Precondition: The node is not the root node.
        """
        #root and unsimulated moves have infinite UCB
        if not self.parent or self.n == 0:
            return float('inf')
        x_i = self.wins/self.n
        return x_i + self.c * sqrt(log(self.parent.n)/self.n)

    def expand(self, candidates):
        self.children = [MoveNode(move=c, parent=self) for c in candidates]

    def back_propagate(self, result):
        curr = self 
        while curr:
            curr.n += 1
            curr.wins += result 
            curr = curr.parent

class MCTS:
    """
    Implements playing of Ultimate Tic-Tac-Toe using 
    Monte Carlo Tree Search.
    """
    #The number of iterations to run the algorithm based on the difficulty
    DIFFICULTY = {level: level * 1000 for level in range(1, 6)}

    def __init__(self, turn=1, difficulty = 5):
        """
        Parameter turn: the token 1 or -1 to which the AI corresponds

        Parameter difficulty: int in [1, 5] that corresponds to the number
        of iterations of the algorithm to run on each move.
        """
        #hyperparameter for computing upper confidence bounds
        self.c = 2
        self.max_iters = MCTS.DIFFICULTY[difficulty]
        self.root_state = None
        #SHOULD NOT BE MODIFIED IN SIMULATIONS
        self.sim_game = None
        self.is_x = turn == 1
        self.root = None

    def pick_move(self, game):
        """
        Runs MCTS for a number of iterations based on difficulty and selects
        the optimal move to play from the current position.

        Returns the move (global_coord, local_coord) corresponding to the 
        highest UCB estimate.
        """
        #save the current game, which should never be modified during simulation
        self.root_state = game
        self.sim_game = copy.deepcopy(game)
        history = self.sim_game.moves
        opp_move = None
        #get the last move played if there is a history
        if history: 
            opp_move = self.sim_game.moves[-1]
        #set root if none exists
        if self.root == None:
            if history:
                self.root = MoveNode(opp_move) 
            else:
                self.root = MoveNode(None)
        else:
            self.set_root(opp_move)
        #on subsequent simulations, root will be calculated
        candidates = self.sim_game.available_moves()
        if candidates == []:
            print("dafuq")
        self.root.expand(candidates)
        return self.run_sims(self.root)

    def best_child(self, move):
        """
        Return the child of an expanded MoveNode with the highest 
        Upper Confidence Bound.
        """
        #find the highest UCB among children
        max_ucb = max([child.compute_ucb() for child in move.children])
        #since there are possible multiple maxima, get all and pick randomly.
        best = [c for c in move.children if c.compute_ucb() == max_ucb]
        return random.choice(best)

    def run_sims(self, root):
        game_tmp = self.sim_game
        #create nodes for the candidate moves in the current position
        next_move = self.best_child(root)

        #run a simulation of a game max_iters times
        for _ in range(self.max_iters):
            if next_move.n == 0:
                game_tmp.move(next_move.move)
                game_over = game_tmp.global_outcome() != State.INCOMPLETE
                result = None
                if not game_over:
                    result = self.play_random(game_tmp)
                #terminal node
                else: 
                    result = game_tmp.global_outcome().value
                next_move.back_propagate(result)
                #after running one simulation, reset the game to the root 
                next_move = self.best_child(root)
                game_tmp.set_state(self.root_state)
            else:
                game_tmp.move(next_move.move)
                #check if in terminal
                outcome = game_tmp.global_outcome()
                if outcome != State.INCOMPLETE:
                    next_move.back_propagate(game_tmp.global_outcome().value)
                    game_tmp.set_state(self.root_state)
                    continue
                candidates = game_tmp.available_moves()
                #expand a node that has been simulated once
                if next_move.n == 1:
                    next_move.expand(candidates)
                try:
                    next_move = self.best_child(next_move)
                except:
                    pass
        to_play = self.best_child(root).move
        self.set_root(to_play)
        return to_play

    def set_root(self, move):
        """
        Searches for a child of root corresponding to move and sets it as 
        the root if it matches.
        """
        for c in self.root.children:
            if c.move == move:
                self.root = c
                    
    def expand(self, node, candidates):
        node.children = [MoveNode(move=c, parent=next_move) for c in candidates]

    def play_random(self, game):
        """
        Returns the outcome of a game in which only random moves have been 
        played for both players
        """
        while game.global_outcome() == State.INCOMPLETE:
            candidates = game.available_moves()
            game.move(random.choice(candidates))
        if game.global_outcome().value == 1:
            return 1 if self.is_x else 0
        #draw
        elif game.global_outcome().value == -2:
            return 0.5
        else:
            return 0 if self.is_x else 1




