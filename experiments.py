import numpy as np
import main

c = [2, 10, 50, 100, 1000]
difficulty = [1, 2, 3, 4, 5, 6]
num_games = 1

# records = np.zeros((len(c)*len(difficulty), 4))
# at i,j there will be an list of wins, losses, draws, and average single game time
records = np.zeros((len(c),len(difficulty)))

def experiments(c, difficulty, num_games, ai_v_rand=True):
    print("here")
    if ai_v_rand:
        for index_c, ucb_c in enumerate(c):
            for index_difficulty, diff in enumerate(difficulty):
                WDL_acc = [0, 0, 0]
                time_avg = 0
                for k in range(num_games):
                    result = main.ai_v_rand(diff, ucb_c)
                    time_avg += result[1]
                    sum_list = [a + b for a, b in zip(WDL_acc, result[0])]
                records[index_c, index_difficulty] = sum_list + time_avg/num_games
    else:
        # play ai_v_ai
        print("a0_v_ai")
    return records


experiments(c, difficulty, num_games)