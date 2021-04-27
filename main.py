
# Basic setup
import numpy as np
import re
import random
from board import UltimateTTT, State


def parse_input(str):
    parsed = re.findall("[0-9]+", str)
    return ((int(parsed[0]), int(parsed[1])), (int(parsed[2]), int(parsed[3])))

def main():
    play_random()
    # game = UltimateTTT()
    # while game.global_outcome() == State.INCOMPLETE:
    #     print(game.__str__(pretty_print=False))
    #     move = parse_input(input("Move: "))
    #     game.move(move)
    # print(game.global_outcome())
    # if input("Play again (y/n)? ") == "y":
    #     main()

def play_random():
    game = UltimateTTT()
    mov = None
    print(game.__str__(pretty_print=True))
    print(game.win_board)
    while game.global_outcome() == State.INCOMPLETE:
        mv = random.choice(game.available_moves())
        mov = mv
        print(mv)
        game.move(mv)
        print(game.__str__(pretty_print=True))
    print(game.global_outcome())
    if input("Play again (y/n)? ") == "y":
        main()

    # class TicTacToe:
    #     def __init__(self):
    #         """
    #         Class constructor for a game of Ultimate Tic-Tac-Toe
    #         """
    #         self.empty = np.zeros((3, 3))
    #         self.turn = True

    #     def display_board(self):
    #         """
    #         Prints the main tic-tac-toe-board given the current game state
    #         """
    #         pass

    #     def _move(self, cell: int) -> bool:
    #         """

    #         """
    #         pass

    #     def check_win():
    #         """
    #         Checks to see if a cell (one of the 3x3 boards) has been won.

    #         Returns True if a cell has been one; otherwise
    #         """
if __name__ == "__main__":
    main()
