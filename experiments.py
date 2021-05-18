from ai import MCTS
from main import agent_play
from agents import RandomAgent
import time
import sys
import inspect
import threading
import csv


###Experiment Definitions###

c = [2, 10, 50, 100, 1000]
difficulty = [1, 2, 3, 4, 5]
num_games = 1

class ExperimentFuncs:
    """
    All experiments should be void functions with no arguments. They can
    be called from the command line. 
    
    For example, to run only experiments 1 and 3, you can type:

    python experiments.py 1 3
    """
    #variables of monte carlo tree search
    c_parameters = [1, 2, 3, 50, 200, 1000, 2000]
    difficulties = MCTS.DIFFICULTY.values()
    #a random opponent that can be used in simulations
    rando = RandomAgent()

    def experiment1():
        """
        Test different ucb and difficulty combinations against a random
        opponent; number of rollouts is fixed.
        """
        num_games = 10
        stats = {}
        #wins, losses, draws
        for c in ExperimentFuncs.c_parameters:
            for d in ExperimentFuncs.difficulties:
                mcts = MCTS(variable_diff=False, difficulty=d, ucb_c=c)
                wld = [0, 0, 0]
                total_time = 0
                for g in range(num_games):
                    t0 = time.time()
                    wld[agent_play(mcts, ExperimentFuncs.rando)] += 1
                    t1 = time.time()
                    total_time += t1 - t0
                    #must reset the root between games
                    mcts.reset_root()
                stats[(c, d)] = wld, total_time / num_games
        save_results(stats)

    def experiment2():
        print("run 2")

    def experiment3():
        print("run 3")

def save_results(experiment_num, stats):
    contents = "c_parameter\tDifficulty\tW\tD\tL\tTime\n"
    with open("experiment{}.csv".format(experiment_num), "w+") as csv_file:
        for param, stat in stats.items():
            WDL = stat[0]
            time = stat[1]
            contents += "{}\t{}\t{}\t{}\t{}\t{}\n".format(
                                                            param[0],
                                                            param[1],
                                                            WDL[0],
                                                            WDL[1],
                                                            WDL[2],
                                                            time)
        csv_file.write(contents)

if __name__ == "__main__":
    to_run = []
    for exp_num in sys.argv[1:]:
        to_run.append("experiment" + exp_num)
    experiment_funcs = inspect.getmembers(ExperimentFuncs)
    experiment_threads = [threading.Thread(target = func[1]) for func in experiment_funcs]
    for thread in experiment_threads:
        thread.start()



    # def experiments(c, difficulty, num_games, ai_v_rand=True):
    #     print("here")
    #     game_stats = {}
    #     if ai_v_rand:
    #         for ucb_c in c:
    #             for diff in difficulty:
    #                 sum_list = [0, 0, 0]
    #                 time_avg = 0
    #                 for k in range(num_games):
    #                     result = main.ai_v_rand(diff, ucb_c)
    #                     time_avg += result[1]
    #                     sum_list = [a + b for a, b in zip(sum_list, result[0])]
    #                 average_time = time_avg / num_games
    #                 game_stats[(ucb_c, diff)] = (sum_list, average_time)
    #                 print(sum_list, average_time)
    #     else:
    #         # play ai_v_ai
    #         print("ai_v_ai")
    #     print(game_stats)
    #     return game_stats