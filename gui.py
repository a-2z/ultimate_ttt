from tkinter import *
from board import *
from functools import *
import itertools
from PIL import ImageTk
from experiments import *
import time
from agents import *
from heuristics import *

def main():
    gui = Gui()
    gui.launch()

class Gui:
    def __init__(self, board=Board(3)):
        self.master = Tk()
        self.master.geometry("800x600")
        self.master.title("AI Ultimate Tic-tac-toe")
        self.px = Label(self.master, text="Player X")
        self.po = Label(self.master, text="Player O")
        self.board = board
        self.p1 = self.p2 = None
        self.in_progress = False
        self.local_boards = {}
        self.make_gui()

    def play_game_visual(self):
        """
        Plays a game of Ultimate Tic-Tac-Toe until completion
        """
        players = [self.p1, self.p2]
        to_play = 0
        while self.board.get_outcome() == 0:
            player = players[to_play]
            move = player.pick_move(self.board)
            self.make_move(move, player)
            player.make_move(self.board)
            update()
            to_play = not to_play
        return self.board.get_outcome()

    def set_player_token(self, agent, token):
        #heuristic vars
        local_h = np.array([[2,1,2],[1,3,1],[2,1,2]])
        global_h = np.array([[8,6,8],[6,10,6],[8,6,8]])
        attack_h = np.array([4,5])
        max_time_mcts = .2
        max_time_minmax = .1

        agents = {"Minimax": TimedMinmaxAgent(token, max_time_minmax,
        end_value, attack_heuristic_fun(local_h, attack_h, 1)), 
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
        var1 = StringVar(self.master)
        var1.set("Player 1")
        var2 = StringVar(self.master)
        var2.set("Player 2")
        p1_select = OptionMenu(self.master, var1, "Minimax", "MCTS", "Random", "Human")
        p2_select = OptionMenu(self.master, var2, "Minimax", "MCTS", "Random", "Human")
        p1_select.place(x=550, y=250)
        p2_select.place(x=625, y=250)
        start_game = Button(self.master, text="Start", 
                            command=partial(self.set_opps, var1, var2))
        start_game.place(x=550, y=300)
        grid = []
        for i in range(3):
            for j in range(3):
                board = LocalBoard(self.master)
                self.local_boards[(i, j)] = board 
                b_canvas = board.local_board().grid(row=i, column=j, padx=3, pady=3)

    def make_move(self, move, player):
        token = "X" if player == 1 else "O"
        glob = (move[0], move[1])
        loc = (move[2], move[3])
        board = self.local_boards[glob]
        cell = board.get_cells()[loc]
        cell.configure(text=token)

class LocalBoard(Frame):
    def __init__(self, root):
        self.x = ImageTk.PhotoImage(file="./x.png")
        self.o = ImageTk.PhotoImage(file="./o.png")
        self.root = root
        self.canvas = Canvas(self.root, 
                            width=root.cget("width") // 3, 
                            height=root.cget("width") // 3,
                            bg="#966F33")
        self.cells = {}
        self.create_board()

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

    def change_token(self, coords, token="X"):
        cell = self.cells[coords]
        cell.configure(text="X")

if __name__ == "__main__":
    main()