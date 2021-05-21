from board import *
from agents import *
from heuristics import *
import time

def play_game(player1, player2, board):
    """
    Plays a game of Ultimate Tic-Tac-Toe until completion
    """
    players = [player1, player2]
    to_play = 0
    while board.get_outcome() == 0:
        move = players[to_play].make_move(board)
        to_play = not to_play
    return board.get_outcome()

def test_visual():
    p1 = RandomAgent(1)
    p2 = RandomAgent(-1)
    b = Board(3)
    play_game_visual(p1, p2, b)

def score_AIs(num_games, player_algo, opponent_algo):
    # 0 -> win
    # 1 -> loss
    # 2 -> tie
    score = np.zeros(3)
    player_token = player_algo.get_player()

    p1, p2 = player_algo, opponent_algo
    #switch players if player is O
    if player_token == -1:
        p1, p2 = opponent_algo, player_algo

    for _ in range(num_games):
        board = Board(3)
        play_game(p1, p2, board)
        if board.get_outcome() == -2:
            score[2] += 1
        elif board.get_outcome() == player_token:
            score[0] += 1
        else:
            score[1] += 1

        player_algo.reset()
        opponent_algo.reset()

    return score


def print_out_result(player_agent, opponent_agent, num_games, label):
    time_s = time.time()
    game = score_AIs(num_games, player_agent, opponent_agent)
    time_e = time.time()
    print(label)
    print(game)
    print(time_e - time_s)


if __name__ == "__main__":
    num_games = 500

    max_time_mcts = .2
    max_time_minmax = .1

    randX = RandomAgent(1)
    randO = RandomAgent(-1)

    mcts1X = TimedMCTSAgent(1, max_time_mcts, 1)
    mcts1O = TimedMCTSAgent(-1, max_time_mcts, 1)
    mcts10X = TimedMCTSAgent(1, max_time_mcts, 10)
    mcts10O = TimedMCTSAgent(-1, max_time_mcts, 10)
    mcts100X = TimedMCTSAgent(1, max_time_mcts, 100)
    mcts100O = TimedMCTSAgent(-1, max_time_mcts, 100)

    minmax1X = TimedMinmaxAgent(
        1,
        max_time_minmax,
        end_value,
        plus_heuristic_fun(
            local_h,
            global_h,
            1))
    minmax1O = TimedMinmaxAgent(-1, max_time_minmax,
                                end_value, plus_heuristic_fun(local_h, global_h, -1))
    minmax2X = TimedMinmaxAgent(
        1,
        max_time_minmax,
        end_value,
        plus_neg_heuristic_fun(
            local_h,
            global_h,
            1))
    minmax2O = TimedMinmaxAgent(-1, max_time_minmax, end_value,
                                plus_neg_heuristic_fun(local_h, global_h, -1))
    minmax3X = TimedMinmaxAgent(
        1,
        max_time_minmax,
        end_value,
        attack_heuristic_fun(
            local_h,
            attack_h,
            1))
    minmax3O = TimedMinmaxAgent(-1, max_time_minmax, end_value,
                                attack_heuristic_fun(local_h, attack_h, -1))

    AIsX = [mcts1X, mcts10X, mcts100X, minmax1X, minmax2X, minmax3X]
    AIsX_labels = [
        "mcts1X",
        "mcts10X",
        "mcts100X",
        "minmax1X",
        "minmax2X",
        "minmax3X"]

    AIsO = [mcts1O, mcts10O, mcts100O, minmax1O, minmax2O, minmax3O]
    AIsO_labels = [
        "mcts1O",
        "mcts10O",
        "mcts100O",
        "minmax1O",
        "minmax2O",
        "minmax3O"]

    print_out_result(randX, randO, num_games, "random X vs random O")

    # O random
    for i in range(len(AIsX)-3):
        print_out_result(
            AIsX[i],
            randO,
            num_games,
            AIsX_labels[i] +
            " vs random O")

    # X random
    for i in range(len(AIsO)):
        print_out_result(
            AIsO[i],
            randX,
            num_games,
            AIsO_labels[i] +
            " vs random X")

    # combos
    for i in range(len(AIsX)):
        for j in range(len(AIsO)):
            print_out_result(
                AIsX[i],
                AIsO[j],
                num_games,
                AIsX_labels[i] +
                " vs " +
                AIsO_labels[j])
