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
        self.menu_frame = tk.Frame(self.window, bg="#1e1e1e")
        self.menu_frame.pack(pady=40)

        title = tk.Label(
            self.menu_frame,
            text="🎮 Tic-Tac-Toe",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        title.pack(pady=10)

        tk.Label(self.menu_frame, text="Player 1 name:", fg="white", bg="#1e1e1e").pack()
        self.p1_entry = tk.Entry(self.menu_frame)
        self.p1_entry.pack()

        tk.Label(self.menu_frame, text="Player 2 name:", fg="white", bg="#1e1e1e").pack()
        self.p2_entry = tk.Entry(self.menu_frame)
        self.p2_entry.pack()

        # modo
        tk.Label(self.menu_frame, text="Mode:", fg="white", bg="#1e1e1e").pack()

        self.mode_var = tk.StringVar(value="pvp")

        tk.Radiobutton(self.menu_frame, text="PvP", variable=self.mode_var, value="pvp", bg="#1e1e1e", fg="white").pack()
        tk.Radiobutton(self.menu_frame, text="PvC", variable=self.mode_var, value="pvc", bg="#1e1e1e", fg="white").pack()

        # dificuldade
        tk.Label(self.menu_frame, text="Difficulty (PvC):", fg="white", bg="#1e1e1e").pack()

        self.diff_var = tk.StringVar(value="easy")

        tk.OptionMenu(self.menu_frame, self.diff_var, "easy", "medium", "hard").pack()

        tk.Button(
            self.menu_frame,
            text="Start Game",
            command=self.start_game,
            bg="#4da6ff",
            fg="white"
        ).pack(pady=10)

    # ---------------- START GAME ----------------
    def start_game(self):
        name1 = self.p1_entry.get() or "Player 1"
        name2 = self.p2_entry.get() or "Computer"

        mode = self.mode_var.get()
        difficulty = self.diff_var.get()

        self.menu_frame.destroy()

        self.game = Game(
            mode=mode,
            difficulty=difficulty,
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

    # ---------------- GAMEPLAY ----------------
    def make_move(self, pos):
        if not self.game.play_move(pos):
            return

        self.update_board()

        status = self.game.get_status()

        if status == "draw":
            self.end_game("draw")

        elif "wins" in status:
            self.end_game(self.game.winner.name)

    def update_board(self):
        for i in range(9):
            value = self.game.board.grid[i]
            self.buttons[i]["text"] = value

            if value == "X":
                self.buttons[i]["fg"] = "#ff4d4d"
            elif value == "O":
                self.buttons[i]["fg"] = "#4da6ff"

    # ---------------- END GAME ----------------
    def end_game(self, result):
        if result == "draw":
            msg = "🤝 Deu velha!\n\nJogar novamente?"
            title = "Empate"
        else:
            msg = f"🏆 {result} venceu!\n\nParabéns!"
            title = "Vitória"

        messagebox.showinfo(title, msg)
        self.reset()

    def reset(self):
        self.game = None
        self.buttons = []

        self.frame.destroy()
        self.show_menu()