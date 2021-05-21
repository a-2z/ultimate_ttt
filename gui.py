from tkinter import *
from board import *
from functools import *
import itertools
from PIL import ImageTk
from experiments import *
import time
import threading
from agents import *
from heuristics import *

def main():
    gui = Gui()
    gui.launch()

class Gui:
    def __init__(self, board=Board(3)):
        self.master = Tk()
        self.master.geometry("800x600")
        self.large_canvas = Canvas(width=800, height=600)
        self.master.title("AI Ultimate Tic-tac-toe")
        self.px = Label(self.master, text="Player X", bg="#FF0000")
        self.po = Label(self.master, text="Player O", bg="#0000FF")
        self.board = board
        self.var1 = StringVar(self.master)
        self.var1.set("Player 1")
        self.var2 = StringVar(self.master)
        self.p1_select = OptionMenu(self.master, self.var1, "Minimax 1", "Minimax 2", "Minimax 3", "MCTS", "Random", "Human")
        self.p2_select = OptionMenu(self.master, self.var2, "Minimax 1", "Minimax 2", "Minimax 3", "MCTS", "Random", "Human")
        self.var2.set("Player 2")
        self.start_game = Button(self.master, text="Start", 
                            command=partial(self.set_opps, self.var1, self.var2))
        self.reset = Button(self.master, text="Reset", state=DISABLED, command=self.reset)
        self.winner = Label(self.master, text="")
        self.p1 = self.p2 = None
        self.in_progress = False
        self.local_boards = {}
        self.make_gui()

    def reset(self):
        self.master.destroy()
        self.__init__()

    def update_board(self):
        if self.board.get_outcome == 1:
            self.winner.configure(text="X wins!", bg="#FF0000")
        elif self.board.get_outcome == -1:
            self.winner.configure(text="O wins!", bg="#0000FF")
        elif self.board.get_outcome == -2:
            self.winner.configure(text="Draw", bg="#0000FF")
        else:
            self.winner.configure(text="", bg="#000000")
        self.winner.place(x=550, y=350)


    def play_game_visual(self):
        """
        Plays a game of Ultimate Tic-Tac-Toe until completion
        """
        players = [self.p1, self.p2]
        to_play = 0
        while self.board.get_outcome() == 0:
            player = players[to_play]
            move = player.pick_move(self.board)
            self.make_move(move, player.get_player())
            player.make_move(self.board)
            to_play = not to_play
        self.update_board()
        self.reset.configure(state=NORMAL)
        self.check_won_boards()
        return self.board.get_outcome()

    def set_player_token(self, agent, token):
        #heuristic vars
        local_h = np.array([[2,1,2],[1,3,1],[2,1,2]])
        global_h = np.array([[8,6,8],[6,10,6],[8,6,8]])
        attack_h = np.array([4,5])
        max_time_mcts = .2
        max_time_minmax = .1

        agents = {"Minimax 3": TimedMinmaxAgent(token, max_time_minmax,
        end_value, attack_heuristic_fun(local_h, attack_h, 1)), 
        "Minimax 2": TimedMinmaxAgent(
        token,
        max_time_minmax,
        end_value,
        plus_neg_heuristic_fun(
            local_h,
            global_h,
            1)),
            "Minimax 1":TimedMinmaxAgent(token, max_time_minmax,
                                end_value, plus_heuristic_fun(local_h, global_h, -1)),
            "MCTS": TimedMCTSAgent(token, max_time_mcts, 10), 
            "Random": RandomAgent(token), 
            "Human": Human_Gui(token)}
        return agents[agent]


    def set_opps(self, p1, p2):
        p1, p2 = p1.get(), p2.get()
        if p1 != "Player 1" and p2 != "Player 2" and not self.in_progress:
            self.p1 = self.set_player_token(p1, 1)
            self.p2 = self.set_player_token(p2, -1)
            self.in_progress = True 
            self.play_game_visual()
            self.in_progress = False

    def launch(self):
        self.master.mainloop()

    def make_gui(self):
        self.px.place(x=500, y=100); self.po.place(x=500, y=400)
        self.p1_select.place(x=550, y=250)
        self.p2_select.place(x=625, y=250)
        self.start_game.place(x=550, y=300)
        self.winner.place(x=550, y=350)
        self.reset.place(x=600, y=300)
        grid = []
        for i in range(3):
            for j in range(3):
                board = LocalBoard(self.master, i, j, self)
                self.local_boards[(i, j)] = board 
                b_canvas = board.local_board().grid(row=i, column=j, padx=3, pady=3)

    def make_move(self, move, player):
        token = "X" if player == 1 else "O"
        glob = (move[0], move[1])
        loc = (move[2], move[3])
        board = self.local_boards[glob]
        cell = board.get_cells()[loc]
        cell["text"] = token
        self.check_won_boards()
    
    def check_won_boards(self):
        wins = self.board.get_win_board()
        for i in range(wins.shape[0]):
            for j in range(wins.shape[1]):
                outcome = wins[i, j]
                board = self.local_boards[(i, j)]
                if outcome == 1 or outcome == -1:
                    color = "#FF0000" if outcome > 0 else "#0000FF"
                    board.set_colors(color)



class LocalBoard(Frame):
    def __init__(self, root, i, j, parent):
        self.x = ImageTk.PhotoImage(file="./x.png")
        self.o = ImageTk.PhotoImage(file="./o.png")
        self.root = root
        self.parent = parent
        self.canvas = Canvas(self.root, 
                            width=int(root.cget("width")) // 3, 
                            height=int(root.cget("width")) // 3,
                            bg="#966F33")
        self.i =i
        self.j = j
        self.cells = {}
        self.create_board()

    def set_colors(self, color: str):
        for cell in self.cells.values():
            cell.configure(bg=color)

    def get_cells(self):
        return self.cells

    def local_board(self):
        return self.canvas

    def create_board(self):
        for i in range(3):
            for j in range(3):
                cell_ij = Button(self.canvas, 
                          text=" ",
                          bg="#e64a19",
                          width=3,
                          height=3,
                          command=partial(self.change_token, (i, j)))
                self.cells[(i, j)] = cell_ij
                cell_ij.grid(row=i, column=j)

    def change_token(self, coords):
        root = self.parent
        token = "X"
        if not root.var1.get() == "Human" or root.var2.get() == "Human":
            return
        if root.var1.get() == "Human":
            root.make_move((self.i, self.j, coords[0], coords[1]), 1)
            opp = root.set_player_token(root.var2.get(), -1)
            opp_move = opp.pick_move(root.board)
            root.make_move(opp_move, -1)
        else:
            opp = root.set_player_token(root.var1.get(), 1)
            opp_move = opp.pick_move(root.board)
            root.make_move(opp_move, 1)
            root.make_move((self.i, self.j, coords[0], coords[1]), -1)
        root.check_won_boards()


if __name__ == "__main__":
    main()