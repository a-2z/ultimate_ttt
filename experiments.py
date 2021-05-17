import numpy as np
import main
import csv

c = [2, 10, 50, 100, 1000]
difficulty = [1, 2, 3, 4, 5]
num_games = 100

def experiments(c, difficulty, num_games, ai_v_rand=True):
    print("here")
    game_stats = {}
    if ai_v_rand:
        for ucb_c in c:
            for diff in difficulty:
                sum_list = [0, 0, 0]
                time_avg = 0
                for k in range(num_games):
                    result = main.ai_v_rand(diff, ucb_c)
                    time_avg += result[1]
                    sum_list = [a + b for a, b in zip(sum_list, result[0])]
                average_time = time_avg / num_games
                game_stats[(ucb_c, diff)] = (sum_list, average_time)
                print(sum_list, average_time)
    else:
        # play ai_v_ai
        print("ai_v_ai")
    print(game_stats)
    return game_stats
  
stats = experiments(c, difficulty, num_games)
# file = open('experiments.csv', 'w+', newline ='')
# with file:    
#     write = csv.writer(file)
#     write.writerow(['difficulty:1', 'difficulty:2', 'difficulty:3', 'difficulty:4', 'difficulty:5'])
#     write.writerows(stats)

def wack_csv(stats):
    contents = "c_parameter\tDifficulty\tW\tD\tL\tTime\n"
    with open("stats_sheet.csv", "w+") as csv_file:
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

wack_csv(stats)
