import tkinter as tk
from tkinter import messagebox
from src.game import Game


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        self.window.geometry("420x520")
        self.window.configure(bg="#1e1e1e")
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        self.game = None
        self.buttons = []

        self.show_menu()

        self.window.mainloop()

    # ---------------- MENU ----------------
    def show_menu(self):
        self.menu = tk.Frame(self.window, bg="#1e1e1e")
        self.menu.pack(pady=30)

        tk.Label(self.menu, text="🎮 Tic-Tac-Toe", fg="white", bg="#1e1e1e",
                 font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(self.menu, text="Player 1 name:", fg="white", bg="#1e1e1e").pack()
        self.p1 = tk.Entry(self.menu)
        self.p1.pack()

        tk.Label(self.menu, text="Player 2 name:", fg="white", bg="#1e1e1e").pack()
        self.p2 = tk.Entry(self.menu)
        self.p2.pack()

        tk.Label(self.menu, text="Mode:", fg="white", bg="#1e1e1e").pack()

        self.mode = tk.StringVar(value="pvp")

        tk.Radiobutton(self.menu, text="PvP", variable=self.mode, value="pvp",
                       bg="#1e1e1e", fg="white").pack()

        tk.Radiobutton(self.menu, text="PvC", variable=self.mode, value="pvc",
                       bg="#1e1e1e", fg="white").pack()

        tk.Label(self.menu, text="Difficulty:", fg="white", bg="#1e1e1e").pack()

        self.diff = tk.StringVar(value="easy")

        tk.OptionMenu(self.menu, self.diff, "easy", "medium", "hard").pack()

        tk.Button(self.menu, text="Start", bg="#4da6ff", fg="white",
                  command=self.start_game).pack(pady=10)

    # ---------------- START ----------------
    def start_game(self):
        name1 = self.p1.get() or "Player 1"
        name2 = self.p2.get() or "Computer"

        mode = self.mode.get()
        diff = self.diff.get()

        self.menu.destroy()

        self.game = Game(
            mode=mode,
            difficulty=diff,
            name1=name1,
            name2=name2
        )

        self.create_board()

    # ---------------- BOARD ----------------
    def create_board(self):
        self.frame = tk.Frame(self.window, bg="#1e1e1e")
        self.frame.pack()

        for i in range(9):
            btn = tk.Button(
                self.frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                bg="#2b2b2b",
                fg="white",
                command=lambda i=i: self.make_move(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

    # ---------------- MOVE ----------------
    def make_move(self, pos):
        if not self.game.play_move(pos):
            return

        self.update_board()

        status = self.game.get_status()

        if status == "draw":
            self.end_game("draw")

        elif "wins" in status:
            self.end_game(self.game.winner.name)

        # ⭐ FIX PvC: IA joga automaticamente
        self.window.after(200, self.handle_ai)

    # ---------------- IA TURN ----------------
    def handle_ai(self):
        if self.game.mode != "pvc":
            return

        if self.game.current_player.name != "Computer":
            return

        pos = self.game.current_player.get_move(self.game.board)
        self.game.play_move(pos)

        self.update_board()

        status = self.game.get_status()

        if status == "draw":
            self.end_game("draw")

        elif "wins" in status:
            self.end_game(self.game.winner.name)

    # ---------------- UPDATE ----------------
    def update_board(self):
        for i in range(9):
            v = self.game.board.grid[i]
            self.buttons[i]["text"] = v

            if v == "X":
                self.buttons[i]["fg"] = "#ff4d4d"
            elif v == "O":
                self.buttons[i]["fg"] = "#4da6ff"

    # ---------------- END ----------------
    def end_game(self, result):
        if result == "draw":
            messagebox.showinfo("Empate", "🤝 Deu velha!")
        else:
            messagebox.showinfo("Vitória", f"🏆 {result} venceu!")

        self.reset()

    def reset(self):
        self.game = None
        self.buttons = []

        self.frame.destroy()
        self.show_menu()