from ai import MCTS
from main import agent_play
from agents import RandomAgent
import time
import sys
import inspect
import threading
from multiprocessing import Process, RawValue, Array, Lock
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

    Experiments run in parallel
    """
    #variables of monte carlo tree search
    c_parameters = [1, 2, 3, 50, 200, 1000, 2000]
    difficulties = MCTS.DIFFICULTY
    #a random opponent that can be used in simulations
    rando = RandomAgent()

    class Stats:
        def __init__(self):
            self.scoreboard = [0, 0, 0]
            self.time = 0
            self.lock = Lock()

        def set_stats(self, score, time):
            with self.lock:
                print(score, "dong")
                self.scoreboard[score] += 1
                self.time += time

    def _time_game(scoreboard, tot_time, d, c):
        mcts = MCTS(variable_diff=True, difficulty=d, ucb_c=c)
        total_time = 0
        t0 = time.time()
        outcome = agent_play(mcts, ExperimentFuncs.rando)
        t1 = time.time()
        total_time += t1 - t0
        scoreboard[outcome] += 1
        tot_time.value = total_time

    def experiment1():
        """
        Test different ucb and difficulty combinations against a random
        opponent; number of rollouts is fixed.
        """
        num_games = 10
        exp_stats = {}
        #wins, losses, draws
        for c in ExperimentFuncs.c_parameters:
            for d in ExperimentFuncs.difficulties:
                total_time = RawValue('f', 0.0)
                wld = Array('d', [0, 0, 0])
                #run games concurrently
                procs = [Process(target=ExperimentFuncs._time_game, 
                                 args=(wld, total_time, d, c)) 
                                 for i in range(num_games)]
                for p in procs: p.start()
                for p in procs: p.join()
                exp_stats[(c, d)] = wld[:], total_time.value / num_games
                print(exp_stats[(c, d)])
        save_results(1, exp_stats)

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
    exp_threads = []
    for func in experiment_funcs:
        if func[0] in to_run:
            exp_threads.append(threading.Thread(target = func[1]))
    for thread in exp_threads:
        thread.start()
