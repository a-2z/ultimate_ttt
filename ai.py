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
    def __init__(self, move, parent = None, children = set(), ucb_c = 2):
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
        if not self.parent or self.n = 0:
            return float('inf')
        x_i = self.wins/self.n
        return x_i + c * sqrt(log(self.parent.n)/self.n)

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
    Monte Carlo Tree Search
    """
    #The number of iterations to run the algorithm based on the difficulty
    DIFFICULTY = {level: level * 100000 for level in range(1, 6)}

    def __init__(self, difficulty = 5):
        #hyperparameter for computing upper confidence bounds
        self.c = 2
        self.max_iters = DIFFICULTY[difficulty]
        self.game = None

    def pick_move(self, game):
        """
        Runs MCTS for a number of iterations based on difficulty and selects
        the optimal move to play from the current position.

        Returns the move (global_coord, local_coord) corresponding to the 
        highest UCB estimate.
        """
        self.game = game
        sim_game = copy.deepcopy(self.game)
        root = MoveNode(self.game.moves[-1])
        candidates = self.game.available_moves()
        root.children = root.expand(candidates)
        run_sims(root)

    def run_sims(self, root):
        game_tmp = copy.deepcopy(self.game)
        next_move = max(root.children, lambda c: c.compute_ucb())

        for _ in self.max_iters:
            if next_move.n == 0:
                result = self.play_random(game_tmp)
                next_move.back_propagate(result)
            else:
                game_tmp.move(next_move)
                candidates = game_tmp.available_moves()
                next_move.expand(candidates)
                next_move = max(next_move.children, lambda c: c.compute_ucb())
                game_tmp.move()
                    
    def expand(self, node, candidates):
        node.children = [MoveNode(move=c, parent=next_move) for c in candidates]

    def play_random(self, game):
        """
        Returns the outcome of a game in which only random moves have been 
        played for both players
        """
        while game.result == INCOMPLETE:
            candidates = game.available_moves
            game.move(random.choice(candidates))
        if game.result.value == 1:
            return 1 
        #draw
        elif game.result.value == -2:
            return 0.5
        else:
            return 0




