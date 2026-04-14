import tkinter as tk
from tkinter import messagebox
from src.game import Game


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("400x550")
        self.window.configure(bg="#121212")

        self.show_menu()
        self.window.mainloop()

    # ---------- MENU ----------
    def show_menu(self):
        self.clear()

        frame = tk.Frame(self.window, bg="#121212")
        frame.pack(expand=True)

        tk.Label(frame, text="TIC TAC TOE",
                 font=("Helvetica", 28, "bold"),
                 fg="#00ffd5", bg="#121212").pack(pady=40)

        self.mode = tk.StringVar(value="pvp")

        options = [
            ("Player vs Player", "pvp"),
            ("Player vs AI", "pvc"),
            ("🔥 Challenge", "challenge")
        ]

        for text, val in options:
            tk.Radiobutton(frame, text=text, value=val,
                           variable=self.mode,
                           fg="white", bg="#121212",
                           selectcolor="#1e1e1e").pack(pady=5)

        tk.Button(frame, text="NEXT",
                  bg="#00ffd5", fg="black",
                  command=self.config_screen).pack(pady=30)

    # ---------- CONFIG ----------
    def config_screen(self):
        self.clear()
        mode = self.mode.get()

        frame = tk.Frame(self.window, bg="#121212")
        frame.pack(expand=True)

        tk.Label(frame, text="Configuration",
                 fg="white", bg="#121212",
                 font=("Helvetica", 18)).pack(pady=20)

        tk.Label(frame, text="Player Name", fg="white", bg="#121212").pack()
        self.name1 = tk.Entry(frame)
        self.name1.pack(pady=10)

        if mode == "pvp":
            tk.Label(frame, text="Player 2 Name", fg="white", bg="#121212").pack()
            self.name2 = tk.Entry(frame)
            self.name2.pack(pady=10)

        if mode == "pvc":
            tk.Label(frame, text="Difficulty", fg="white", bg="#121212").pack()
            self.difficulty = tk.StringVar(value="2")

            tk.Radiobutton(frame, text="Easy", value="1", variable=self.difficulty,
                           fg="white", bg="#121212", selectcolor="#1e1e1e").pack()
            tk.Radiobutton(frame, text="Medium", value="2", variable=self.difficulty,
                           fg="white", bg="#121212", selectcolor="#1e1e1e").pack()
            tk.Radiobutton(frame, text="Hard", value="3", variable=self.difficulty,
                           fg="white", bg="#121212", selectcolor="#1e1e1e").pack()

        tk.Button(frame, text="START",
                  bg="#00ffd5",
                  command=self.start_game).pack(pady=20)

    # ---------- START ----------
    def start_game(self):
        mode = self.mode.get()

        name1 = self.name1.get() or "Player 1"
        name2 = getattr(self, "name2", None)
        name2 = name2.get() if name2 else "AI"

        difficulty = 1

        if mode == "pvc":
            difficulty = int(self.difficulty.get())

        if mode == "challenge":
            difficulty = 99

        self.game = Game(mode, difficulty, name1, name2)

        self.create_board()

    # ---------- BOARD ----------
    def create_board(self):
        self.clear()

        self.canvas = tk.Canvas(self.window, width=300, height=300,
                                bg="#121212", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.click)

        self.status = tk.Label(self.window, text="",
                               fg="white", bg="#121212")
        self.status.pack()

        self.update_status()

    def draw_grid(self):
        for i in range(1, 3):
            self.canvas.create_line(0, i*100, 300, i*100, fill="#2a2a2a", width=4)
            self.canvas.create_line(i*100, 0, i*100, 300, fill="#2a2a2a", width=4)

    def click(self, event):
        col = event.x // 100
        row = event.y // 100
        pos = row * 3 + col
        self.move(pos)

    def move(self, pos):
        if not self.game.play_move(pos):
            return

        self.update()

        if self.game.finished:
            if self.game.winner:
                self.draw_win_line(self.game.win_combo)
            self.end()
            return

        if self.game.mode != "pvp" and self.game.current_player.name == "AI":
            self.window.after(300, self.ai)
        else:
            self.update_status()

    def ai(self):
        pos = self.game.current_player.get_move(
            self.game.board,
            self.game.difficulty
        )

        self.game.play_move(pos)
        self.update()

        if self.game.finished:
            if self.game.winner:
                self.draw_win_line(self.game.win_combo)
            self.end()
            return

        self.update_status()

    def update(self):
        self.canvas.delete("symbol")

        for i in range(9):
            x = (i % 3) * 100 + 50
            y = (i // 3) * 100 + 50
            s = self.game.board.grid[i]

            if s == "X":
                self.canvas.create_text(x, y, text="X",
                                        fill="red",
                                        font=("Helvetica", 40, "bold"),
                                        tags="symbol")
            elif s == "O":
                self.canvas.create_text(x, y, text="O",
                                        fill="blue",
                                        font=("Helvetica", 40, "bold"),
                                        tags="symbol")

    def draw_win_line(self, combo):
        coords = {
            0:(50,50),1:(150,50),2:(250,50),
            3:(50,150),4:(150,150),5:(250,150),
            6:(50,250),7:(150,250),8:(250,250)
        }

        s = coords[combo[0]]
        e = coords[combo[2]]

        self.canvas.create_line(s[0], s[1], e[0], e[1],
                                fill="white", width=6)

    def update_status(self):
        p = self.game.current_player
        self.status.config(text=f"{p.name} turn ({p.symbol})")

    def end(self):
        if self.game.winner:
            messagebox.showinfo("Game Over", f"{self.game.winner.name} wins!")
        else:
            messagebox.showinfo("Game Over", "Draw!")

        self.show_menu()

    def clear(self):
        for w in self.window.winfo_children():
            w.destroy()